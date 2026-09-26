/**
 * Plant Care Strategy
 *
 * Maintains a deep pool of US-focused houseplant care topics and generates
 * GEO-optimized prompts that instruct Gemini to produce expert-level,
 * 2 500+ word articles with comparison tables, FAQ sections, and natural
 * product mentions.
 */

import { pickUnusedTopic, getTopicStats } from '../lib/linker.js';
// ── Topic pool (50+ unique topics for US plant enthusiasts) ──────────────────
const TOPICS = [
  'Spathiphyllum Peace Lily Expert Care Guide',
  'Fiddle Leaf Fig Brown Spots: Causes and Proven Treatments',
  'Predatory Mites vs Neem Oil for Houseplant Pest Control',
  'Monstera Deliciosa Complete Care Guide for US Homes',
  'Why Your Fiddle Leaf Fig Is Dropping Leaves and How to Fix It',
  'Best Low-Light Plants for New York Apartments',
  'Pothos Varieties: Every Type You Can Grow in the US',
  'Snake Plant Care: The Indestructible Houseplant Americans Love',
  'How to Repot a Root-Bound Plant Step by Step',
  'Philodendron Brasil vs Pothos: Differences and Care Tips',
  'Calathea Care Guide: Keeping Prayer Plants Happy Indoors',
  'ZZ Plant Care Guide for Beginners in the United States',
  'Rubber Plant Care: Light, Water, and Pruning Tips',
  'String of Pearls Care Guide: Watering, Light, and Propagation',
  'How to Propagate Monstera from Cuttings at Home',
  'Alocasia Polly Care Guide for Indoor Gardeners',
  'Best Hanging Plants for Small US Apartments',
  'Peace Lily Care: Blooming Tips for American Homes',
  'Bird of Paradise Indoor Care Guide for Warm US Climates',
  'How to Choose the Right Pot Size for Every Houseplant',
  'Spider Plant Care and Propagation for Beginners',
  'Hoya Varieties: Best Wax Plants to Grow Indoors in the US',
  'Chinese Evergreen Care: Low-Light Champion for US Offices',
  'How to Set Up a Plant Shelf with Grow Lights',
  'Anthurium Care Guide: Tropical Blooms in Your Living Room',
  'How to Bottom Water Your Houseplants Correctly',
  'Fern Care Indoors: Boston Fern, Maidenhair, and More',
  'Dracaena Marginata Care Guide for US Plant Parents',
  'Pilea Peperomioides: Chinese Money Plant Care Tips',
  'How to Treat Root Rot in Houseplants Step by Step',
  'Best Air-Purifying Plants Recommended by NASA for US Homes',
  'How to Create a Humidity Tray for Tropical Houseplants',
  'Croton Plant Care: Color, Light, and Temperature Needs',
  'Jade Plant Care Guide: Watering and Sunlight for Succulents',
  'How to Overwinter Outdoor Plants Indoors in Cold US States',
  'Begonia Rex Care: Colorful Foliage for American Collectors',
  'Peperomia Varieties and Care Guide for Indoor Gardens',
  'How to Fertilize Houseplants: Schedules and Best Products',
  'Orchid Care for Beginners: Phalaenopsis Growing Tips',
  'Monstera Adansonii vs Monstera Deliciosa: Which Is Right for You',
  'How to Identify and Treat Common Houseplant Pests in the US',
  'Best Plants for Bathrooms with Low Light and High Humidity',
  'Tradescantia Care Guide: Grow Wandering Dude Like a Pro',
  'How to Grow Herbs Indoors Year-Round in American Kitchens',
  'Dieffenbachia Care Guide: Dumb Cane for US Homes',
  'Majesty Palm Indoor Care: Tropical Vibes in Any Room',
  'How to Use Leca for Semi-Hydro Plant Growing at Home',
  'Syngonium Varieties and Care Tips for US Collectors',
  'How to Acclimate New Plants After Buying Them Online',
  'Bromeliad Care Guide: Exotic Color Without the Fuss',
  'How to Build a DIY Indoor Greenhouse on a Budget',
  'Norfolk Island Pine Care: A Living Christmas Tree Year-Round',
  'Best Pet-Safe Houseplants for Dog and Cat Owners in the US',
  'How to Diagnose Yellow Leaves on Any Houseplant',
  'Cactus Care Indoors: Watering, Light, and Soil Mix Guide',
  'Aloe Vera Care and Uses Every American Should Know',
];

// Export for topic tracking
export { TOPICS };

/**
 * Pick an unused topic from the pool (tracked in SQLite).
 */
export function pickTopic() {
  return pickUnusedTopic(TOPICS, 'plant-care');
}

/**
 * Build a GEO-optimized Gemini prompt for a plant-care article.
 *
 * @returns {string} Prompt text ready to send to Gemini.
 */
export function getPrompt() {
  const topic = pickTopic();

  return `
You are a senior horticulturist and SEO content strategist writing for PlantsMag.com, a leading US-based online plant magazine.

Write an expert-level, comprehensive article about: "${topic}"

REQUIREMENTS:
1. LENGTH: Highly useful, concise, and dense SEO-optimized article of 800-1200 words. Keep H2 sections max 150 words without fluff.
2. AUDIENCE: US plant enthusiasts — use American English, US hardiness zones, US-available products, and US pricing in USD.
3. STRUCTURE (use proper HTML):
   - An engaging H1 title (include the primary keyword naturally)
   - At least 5 H2 sub-headings with detailed paragraphs
   - At least 2 H3 sub-sections under relevant H2s
   - An HTML <table> comparing care requirements (light, water, humidity, soil, temperature)
   - An ordered <ol> list for any step-by-step instructions
   - An FAQ section using <details> and <summary> HTML tags (at least 5 FAQs)
4. PRODUCT MENTIONS: Naturally reference helpful products US plant owners buy (moisture meters, grow lights, specific soil brands, fertilizers). Mention them contextually, not as ads.
5. SEO: Include the primary keyword in the first 100 words, use semantic variations throughout, and write a compelling meta description (under 160 characters).
6. TONE: Friendly, authoritative, like a knowledgeable friend who happens to be a botanist.
7. CRITICAL TITLE RULES: Generate a professional, academic, and problem-solving title. DO NOT use clickbait words like "Instantly", "Ultimate", "Showdown", "Magic", "Secret", or "Miracle". Ensure it matches user search intent perfectly.

Return ONLY valid JSON. No markdown fences. No extra text before or after the JSON.

JSON format:
{
  "title": "SEO-optimized article title",
  "slug": "url-friendly-slug",
  "meta_description": "Compelling meta description under 160 characters",
  "content": "Full HTML article content here"
}
`.trim();
}

/**
 * WordPress category slug for plant-care articles.
 *
 * @returns {string}
 */
export function getCategorySlug() {
  return 'houseplant-guides';
}
