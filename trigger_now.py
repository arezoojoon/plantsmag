"""
PlantsMag Direct Publisher
Generates article via Gemini and publishes to WordPress with fresh credentials.
"""
import json, time, urllib.request, base64, random, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# ── CONFIG ──────────────────────────────────────────────────
GEMINI_KEY = "REDACTED_API_KEY"
WP_USER = "n8n-bloger"
WP_PASS = "VQ05 3amn qMzu aPkX VLsu 6XiA"  # freshly generated
WP_API = "https://plantsmag.com/wp-json/wp/v2/posts"

US_TOPICS = [
    "Spider mites on houseplants: identification treatment and prevention guide 2026",
    "Monstera deliciosa yellowing leaves: complete diagnosis and fix guide",
    "Root rot rescue: how to save your houseplants from overwatering damage",
    "Best soil mix for tropical houseplants: ingredients and DIY recipes 2026",
    "Orchid care mistakes every beginner makes and how to avoid them",
    "Snake plant care guide: watering light and propagation tips for beginners",
    "Pothos varieties guide: golden marble queen neon and more",
    "How to propagate houseplants in water: step by step guide 2026",
    "Best grow lights for indoor plants: LED buyer guide 2026",
    "Calathea care guide: humidity watering and common problems solved",
    "Fiddle leaf fig troubleshooting: brown spots drooping and leaf drop",
    "ZZ plant care ultimate guide: the nearly indestructible houseplant",
    "Peace lily care and flowering tips for beginners 2026",
    "Succulent watering schedule: how often and how much to water",
    "Alocasia care guide: elephant ear plant indoor growing tips",
]

topic = random.choice(US_TOPICS)
print(f"Selected topic: {topic}")

# ── STEP 1: Generate with Gemini ────────────────────────────
print("\n[1/3] Calling Gemini 2.0 Flash...")
gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"

prompt = f"""Write a comprehensive, expert-level 2500-word SEO article about: {topic}.

Target audience: US plant enthusiasts and indoor gardeners.

Requirements:
- Use H2 and H3 subheadings for structure  
- Include practical, actionable advice
- Naturally mention useful Amazon products (moisture meters, grow lights, soil mixes, pots)
- Write in an authoritative yet friendly tone
- Include a brief FAQ section at the end with 3 common questions

Return your response as valid JSON with these exact keys:
{{
  "title": "SEO-optimized article title (60 chars max)",
  "slug": "url-friendly-slug-with-dashes",
  "meta_description": "Compelling meta description under 160 characters",
  "content": "Full HTML article content with h2, h3, p, ul, li tags"
}}

IMPORTANT: Return ONLY the JSON object, no markdown code fences, no extra text."""

payload = json.dumps({
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192}
}).encode()

req = urllib.request.Request(gemini_url, headers={"Content-Type": "application/json"}, data=payload)
try:
    with urllib.request.urlopen(req, timeout=120, context=ctx) as r:
        resp = json.loads(r.read().decode())
        raw_text = resp['candidates'][0]['content']['parts'][0]['text']
        print(f"  Gemini responded: {len(raw_text)} chars")
except Exception as e:
    print(f"  FATAL: Gemini failed: {e}")
    exit(1)

# ── STEP 2: Parse ───────────────────────────────────────────
print("\n[2/3] Parsing article...")
clean = raw_text.strip()
if clean.startswith('```'):
    clean = clean.split('\n', 1)[1] if '\n' in clean else clean[3:]
if clean.endswith('```'):
    clean = clean.rsplit('```', 1)[0]
clean = clean.strip()

try:
    article = json.loads(clean)
    title = article.get('title', 'Plant Care Guide')
    slug = article.get('slug', 'plant-care-guide')
    meta_desc = article.get('meta_description', '')
    content = article.get('content', clean)
except json.JSONDecodeError:
    title = topic.split(':')[0].strip().title()[:60]
    slug = topic.lower().replace(' ', '-').replace(':', '').replace(',', '')[:60]
    meta_desc = topic[:155]
    content = f"<p>{raw_text}</p>"

print(f"  Title: {title}")
print(f"  Slug: {slug}")
print(f"  Content: {len(content)} chars")

# ── STEP 3: Publish ─────────────────────────────────────────
print("\n[3/3] Publishing to WordPress...")
wp_cred = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()

wp_data = json.dumps({
    "title": title,
    "slug": slug,
    "content": content,
    "excerpt": meta_desc,
    "status": "publish"
}).encode()

wp_req = urllib.request.Request(
    WP_API,
    headers={"Authorization": f"Basic {wp_cred}", "Content-Type": "application/json"},
    data=wp_data
)

try:
    with urllib.request.urlopen(wp_req, timeout=30, context=ctx) as r:
        wp_resp = json.loads(r.read().decode())
        print(f"  Post ID: {wp_resp.get('id')}")
        print(f"  URL: {wp_resp.get('link')}")
        print(f"  Status: {wp_resp.get('status')}")
except urllib.error.HTTPError as e:
    error_body = e.read().decode()
    print(f"  WP Error {e.code}: {error_body[:500]}")
except Exception as e:
    print(f"  WP Error: {e}")

print("\n--- DONE ---")
