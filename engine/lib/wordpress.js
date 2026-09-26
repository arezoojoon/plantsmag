/**
 * WordPress REST API Client
 *
 * Publishes posts and manages categories on plantsmag.com via the
 * WP REST API v2 with Basic Auth (application password).
 */

import axios from 'axios';

// ── Configuration ────────────────────────────────────────────────────────────
const WP_SITE     = 'https://plantsmag.com';
const WP_API      = `${WP_SITE}/wp-json/wp/v2`;
const WP_USER     = process.env.WP_USER;
const WP_APP_PASS = process.env.WP_APP_PASS;

if (!WP_USER || !WP_APP_PASS) {
  throw new Error('Missing WP_USER or WP_APP_PASS in environment variables');
}

// Base64-encoded credentials for Basic Auth
const AUTH_TOKEN = Buffer.from(`${WP_USER}:${WP_APP_PASS}`).toString('base64');

/** Pre-configured axios instance with auth headers. */
const wp = axios.create({
  baseURL: WP_API,
  timeout: 30_000,
  headers: {
    'Content-Type':  'application/json',
    Authorization:   `Basic ${AUTH_TOKEN}`,
  },
});

// ── Category helpers ─────────────────────────────────────────────────────────

/**
 * Fetch every category from the site (handles WP pagination).
 *
 * @returns {Promise<Array<{id: number, name: string, slug: string}>>}
 */
export async function getCategories() {
  const categories = [];
  let page = 1;
  let hasMore = true;

  while (hasMore) {
    const { data, headers } = await wp.get('/categories', {
      params: { per_page: 100, page },
    });

    categories.push(
      ...data.map((c) => ({ id: c.id, name: c.name, slug: c.slug })),
    );

    const totalPages = parseInt(headers['x-wp-totalpages'] || '1', 10);
    hasMore = page < totalPages;
    page++;
  }

  return categories;
}

/**
 * Create a new category.
 *
 * @param   {string} name – Human-readable name, e.g. "Houseplant Guides"
 * @param   {string} slug – URL slug, e.g. "houseplant-guides"
 * @returns {Promise<{id: number, name: string, slug: string}>}
 */
export async function createCategory(name, slug) {
  const { data } = await wp.post('/categories', { name, slug });
  return { id: data.id, name: data.name, slug: data.slug };
}

// ── Media uploading ────────────────────────────────────────────────────────────

/**
 * Upload an image to the WordPress Media Library.
 * 
 * @param {Buffer} buffer - Image data buffer
 * @param {string} filename - Filename for the image
 * @param {string} alt - Alt text for the image
 * @returns {Promise<number|null>} The media attachment ID, or null on failure
 */
export async function uploadMedia(buffer, filename, alt) {
  try {
    const { data } = await wp.post('/media', buffer, {
      headers: {
        'Content-Type': 'image/jpeg',
        'Content-Disposition': `attachment; filename="${filename}"`
      }
    });

    const mediaId = data.id;

    // Optional: Set alt text
    if (alt) {
      await wp.post(`/media/${mediaId}`, { alt_text: alt });
    }

    return mediaId;
  } catch (error) {
    console.error('[WordPress] Failed to upload media:', error.response?.data || error.message);
    return null;
  }
}

// ── Post publishing ──────────────────────────────────────────────────────────

/**
 * Resolve a category slug to its numeric WP ID, creating it if necessary.
 *
 * @param   {string} slug
 * @returns {Promise<number>}
 */
async function resolveCategoryId(slug) {
  const cats = await getCategories();
  const existing = cats.find((c) => c.slug === slug);
  if (existing) return existing.id;

  // Auto-create the category with a title-cased name
  const name = slug
    .split('-')
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');

  const created = await createCategory(name, slug);
  return created.id;
}

/**
 * Save a new post to WordPress as DRAFT (pending human review).
 *
 * Articles are saved as drafts so a human editor can review content quality,
 * accuracy, and E-E-A-T compliance before publishing. This protects against
 * Google's Helpful Content Update penalties for unreviewed AI content.
 *
 * Workflow: Engine creates draft → Human reviews in WP dashboard → Publishes
 *
 * @param   {object} opts
 * @param   {string} opts.title    – Post title
 * @param   {string} opts.slug     – URL slug
 * @param   {string} opts.content  – Full HTML content
 * @param   {string} [opts.excerpt]  – Meta description / excerpt
 * @param   {string} [opts.category] – Category slug (resolved or created)
 * @param   {number} [opts.featured_media] - ID of uploaded media for featured image
 * @returns {Promise<{id: number, url: string, status: string}>}
 */
export async function publishPost({ title, slug, content, excerpt, category, featured_media }) {
  // Resolve category
  const categories = category ? [await resolveCategoryId(category)] : [];

  // Always publish automatically as requested by the user
  const status = 'draft';

  if (!slug || slug === 'json-slug' || slug.includes('undefined')) {
    throw new Error(`Invalid slug generated: ${slug}`);
  }

  const { data } = await wp.post('/posts', {
    title,
    slug,
    content,
    excerpt: excerpt || '',
    status,
    categories,
    ...(featured_media && { featured_media }),
  });

  return { id: data.id, url: data.link, status };
}
