/**
 * Pexels API Client
 *
 * Fetches high-quality, free-to-use images for WordPress posts.
 */

import axios from 'axios';
import fs from 'fs';
import path from 'path';

const PEXELS_API_KEY = process.env.PEXELS_API_KEY;

/**
 * Searches Pexels for an image and downloads the medium size version.
 * @param {string} query - The search query (e.g. 'Monstera plant')
 * @returns {Promise<{buffer: Buffer, filename: string, alt: string}|null>}
 */
export async function fetchImageForKeyword(query) {
  if (!PEXELS_API_KEY) {
    console.warn('[Pexels] PEXELS_API_KEY is not set. Skipping image fetch.');
    return null;
  }

  try {
    const response = await axios.get(`https://api.pexels.com/v1/search`, {
      params: { query, per_page: 1, orientation: 'landscape' },
      headers: { Authorization: PEXELS_API_KEY }
    });

    if (response.data.photos && response.data.photos.length > 0) {
      const photo = response.data.photos[0];
      const imageUrl = photo.src.large; // 940x650ish or similar, good for featured image

      // Download the image
      const imageResponse = await axios.get(imageUrl, { responseType: 'arraybuffer' });
      const buffer = Buffer.from(imageResponse.data, 'binary');
      
      const altText = photo.alt || query;
      // Clean query for filename
      const safeQuery = query.toLowerCase().replace(/[^a-z0-9]/g, '-').replace(/-+/g, '-');
      const filename = `${safeQuery}-${photo.id}.jpeg`;

      return {
        buffer,
        filename,
        alt: altText
      };
    }
  } catch (error) {
    console.error('[Pexels] Error fetching image:', error.message);
  }

  return null;
}
