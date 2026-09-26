/**
 * Smart Internal Linking Engine
 *
 * Maintains a local SQLite database of published articles and uses keyword
 * matching to inject contextual internal links into new content.  This boosts
 * topical authority and keeps readers on plantsmag.com longer.
 */

import Database from 'better-sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';

// ── Resolve DB path relative to this file ────────────────────────────────────
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DB_PATH   = path.join(__dirname, '..', 'articles.db');

/** @type {Database.Database | null} */
let db = null;

// ── Common English stop words to ignore during keyword extraction ────────────
const STOP_WORDS = new Set([
  'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
  'her', 'was', 'one', 'our', 'out', 'has', 'have', 'been', 'some', 'them',
  'than', 'its', 'over', 'from', 'that', 'this', 'with', 'will', 'each',
  'make', 'like', 'just', 'into', 'your', 'what', 'when', 'they', 'which',
  'their', 'said', 'about', 'would', 'there', 'could', 'other', 'more',
  'very', 'after', 'also', 'these', 'then', 'only', 'come', 'made', 'find',
  'here', 'thing', 'many', 'well', 'does', 'most', 'best', 'much', 'those',
  'being', 'should', 'back', 'still', 'every', 'even', 'need', 'keep',
  'know', 'take', 'where', 'why', 'how', 'way', 'look', 'help', 'good',
  'great', 'really', 'right', 'going', 'before', 'between', 'both',
  'guide', 'complete', 'ultimate', 'tips',
]);

// ── Initialisation ───────────────────────────────────────────────────────────

/**
 * Open (or create) the SQLite database and ensure the articles table exists.
 */
export function init() {
  db = new Database(DB_PATH);

  // Enable WAL mode for better concurrent read performance
  db.pragma('journal_mode = WAL');

  db.exec(`
    CREATE TABLE IF NOT EXISTS articles (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      wp_id       INTEGER,
      title       TEXT,
      slug        TEXT,
      keywords    TEXT,
      strategy    TEXT,
      url         TEXT,
      created_at  TEXT DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Topic tracking table — prevents duplicate topic selection
  db.exec(`
    CREATE TABLE IF NOT EXISTS used_topics (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      strategy    TEXT NOT NULL,
      topic       TEXT NOT NULL,
      used_at     TEXT DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(strategy, topic)
    )
  `);

  // Index for fast lookup
  db.exec(`CREATE INDEX IF NOT EXISTS idx_used_strategy ON used_topics(strategy)`);
  db.exec(`CREATE INDEX IF NOT EXISTS idx_articles_keywords ON articles(keywords)`);
}

// ── CRUD operations ──────────────────────────────────────────────────────────

/**
 * Persist a published article's metadata for future linking.
 *
 * @param {object} article
 * @param {number} article.wp_id
 * @param {string} article.title
 * @param {string} article.slug
 * @param {string} article.keywords  – Comma-separated keyword list
 * @param {string} article.strategy  – Strategy that generated this article
 * @param {string} article.url       – Full permalink
 */
export function saveArticle({ wp_id, title, slug, keywords, strategy, url }) {
  const stmt = db.prepare(`
    INSERT INTO articles (wp_id, title, slug, keywords, strategy, url)
    VALUES (@wp_id, @title, @slug, @keywords, @strategy, @url)
  `);
  stmt.run({ wp_id, title, slug, keywords, strategy, url });
}

/**
 * Return every article stored in the database.
 *
 * @returns {Array<object>}
 */
export function getAllArticles() {
  return db.prepare('SELECT * FROM articles ORDER BY created_at DESC').all();
}

// ── Topic tracking ───────────────────────────────────────────────────────────

/**
 * Mark a topic as used for a given strategy.
 *
 * @param {string} strategy – Strategy name (e.g. 'plant-care')
 * @param {string} topic    – The full topic string that was used
 */
export function markTopicUsed(strategy, topic) {
  const stmt = db.prepare(`
    INSERT OR IGNORE INTO used_topics (strategy, topic) VALUES (?, ?)
  `);
  stmt.run(strategy, topic);
}

/**
 * Get all used topics for a strategy.
 *
 * @param   {string}   strategy
 * @returns {Set<string>}
 */
export function getUsedTopics(strategy) {
  const rows = db.prepare('SELECT topic FROM used_topics WHERE strategy = ?').all(strategy);
  return new Set(rows.map(r => r.topic));
}

/**
 * Pick an unused topic from a pool. If all topics have been used, reset the
 * tracking table for that strategy and start fresh.
 *
 * @param   {string[]} allTopics  – Full topic pool
 * @param   {string}   strategy   – Strategy name
 * @returns {string}              – Selected unused topic
 */
export function pickUnusedTopic(allTopics, strategy) {
  const used = getUsedTopics(strategy);
  const available = allTopics.filter(t => !used.has(t));

  if (available.length === 0) {
    // All topics exhausted — reset pool
    db.prepare('DELETE FROM used_topics WHERE strategy = ?').run(strategy);
    // Pick random from full pool after reset
    const topic = allTopics[Math.floor(Math.random() * allTopics.length)];
    markTopicUsed(strategy, topic);
    return topic;
  }

  // Pick random from available (unused) topics
  const topic = available[Math.floor(Math.random() * available.length)];
  markTopicUsed(strategy, topic);
  return topic;
}

/**
 * Get tracking stats for a strategy.
 *
 * @param   {string} strategy
 * @param   {number} totalTopics
 * @returns {{ used: number, remaining: number, total: number }}
 */
export function getTopicStats(strategy, totalTopics) {
  const row = db.prepare('SELECT COUNT(*) as cnt FROM used_topics WHERE strategy = ?').get(strategy);
  const used = row.cnt;
  return { used, remaining: totalTopics - used, total: totalTopics };
}

// ── Keyword extraction ───────────────────────────────────────────────────────

/**
 * Extract significant keywords from a title (words > 3 chars, not stop words).
 *
 * @param   {string} title
 * @returns {string[]}
 */
export function extractKeywords(title) {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, '')      // strip punctuation
    .split(/\s+/)
    .filter((w) => w.length > 3 && !STOP_WORDS.has(w));
}

// ── Related-article lookup ───────────────────────────────────────────────────

/**
 * Find existing articles whose keywords overlap with the supplied list.
 *
 * @param   {string[]} keywords – Keywords to match against
 * @param   {number}   [limit=5]
 * @returns {Array<object>}
 */
export function findRelated(keywords, limit = 5) {
  if (!keywords.length) return [];

  // Build a query that scores articles by how many keywords match
  const conditions = keywords.map(() => 'keywords LIKE ?').join(' OR ');
  const params     = keywords.map((kw) => `%${kw}%`);

  const sql = `
    SELECT *, (
      ${keywords.map(() => '(CASE WHEN keywords LIKE ? THEN 1 ELSE 0 END)').join(' + ')}
    ) AS relevance
    FROM articles
    WHERE ${conditions}
    ORDER BY relevance DESC, created_at DESC
    LIMIT ?
  `;

  // Parameters: first set for relevance scoring, second set for WHERE clause
  return db.prepare(sql).all([...params, ...params, limit]);
}

// ── Link injection ───────────────────────────────────────────────────────────

/**
 * Inject up to 5 internal links into article HTML by matching keyword
 * mentions in the content to related articles.
 *
 * Rules:
 *  - Maximum 5 links per article
 *  - Never link the same URL twice
 *  - Case-insensitive, whole-word matching
 *  - Only link plain text (skip content already inside <a> tags)
 *
 * @param   {string}        content          – HTML content of the new article
 * @param   {Array<object>} relatedArticles  – Articles from findRelated()
 * @returns {string}                         – Content with internal links injected
 */
export function injectLinks(content, relatedArticles) {
  if (!relatedArticles.length) return content;

  let result       = content;
  const usedUrls   = new Set();
  let linkCount    = 0;
  const MAX_LINKS  = 5;

  for (const article of relatedArticles) {
    if (linkCount >= MAX_LINKS) break;
    if (usedUrls.has(article.url)) continue;

    // Try to link on each keyword from this related article
    const keywords = (article.keywords || '').split(',').map((k) => k.trim()).filter(Boolean);

    for (const keyword of keywords) {
      if (linkCount >= MAX_LINKS) break;
      if (keyword.length < 4) continue;

      // Match keyword NOT already inside an <a> tag (simple heuristic)
      const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const regex   = new RegExp(`(?<!<a[^>]*>.*?)\\b(${escaped})\\b(?![^<]*<\\/a>)`, 'i');

      if (regex.test(result)) {
        result = result.replace(
          regex,
          `<a href="${article.url}" title="${article.title}">$1</a>`,
        );
        usedUrls.add(article.url);
        linkCount++;
        break; // one link per related article, then move on
      }
    }
  }

  return result;
}
