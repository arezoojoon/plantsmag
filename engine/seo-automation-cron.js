/**
 * PlantsMag SEO Automation Engine – Main Entry Point
 *
 * Orchestrates the full content pipeline:
 *   1. Strategy selection (plant-care, comparison, trending-rss)
 *   2. Prompt generation
 *   3. Gemini article generation
 *   4. Internal-link injection via SQLite keyword matching
 *   5. WordPress publishing
 *   6. Article persistence for future linking
 *
 * Schedule (US Eastern-friendly, 3 articles / day):
 *   08:00 UTC → Plant Care
 *   15:00 UTC → Comparison
 *   21:00 UTC → Trending RSS
 *
 * Run modes:
 *   node seo-automation-cron.js           → start cron daemon
 *   node seo-automation-cron.js --test    → run one article and exit
 */

import 'dotenv/config';
import cron from 'node-cron';
import winston from 'winston';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// ── Library imports ──────────────────────────────────────────────────────────
import { generateArticle } from './lib/gemini.js';
import { publishPost, uploadMedia } from './lib/wordpress.js';
import * as linker from './lib/linker.js';
import { getTrendingPlantTopics } from './lib/rss.js';
import * as pexels from './lib/pexels.js';

// ── Strategy imports ─────────────────────────────────────────────────────────
import * as plantCare from './strategies/plant-care.js';
import * as comparison from './strategies/comparison.js';
import * as trendingRss from './strategies/trending-rss.js';

// ── Paths ────────────────────────────────────────────────────────────────────
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const LOGS_DIR  = path.join(__dirname, 'logs');

// Ensure the logs directory exists
if (!fs.existsSync(LOGS_DIR)) {
  fs.mkdirSync(LOGS_DIR, { recursive: true });
}

// ── Logger (file + console) ──────────────────────────────────────────────────
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.printf(
      ({ timestamp, level, message }) => `${timestamp} [${level.toUpperCase()}] ${message}`,
    ),
  ),
  transports: [
    new winston.transports.File({
      filename: path.join(LOGS_DIR, 'engine.log'),
      maxsize: 5_242_880, // 5 MB
      maxFiles: 5,
    }),
    new winston.transports.Console(),
  ],
});

// ── Strategy registry ────────────────────────────────────────────────────────
const STRATEGIES = {
  'plant-care': plantCare,
  comparison,
  'trending-rss': trendingRss,
};

// ── Core pipeline ────────────────────────────────────────────────────────────

/**
 * Run the full article pipeline for a given strategy.
 *
 * @param {string} strategyName – One of 'plant-care', 'comparison', 'trending-rss'
 */
export async function runOnce(strategyName) {
  const strategy = STRATEGIES[strategyName];
  if (!strategy) {
    logger.error(`Unknown strategy: ${strategyName}`);
    return;
  }

  logger.info(`━━━ Starting pipeline: ${strategyName} ━━━`);

  try {
    // 1. Build the prompt (trending-rss needs RSS data)

    let topicStr = '';
    if (strategyName === 'trending-rss') {
      logger.info('Fetching trending plant topics from RSS…');
      let rssFeed = [];
      try {
        rssFeed = await getTrendingPlantTopics();
        logger.info(`Fetched ${rssFeed.length} trending topics`);
      } catch (rssErr) {
        logger.warn(`RSS fetch failed, using fallback topics: ${rssErr.message}`);
      }
      topicStr = rssFeed.length > 0 ? rssFeed[0].title : 'trending plant';
      prompt = strategy.getPrompt(rssFeed);
    } else {
      topicStr = strategy.pickTopic ? strategy.pickTopic() : '';
      prompt = strategy.getPrompt();
    }

    if (topicStr) {
      logger.info(`Pre-flight checking duplicate for topic: ${topicStr}`);
      const keyword = topicStr.split(' ').slice(0, 3).join('+');
      try {
        const res = await fetch(`https://plantsmag.com/wp-json/wp/v2/posts?search=${encodeURIComponent(keyword)}&per_page=1`);
        const data = await res.json();
        if (data && data.length > 0) {
          logger.warn(`[PRE-FLIGHT] Topic already exists: ${topicStr}. Skipping generation.`);
          return;
        }
      } catch (e) {
        logger.error('Pre-flight check failed: ' + e.message);
      }
    }
    
    logger.info('Prompt generated – calling Gemini API…');


    // 2. Generate article via Gemini
    const article = await generateArticle(prompt);
    logger.info(`Article generated: "${article.title}"`);

    
    // 2.5 Slug lock check
    logger.info(`Checking slug lock for: ${article.slug}`);
    try {
      const slugRes = await fetch(`https://plantsmag.com/wp-json/wp/v2/posts?slug=${article.slug}`);
      const slugData = await slugRes.json();
      if (slugData && slugData.length > 0) {
        logger.warn(`[SLUG LOCK] Slug already exists: ${article.slug}. Aborting publish.`);
        return;
      }
    } catch (e) { }

    // 3. Extract keywords for internal linking

    const keywords = linker.extractKeywords(article.title);
    logger.info(`Extracted keywords: ${keywords.join(', ')}`);

    // 4. Find related articles in SQLite
    const related = linker.findRelated(keywords);
    logger.info(`Found ${related.length} related articles for linking`);

    // 5. Inject internal links
    let enrichedContent = article.content;
    if (related.length > 0) {
      enrichedContent = linker.injectLinks(article.content, related);
      logger.info('Internal links injected');
    }

    // 5.5 Fetch featured image from Pexels
    logger.info('Fetching featured image from Pexels…');
    // Use the first 2 keywords for a better search, or the first one if only one exists
    const imageQuery = keywords.slice(0, 2).join(' ') || 'plant';
    let featured_media = null;
    const imgData = await pexels.fetchImageForKeyword(imageQuery);
    
    if (imgData) {
      logger.info(`Uploading image to WordPress: ${imgData.filename}`);
      featured_media = await uploadMedia(imgData.buffer, imgData.filename, imgData.alt);
      if (featured_media) {
        logger.info(`Media uploaded successfully (ID: ${featured_media})`);
      }
    } else {
      logger.warn('No image found or Pexels API key missing.');
    }

    // 6. Publish to WordPress
    logger.info('Publishing to WordPress…');
    const categorySlug = strategy.getCategorySlug();
    const published = await publishPost({
      title:    article.title,
      slug:     article.slug,
      content:  enrichedContent,
      excerpt:  article.meta_description,
      category: categorySlug,
      featured_media
    });
    logger.info(`Article saved → ID: ${published.id} | Status: ${published.status.toUpperCase()} | URL: ${published.url}`);

    // 7. Save to SQLite for future linking
    linker.saveArticle({
      wp_id:    published.id,
      title:    article.title,
      slug:     article.slug,
      keywords: keywords.join(','),
      strategy: strategyName,
      url:      published.url,
    });
    logger.info('Article saved to link database');

    logger.info(`━━━ Pipeline complete: ${strategyName} ━━━\n`);
  } catch (err) {
    logger.error(`Pipeline failed [${strategyName}]: ${err.message}`);
    logger.error(err.stack);
  }
}

// ── Initialisation ───────────────────────────────────────────────────────────

/** Boot the engine: init SQLite and register cron schedules. */
function startEngine() {
  // Initialise the SQLite link database
  linker.init();
  logger.info('🌿 PlantsMag SEO Engine started');
  logger.info(`   Strategies: ${Object.keys(STRATEGIES).join(', ')}`);
  logger.info('   Schedule:   08:00 plant-care | 15:00 comparison | 21:00 trending-rss');

  // Log topic tracking stats
  const pcStats = linker.getTopicStats('plant-care', plantCare.TOPICS.length);
  const cmStats = linker.getTopicStats('comparison', comparison.TOPICS.length);
  const trStats = linker.getTopicStats('trending-rss', trendingRss.FALLBACK_TOPICS.length);
  logger.info(`   Topic pool: plant-care ${pcStats.remaining}/${pcStats.total} remaining | comparison ${cmStats.remaining}/${cmStats.total} | trending ${trStats.remaining}/${trStats.total}`);

  // ── Cron schedules (3 articles per day) ──────────────────────────────────
  cron.schedule('0 8 * * *', () => {
    logger.info('[CRON] Triggered: plant-care (08:00)');
    runOnce('plant-care');
  });

  // cron.schedule('0 15 * * *', () => {
  //   logger.info('[CRON] Triggered: comparison (15:00)');
  //   runOnce('comparison');
  // });

  // cron.schedule('0 21 * * *', () => {
  //   logger.info('[CRON] Triggered: trending-rss (21:00)');
  //   runOnce('trending-rss');
  // });

  logger.info('Cron jobs registered – engine is running ✔');
}

// ── CLI handling ─────────────────────────────────────────────────────────────

const args = process.argv.slice(2);

if (args.includes('--test')) {
  // Quick-test mode: run one article immediately and exit
  const strategyArg = args.find((a) => a !== '--test') || 'plant-care';
  logger.info(`[TEST MODE] Running single article with strategy: ${strategyArg}`);

  linker.init();

  runOnce(strategyArg)
    .then(() => {
      logger.info('[TEST MODE] Done – exiting.');
      process.exit(0);
    })
    .catch((err) => {
      logger.error(`[TEST MODE] Fatal: ${err.message}`);
      process.exit(1);
    });
} else {
  // Normal daemon mode
  startEngine();
}
