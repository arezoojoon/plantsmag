/**
 * Product Comparison Strategy
 *
 * Generates GEO-optimized comparison and review articles targeting
 * commercial-intent plant-product queries.  Articles include HTML
 * comparison tables, US pricing, and natural Amazon product references.
 */

import { pickUnusedTopic, getTopicStats } from '../lib/linker.js';
// ── Comparison topic pool (30+ topics) ───────────────────────────────────────
const TOPICS = [
  'Best Grow Lights for Indoor Plants 2026: LED vs Full Spectrum',
  'Top 10 Self-Watering Pots: Tested and Reviewed',
  'Best Soil Mix for Aroids: Store-Bought vs DIY',
  'Moisture Meter Showdown: Which One Actually Works?',
  'Best Indoor Plant Fertilizers: Liquid vs Slow-Release Compared',
  'Top Humidifiers for Plant Rooms 2026: Warm Mist vs Cool Mist',
  'Best Planters for Monstera: Ceramic vs Terracotta vs Plastic',
  'Pruning Shears Compared: Felco vs Fiskars vs ARS',
  'Best Potting Benches for Indoor Gardeners in 2026',
  'Peat Moss vs Coco Coir: Which Is Better for Houseplants?',
  'Best Watering Cans for Indoor Plants: Top Picks Reviewed',
  'Smart Plant Sensors Compared: Xiaomi vs ECOWITT vs Sustee',
  'Best Seed Starting Kits for US Home Gardeners 2026',
  'Top Plant Stands for Small Apartments: Style Meets Function',
  'Neem Oil vs Insecticidal Soap: Best Pest Control for Houseplants',
  'Best Perlite vs Pumice vs Vermiculite for Soil Amendments',
  'Indoor Greenhouse Cabinets Compared: IKEA vs Milsbo vs Custom',
  'Best Hanging Basket Liners: Coco vs Sphagnum vs Plastic',
  'Top Grow Tents for Indoor Plant Propagation 2026',
  'Best Orchid Pots: Clear Plastic vs Ceramic vs Net Pots',
  'Best Plant Labels and Markers for Organized Collections',
  'Top Drip Irrigation Kits for Indoor Plant Shelves',
  'Best Root Hormone Products: Gel vs Powder vs Liquid',
  'Worm Castings vs Compost: Which Feeds Houseplants Better?',
  'Best Plant Apps 2026: Planta vs Greg vs Vera Compared',
  'Top Terracotta Pots: Handmade vs Machine-Made Quality Test',
  'Best Moss Poles for Climbing Plants: Coco vs Sphagnum vs Plastic',
  'Leca vs Pon vs Perlite: Best Semi-Hydro Substrate Compared',
  'Best Plant Heat Mats for Winter Propagation in Cold US States',
  'Top Macramé Plant Hangers: Handmade vs Store-Bought Review',
  'Best Water Filters for Houseplants: Brita vs Inline vs Distilled',
  'Systemic Insecticide Granules: Bonide vs BioAdvanced Compared',
];

// Export for topic tracking
export { TOPICS };

/**
 * Pick an unused comparison topic from the pool (tracked in SQLite).
 */
export function pickTopic() {
  return pickUnusedTopic(TOPICS, 'comparison');
}

/**
 * Build a GEO-optimized Gemini prompt for a comparison/review article.
 *
 * @returns {string} Prompt text ready to send to Gemini.
 */
export function getPrompt() {
  const topic = pickTopic();

  return `
You are a product-review specialist and indoor-gardening expert writing for PlantsMag.com, a leading US plant magazine.

Write a comprehensive, honest comparison article about: "${topic}"

REQUIREMENTS:
1. LENGTH: Highly useful, concise, and dense SEO-optimized article of 800-1200 words. Keep H2 sections max 150 words without fluff.
2. AUDIENCE: US plant hobbyists — use American English, USD pricing, and products available on Amazon US or US retailers.
3. STRUCTURE (use proper HTML):
   - An engaging H1 title with the year and primary keyword
   - At least 5 H2 sub-headings covering different products or comparison angles
   - An HTML <table> comparing products with columns for: Product Name, Price Range, Pros, Cons, Best For
   - Detailed pros/cons for each product in <ul> lists
   - A "How We Tested" or "What to Look For" section with an ordered <ol> list
   - A "Verdict" or "Our Top Pick" section
   - An FAQ section using <details> and <summary> HTML tags (at least 4 FAQs)
4. PRODUCT DETAILS: Write as if you have hands-on experience. Include specific model names, realistic US price ranges, and where to buy (primarily Amazon). Do NOT include actual affiliate links.
5. SEO: Include the primary keyword in the first 100 words, use buyer-intent variations, and write a compelling meta description (under 160 characters).
6. TONE: Trustworthy, helpful reviewer — honest about pros AND cons.
7. CRITICAL TITLE RULES: Generate a professional, academic, and problem-solving title. DO NOT use clickbait words like "Instantly", "Ultimate", "Showdown", "Magic", "Secret", or "Miracle". Ensure it perfectly matches user search intent.

Return ONLY valid JSON. No markdown fences. No extra text before or after the JSON.

JSON format:
{
  "title": "SEO-optimized comparison title with year",
  "slug": "url-friendly-slug",
  "meta_description": "Compelling meta description under 160 characters",
  "content": "Full HTML article content here"
}
`.trim();
}

/**
 * WordPress category slug for comparison/review articles.
 *
 * @returns {string}
 */
export function getCategorySlug() {
  return 'trending';
}
