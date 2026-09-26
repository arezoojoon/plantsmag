# PlantsMag SEO & Content Automation Architecture Guide
**Version:** 1.0.0
**Target Environment:** PlantsMag Premium (WordPress Custom Core)
**Objective:** Maintain, scale, and develop the 10/10 SEO and Automated Content pipeline.

---

## 🚀 Strategy 1: The "YouTube Sniper" Content Pipeline

### Concept
Instead of chasing high-competition "broad" keywords (e.g., "how to grow monstera"), PlantsMag targets highly specific, user-panicked, long-tail queries typically found as click-bait YouTube videos (e.g., "Why is my Monstera crying water?"). This guarantees high intent and low competition.

### Implementation Scripts
- **File Names:** `mass_import_publish_25.php`, `mass_publish_3.php`, `mass_publish_5_latest.php`
- **Location:** Project Root (`d:\project\plantsmag\`) -> uploaded to server root `/public_html/`
- **Mechanism:**
  - Uses native WordPress functions `wp_insert_post()` and `wp_insert_attachment()`.
  - Automatically moves physical image files from `tmp_upload/mass_images/` into the official WordPress `wp-content/uploads/` directory.
  - Attaches the image as the "Featured Image" and assigns the post to the "Trending" category (ID: 5).

### Maintenance & Scaling
To publish another batch:
1. Update the `$articles` array inside a duplicate script with new titles, content, and image paths.
2. Upload the images via SCP to `/public_html/tmp_upload/mass_images/`.
3. Run the script via SSH: `php mass_publish_new.php`.

---

## 📈 Strategy 2: The "Mega-Content" Expansion (2500+ Words)

### Concept
Google\'s Algorithm strongly penalizes "Thin Content" (articles under 600 words). To guarantee 10/10 Content SEO without manually writing 12,500 words per day, a programmatic "Hydration" script was created to transform short articles into massive 2500+ word deep-dives.

### Implementation Scripts
- **File Name:** `mass_seo_expansion_all.php`
- **Location:** Server root `/public_html/`
- **Mechanism:**
  - Performs a massive `WP_Query` fetching **all 150 published articles** containing `post_type => 'post'`.
  - Append an invisible-to-user but highly-indexed `epic-seo-expansion` HTML block containing 1,500+ words of advanced taxonomy (PPFD, DLI, CEC, Capillary action).
  - Uses `strpos()` to check if the expansion already exists to absolutely prevent duplicate appending, then updates the database via `wp_update_post()`.

### Maintenance & Scaling
- **Idempotency:** The script is completely safe to run multiple times. If an article already has the `epic-seo-expansion` class, the script skips it.
- **Future Use:** Whenever n8n or an admin publishes a new batch of 50 short AI articles, simply run `php mass_seo_expansion_all.php` on the server one time to instantly convert all 50 new articles into 2500+ word SEO megacontent.

---

## 🕸️ Strategy 3: 10/10 Technical SEO & The Wiki-Net

### Concept
Heavy SEO plugins like Yoast or RankMath add hundreds of database queries and bloat CSS/JS, ruining the 100/100 Core Web Vitals speed score. The Technical SEO strategy was handled completely natively via code. The "Wiki-Net" strategy ensures a 0% orphaned page rate by algorithmically interlinking the entire database exactly like Wikipedia.

### Implementation Scripts

#### Part A: Native Technical Meta Engine
- **File Name:** `functions.php` (inside `plantsmag-premium` theme)
- **Mechanism:**
  - The function `plantsmag_dynamic_seo_meta_tags()` hooks into `wp_head`.
  - Generates `<link rel="canonical">` dynamically.
  - Automatically strips HTML and shortcodes from `$post->post_content` to generate an organic `<meta name="description">` limit 35 words.
  - Injects Social Media Open Graph tags (`og:title`, `og:image`, `og:description`, `twitter:card`) pulling the Featured Image automatically so links look professional on WhatsApp and LinkedIn.

#### Part B: Automated Semantic Interlinker 
- **File Name:** `mass_seo_interlinker.php`
- **Location:** Server root `/public_html/`
- **Mechanism:**
  - Contains a heavy-duty associative array mapping high-value Targets to URLs (e.g., `'root rot' => '/category/diseases/root-rot/'`).
  - Iterates through the database.
  - Uses highly advanced PHP Regex (`preg_replace` with negative lookarounds `(?![^<]*>|[^<>]*<\/a>)`) to find the **first instance** of a target keyword inside the raw text.
  - It specifically prevents wrapping text inside existing `href` tags or image `alt` attributes.
  - Injects a branded `<a class="seo-auto-link">` tag around the target word precisely **1 time per post** to prevent spammy over-linking.

### Maintenance & Scaling
- If you launch a new tool (e.g., a "Repotting AI"), simply add `'repotting' => '/repotting-tool/'` to the `$keyword_map` array inside `mass_seo_interlinker.php`.
- Run `php mass_seo_interlinker.php` via SSH. Within 3 seconds, all 150+ articles in your database will retroactively point a highly-contextual backlink to your new tool.

---

## 🛑 Critical CSS Maintenance Note
- The `<h1>` size on single posts was structurally overriding generic styles. The size is permanently locked at a clean magazine size via `h1.entry-title { font-size: clamp(1.2rem, 2vw, 1.8rem) !important; }` in `style.css`. 
- **Inline Safety:** A hardcoded `style="font-size: clamp(1.2rem, 2.5vw, 2rem) !important;"` exists in `template-parts/content-single.php` to absolutely bypass Hostinger CDN caching. Do not remove this inline style unless you have root access to flush the edge cache.

---

## 🤖 Strategy 4: The Continuous SEO Optimizer (n8n Bot)

### Concept
To achieve massive rankings (Top 1-5 positions) and exponential traffic scaling across the entire network, content cannot remain static. Google's Query Deserves Freshness (QDF) algorithm heavily rewards actively updated content. The **Master SEO Optimizer** acts as an automated Senior SEO Expert.

### Implementation Scripts
- **File Name:** `n8n_master_seo_optimizer.json`
- **Location:** `d:\project\n8n\n8n_workflows-artinwebs.com\`
- **Mechanism:**
  - Designed natively within n8n to manage 7 separate websites from a single Master Configuration.
  - **Randomized Trigger:** Runs periodically but picks a random subset of sites and random wait times (30 to 150 minutes) to exactly replicate manual human editing. This prevents any bot footprint and protects against Google Content Spam Penalties.
  - **LSI Keyword Injection:** Connects to Gemini to intelligently rewrite 2-3 paragraphs. This natively injects Latent Semantic Indexing (LSI) sales-focused keywords into historical content.
  - **Dynamic Link Building:** Reads the document and finds organic places to drop highly relevant internal anchor text pointing to new critical pages.
  - **Media Enrichment Audit:** Checks if an article is media-poor (< 2 images). If so, it dynamically queries AI (Pollinations.ai) to generate a high-quality relevant image and uploads it via the WordPress API.
  - **Meta Reboot:** Re-writes the Yoast Meta Description if it determines the current one has a weak Click-Through-Rate (CTR) potential.

### Maintenance & Scaling
- The only maintenance required for the 7 sites is keeping the `sites` array populated inside the n8n Master Configuration block (`Select Dynamic Site`). Add the new sites' WP REST API credentials and target keywords directly inside n8n.
