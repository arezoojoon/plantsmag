/**
 * Trending RSS Strategy
 *
 * Leverages real-time Google News headlines to produce "newsjacking" articles
 * that ride trending plant topics.  Falls back to an evergreen topic pool
 * when the RSS feed is empty or unreachable.
 */

import { pickUnusedTopic, getTopicStats } from '../lib/linker.js';
// ── Fallback topics in case RSS returns nothing ──────────────────────────────
const FALLBACK_TOPICS = [
  'Why Houseplant Sales Are Booming Again Across the United States',
  'The Rise of Plant Subscription Boxes: Are They Worth It?',
  'How Climate Change Is Affecting Indoor Gardening in the US',
  'Rare Plant Market Trends: What Collectors Are Buying in 2026',
  'Social Media Plant Trends: From TikTok to Your Living Room',
  'How US Millennials Turned Houseplants into a Lifestyle Movement',
  'Urban Farming in American Cities: A Growing Trend',
  'The Science Behind Talking to Your Plants: Myth or Fact?',
  'Plant Theft Is Rising in the US: How to Protect Your Collection',
  'How the USDA Plant Hardiness Zones Are Shifting in 2026',
  'Biophilic Design: Why US Offices Are Filling Up with Plants',
  'The Comeback of Victory Gardens in Suburban America',
  'Are Artificial Plants Finally Acceptable? The Great Debate',
  'How US Nurseries Are Adapting to Supply Chain Challenges',
  'Plant Parenthood: How Houseplants Help American Mental Health',
];

// Export for topic tracking
export { FALLBACK_TOPICS };

/**
 * Pick a trending topic from RSS data, or fall back to an unused evergreen topic.
 *
 * @param   {Array<{title: string, link: string, pubDate: string}>} [rssFeed]
 * @returns {string} A topic headline to write about.
 */
function pickTopic(rssFeed) {
  if (rssFeed && rssFeed.length > 0) {
    // RSS topics are always fresh (news), no need to track
    const pool = rssFeed.slice(0, 5);
    return pool[Math.floor(Math.random() * pool.length)].title;
  }

  // Fallback: use tracked picker to avoid repeats
  return pickUnusedTopic(FALLBACK_TOPICS, 'trending-rss');
}

/**
 * Build a GEO-optimized Gemini prompt based on a trending headline.
 *
 * @param   {Array<{title: string, link: string, pubDate: string}>} [rssFeed]
 * @returns {string} Prompt text ready to send to Gemini.
 */
export function getPrompt(rssFeed) {
  const topic = pickTopic(rssFeed);

  return `
You are a senior plant journalist and SEO strategist writing for PlantsMag.com, a leading US-based online plant magazine.

A trending news headline in the plant world is: "${topic}"

Write a timely, in-depth article that covers this topic from the perspective of a plant expert speaking to US plant enthusiasts.

REQUIREMENTS:
1. LENGTH: Highly useful, concise, and dense SEO-optimized article of 800-1200 words. Keep H2 sections max 150 words without fluff.
2. AUDIENCE: US plant lovers — use American English, reference US retailers, USDA zones, and US cultural context.
3. STRUCTURE (use proper HTML):
   - An engaging H1 title that captures the trending angle with an SEO keyword
   - At least 5 H2 sub-headings exploring different facets of the story
   - At least 2 H3 sub-sections for deeper dives
   - An HTML <table> summarizing key data points (if applicable)
   - Blockquotes for expert opinions or notable statements
   - An FAQ section using <details> and <summary> HTML tags (at least 4 FAQs)
4. NEWSJACKING: Tie the trending topic back to actionable plant-care advice US readers can use. Make the article both newsworthy AND evergreen.
5. PRODUCT CONTEXT: Where relevant, mention products US plant owners might find useful (grow lights, soil, tools) — keep mentions natural and helpful.
6. SEO: Work the primary keyword into the first 100 words, use semantic variations, and write a compelling meta description (under 160 characters).
7. TONE: Authoritative journalist meets friendly plant expert. Informative but never dry.

Return ONLY valid JSON. No markdown fences. No extra text before or after the JSON.

JSON format:
{
  "title": "SEO-optimized trending article title",
  "slug": "url-friendly-slug",
  "meta_description": "Compelling meta description under 160 characters",
  "content": "Full HTML article content here"
}
`.trim();
}

/**
 * WordPress category slug for trending / blog articles.
 *
 * @returns {string}
 */
export function getCategorySlug() {
  return 'blog';
}
