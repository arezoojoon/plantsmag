/**
 * Google News RSS Parser
 *
 * Fetches trending plant-related topics from multiple Google News RSS feeds,
 * filters for English content, and returns the 10 most recent items.
 */

import Parser from 'rss-parser';

const parser = new Parser({
  timeout: 15_000,
  headers: {
    'User-Agent': 'PlantsMag-SEO-Engine/1.0',
    'Accept-Language': 'en-US,en;q=0.9',
  },
});

// ── Google News RSS feeds targeting US plant enthusiasts ──────────────────────
const FEEDS = [
  'https://news.google.com/rss/search?q=houseplant+care+tips&hl=en-US&gl=US',
  'https://news.google.com/rss/search?q=indoor+gardening+2026&hl=en-US&gl=US',
  'https://news.google.com/rss/search?q=rare+plants+trending&hl=en-US&gl=US',
];

/**
 * Fetch and merge items from all RSS feeds.
 *
 * @returns {Promise<Array<{title: string, link: string, pubDate: string}>>}
 *          Top 10 trending items sorted newest-first.
 */
export async function getTrendingPlantTopics() {
  const allItems = [];

  // Fetch all feeds concurrently – if one fails, the others still contribute
  const results = await Promise.allSettled(
    FEEDS.map((url) => parser.parseURL(url)),
  );

  for (const result of results) {
    if (result.status === 'fulfilled' && result.value?.items) {
      for (const item of result.value.items) {
        // Basic English filter: skip items whose titles contain non-Latin chars
        if (item.title && /^[\x20-\x7E]+$/.test(item.title)) {
          allItems.push({
            title:   item.title,
            link:    item.link || '',
            pubDate: item.pubDate || item.isoDate || new Date().toISOString(),
          });
        }
      }
    }
  }

  // Sort by publication date (newest first) and return the top 10
  allItems.sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate));

  return allItems.slice(0, 10);
}
