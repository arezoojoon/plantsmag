/**
 * Gemini API Client
 *
 * Calls the Gemini 2.0 Flash model to generate SEO-optimized plant articles.
 * Includes retry logic with exponential back-off, multiple JSON-parsing
 * strategies, and automatic markdown-fence stripping.
 */

import axios from 'axios';

// ── Configuration ────────────────────────────────────────────────────────────
const API_KEY = process.env.GEMINI_API_KEY;
if (!API_KEY) {
  throw new Error('Missing GEMINI_API_KEY in environment variables');
}
const MODEL         = 'gemini-2.5-flash';
const ENDPOINT      = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${API_KEY}`;
const TIMEOUT_MS    = 120_000;   // 120 seconds – long prompts need breathing room
const MAX_RETRIES   = 3;
const BASE_DELAY_MS = 2_000;     // first retry waits ~2 s

// ── Helpers ──────────────────────────────────────────────────────────────────

/**
 * Strip markdown code fences (```json … ```) that the model sometimes wraps
 * around its output despite being told not to.
 */
function stripMarkdownFences(text) {
  let cleaned = text.trim();

  // Remove leading ```json or ``` and trailing ```
  cleaned = cleaned.replace(/^```(?:json)?\s*\n?/i, '');
  cleaned = cleaned.replace(/\n?```\s*$/i, '');

  return cleaned.trim();
}

function parseJSON(raw) {
  // Completely strip all markdown code fences, regardless of where they appear
  let cleaned = raw.replace(/```(?:json)?/gi, '').replace(/```/g, '').trim();

  // Strategy 1 – direct parse
  try {
    return JSON.parse(cleaned);
  } catch { /* fall through */ }

  // Strategy 2 – Extract from first { to last }
  const first = cleaned.indexOf('{');
  const last  = cleaned.lastIndexOf('}');
  if (first !== -1 && last !== -1 && last > first) {
    const jsonStr = cleaned.substring(first, last + 1);
    try {
      // Clean control characters that might break JSON.parse
      const sanitized = jsonStr.replace(/[\u0000-\u0019]+/g, "");
      return JSON.parse(sanitized);
    } catch (e) {
       console.error('[JSON Parse Strategy 2 Failed]:', e.message);
    }
  }

  console.error('[JSON Parse Error] Raw text was:', raw.substring(0, 500) + '...');
  throw new Error('Failed to parse Gemini response as JSON');
}

/**
 * Sleep helper for exponential back-off.
 */
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// ── Public API ───────────────────────────────────────────────────────────────

/**
 * Generate a plant-care article via Gemini 2.0 Flash.
 *
 * @param   {string} prompt – The full prompt to send to the model.
 * @returns {Promise<{title: string, slug: string, meta_description: string, content: string}>}
 */
export async function generateArticle(prompt) {
  let lastError;

  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    try {
      const response = await axios.post(
        ENDPOINT,
        {
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: {
            temperature: 0.7,
            maxOutputTokens: 8192,
            responseMimeType: 'application/json',
          },
        },
        { timeout: TIMEOUT_MS },
      );

      // Extract the text payload from Gemini's response envelope
      const text =
        response.data?.candidates?.[0]?.content?.parts?.[0]?.text ?? '';

      if (!text) {
        throw new Error('Empty response from Gemini API');
      }

      const article = parseJSON(text);

      // Validate required fields
      if (!article.title || !article.slug || !article.content) {
        throw new Error(
          `Missing required fields in Gemini response. Got keys: ${Object.keys(article).join(', ')}`,
        );
      }

      return {
        title:            article.title,
        slug:             article.slug,
        meta_description: article.meta_description || '',
        content:          article.content,
      };
    } catch (err) {
      lastError = err;

      const status = err.response?.status;
      // Don't retry on auth or bad-request errors
      if (status === 401 || status === 403) {
        throw new Error(`Gemini auth error (${status}): ${err.message}`);
      }

      if (attempt < MAX_RETRIES) {
        const delay = BASE_DELAY_MS * Math.pow(2, attempt - 1);
        console.warn(
          `[Gemini] Attempt ${attempt}/${MAX_RETRIES} failed – retrying in ${delay}ms…`,
        );
        await sleep(delay);
      }
    }
  }

  throw new Error(
    `Gemini API failed after ${MAX_RETRIES} attempts: ${lastError?.message}`,
  );
}
