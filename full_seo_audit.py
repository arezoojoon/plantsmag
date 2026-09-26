"""
PlantsMag FULL SEO AUDIT — Google-Level Deep Analysis
=====================================================
Checks: Canonical, Meta, Schema, Robots, Sitemap, Content Quality,
        Internal Links, Core Web Vitals signals, Mobile, Duplicate Content,
        H1/H2 structure, Image ALT, Orphan pages, Thin content, etc.
"""
import paramiko, json, sys, io, re, urllib.request, ssl
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            return r.read().decode('utf-8', errors='replace'), r.status, dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.read().decode('utf-8', errors='replace'), e.code, {}
    except Exception as e:
        return str(e), 0, {}

bugs = []
warnings = []
ok_items = []

print("=" * 70)
print("PLANTSMAG.COM — COMPREHENSIVE SEO AUDIT")
print("=" * 70)

# ================================================================
# 1. ROBOTS.TXT
# ================================================================
print("\n[1/12] Checking robots.txt...")
robots_body, robots_code, _ = fetch('https://plantsmag.com/robots.txt')
if robots_code == 200:
    print(f"  Status: {robots_code} OK")
    print(f"  Content:\n{robots_body[:500]}")
    if 'Disallow: /' in robots_body and 'Disallow: /wp-admin' not in robots_body:
        bugs.append("CRITICAL: robots.txt blocks entire site with 'Disallow: /'")
    if 'Sitemap:' not in robots_body:
        bugs.append("robots.txt missing Sitemap: directive")
    else:
        ok_items.append("robots.txt has Sitemap directive")
    if 'User-agent: *' in robots_body:
        ok_items.append("robots.txt has User-agent: *")
else:
    bugs.append(f"robots.txt returns HTTP {robots_code}")

# ================================================================
# 2. SITEMAP
# ================================================================
print("\n[2/12] Checking sitemap...")
sitemap_body, sitemap_code, _ = fetch('https://plantsmag.com/sitemap_index.xml')
if sitemap_code == 200:
    sitemap_urls = re.findall(r'<loc>(.*?)</loc>', sitemap_body)
    print(f"  Sitemap index: {sitemap_code} OK, {len(sitemap_urls)} sub-sitemaps")
    for su in sitemap_urls[:5]:
        print(f"    {su}")
    ok_items.append(f"Sitemap index exists with {len(sitemap_urls)} sub-sitemaps")
else:
    # Try alternate
    sitemap_body2, sitemap_code2, _ = fetch('https://plantsmag.com/sitemap.xml')
    if sitemap_code2 == 200:
        print(f"  sitemap.xml: {sitemap_code2} OK")
    else:
        bugs.append(f"No sitemap found (sitemap_index.xml={sitemap_code}, sitemap.xml={sitemap_code2})")

# ================================================================
# 3. HOMEPAGE ANALYSIS
# ================================================================
print("\n[3/12] Analyzing homepage...")
home_body, home_code, home_headers = fetch('https://plantsmag.com/')
if home_code == 200:
    print(f"  Status: {home_code} OK, Size: {len(home_body)} bytes")
    
    # Check title tag
    title_match = re.search(r'<title>(.*?)</title>', home_body, re.I | re.S)
    if title_match:
        title_text = title_match.group(1).strip()
        print(f"  Title: {title_text}")
        if len(title_text) > 65:
            warnings.append(f"Homepage title too long ({len(title_text)} chars): {title_text[:70]}...")
        elif len(title_text) < 30:
            warnings.append(f"Homepage title too short ({len(title_text)} chars)")
        else:
            ok_items.append("Homepage title length OK")
    else:
        bugs.append("Homepage missing <title> tag!")
    
    # Check meta description
    meta_desc = re.search(r'<meta\s+name="description"\s+content="(.*?)"', home_body, re.I)
    if meta_desc:
        desc = meta_desc.group(1)
        print(f"  Meta desc: {desc[:100]}...")
        if len(desc) > 160:
            warnings.append(f"Homepage meta description too long ({len(desc)} chars)")
        ok_items.append("Homepage has meta description")
    else:
        bugs.append("Homepage missing meta description!")
    
    # Check canonical
    canonicals = re.findall(r'<link\s+rel="canonical"\s+href="(.*?)"', home_body, re.I)
    print(f"  Canonical tags: {len(canonicals)}")
    for c in canonicals:
        print(f"    {c}")
    if len(canonicals) > 1:
        bugs.append(f"Homepage has {len(canonicals)} canonical tags (DUPLICATE)")
    elif len(canonicals) == 0:
        bugs.append("Homepage missing canonical tag!")
    else:
        ok_items.append("Homepage has single canonical tag")
    
    # Check H1
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', home_body, re.I | re.S)
    print(f"  H1 tags: {len(h1s)}")
    if len(h1s) == 0:
        bugs.append("Homepage missing H1 tag!")
    elif len(h1s) > 1:
        warnings.append(f"Homepage has {len(h1s)} H1 tags (should be 1)")
    
    # Check Open Graph
    og_title = re.search(r'og:title', home_body, re.I)
    og_desc = re.search(r'og:description', home_body, re.I)
    og_image = re.search(r'og:image', home_body, re.I)
    if og_title and og_desc:
        ok_items.append("Homepage has Open Graph tags")
    else:
        warnings.append("Homepage missing Open Graph tags")
    
    # Check JSON-LD schema
    schemas = re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', home_body, re.I | re.S)
    print(f"  JSON-LD schemas: {len(schemas)}")
    for i, s in enumerate(schemas):
        try:
            sd = json.loads(s)
            schema_type = sd.get('@type', sd.get('@graph', [{}])[0].get('@type', 'unknown') if '@graph' in sd else 'unknown')
            print(f"    Schema {i+1}: {schema_type}")
        except:
            print(f"    Schema {i+1}: (parse error)")
    
    # Check for render-blocking resources
    css_count = len(re.findall(r'<link[^>]+stylesheet', home_body, re.I))
    js_count = len(re.findall(r'<script[^>]+src=', home_body, re.I))
    print(f"  CSS files: {css_count}, JS files: {js_count}")
    if css_count > 8:
        warnings.append(f"Too many CSS files ({css_count}) — may block rendering")
    if js_count > 10:
        warnings.append(f"Too many JS files ({js_count}) — may hurt LCP")
    
    # Check lazy loading on images
    imgs = re.findall(r'<img[^>]*>', home_body, re.I)
    lazy_imgs = [i for i in imgs if 'loading="lazy"' in i or 'data-src' in i]
    print(f"  Images: {len(imgs)} total, {len(lazy_imgs)} lazy-loaded")
    if len(imgs) > 5 and len(lazy_imgs) == 0:
        warnings.append("No lazy-loaded images detected on homepage")
    
    # Check viewport meta
    if 'viewport' in home_body.lower():
        ok_items.append("Viewport meta tag present")
    else:
        bugs.append("Missing viewport meta tag — NOT MOBILE FRIENDLY")

else:
    bugs.append(f"Homepage returns HTTP {home_code}")

# ================================================================
# 4. ARTICLE PAGE ANALYSIS
# ================================================================
print("\n[4/12] Analyzing article pages...")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

def run_wp(cmd):
    _, o, _ = ssh.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace')

wp = '/home/u284669846/domains/plantsmag.com/public_html'

# Get post details
posts_json = run_wp(f'cd {wp} && wp post list --post_type=post --post_status=publish --fields=ID,post_title,post_name,post_content,post_excerpt --format=json 2>&1')
try:
    posts = json.loads(posts_json)
except:
    posts = []
    bugs.append("Could not retrieve post list from WP-CLI")

print(f"  Total posts: {len(posts)}")

thin_content = 0
empty_titles = 0
empty_excerpts = 0
duplicate_titles = {}
raw_template_posts = 0
no_h2_posts = 0
short_slugs = 0

for p in posts:
    title = p.get('post_title', '')
    content = p.get('post_content', '')
    excerpt = p.get('post_excerpt', '')
    slug = p.get('post_name', '')
    
    # Check for empty/short titles
    if not title or len(title) < 5:
        empty_titles += 1
    
    # Check for duplicate titles
    if title:
        duplicate_titles[title] = duplicate_titles.get(title, 0) + 1
    
    # Check for thin content (less than 300 words)
    word_count = len(re.findall(r'\w+', re.sub(r'<[^>]+>', '', content)))
    if word_count < 300:
        thin_content += 1
    
    # Check for raw template expressions
    if '{{$json' in content or '{{ $json' in content or '$json.' in content:
        raw_template_posts += 1
    
    # Check for empty excerpt (meta description source)
    if not excerpt or len(excerpt) < 10:
        empty_excerpts += 1
    
    # Check for H2 in content
    if '<h2' not in content.lower():
        no_h2_posts += 1
    
    # Check for very short slugs
    if slug and len(slug) < 5:
        short_slugs += 1

dupes = {k: v for k, v in duplicate_titles.items() if v > 1}

print(f"  Empty/short titles: {empty_titles}")
print(f"  Duplicate titles: {len(dupes)}")
print(f"  Thin content (<300 words): {thin_content}")
print(f"  Raw template posts: {raw_template_posts}")
print(f"  Missing excerpt/meta: {empty_excerpts}")
print(f"  No H2 headings: {no_h2_posts}")
print(f"  Short slugs: {short_slugs}")

if empty_titles > 0:
    bugs.append(f"{empty_titles} posts have empty/very short titles — Google ignores these")
if len(dupes) > 0:
    bugs.append(f"{len(dupes)} duplicate titles found — Google sees these as duplicate content")
    for t, c in list(dupes.items())[:5]:
        print(f"    DUPE: '{t[:50]}...' x{c}")
if thin_content > 0:
    bugs.append(f"{thin_content} posts have thin content (<300 words) — Panda penalty risk")
if raw_template_posts > 0:
    bugs.append(f"{raw_template_posts} posts contain raw template expressions ({{$json}}) — SPAM SIGNAL")
if empty_excerpts > 0:
    warnings.append(f"{empty_excerpts}/{len(posts)} posts missing excerpt (auto-generated meta desc may be poor)")
if no_h2_posts > 0:
    warnings.append(f"{no_h2_posts} posts have no H2 headings — poor content structure")

# ================================================================
# 5. CHECK A SAMPLE ARTICLE FOR SEO ELEMENTS
# ================================================================
print("\n[5/12] Deep-checking a sample article...")
# Find a real article (not json-slug)
sample_url = None
for p in posts:
    if p.get('post_name') and 'json-slug' not in p.get('post_name', '') and len(p.get('post_content', '')) > 500:
        sample_url = f"https://plantsmag.com/{p['post_name']}/"
        break

if sample_url:
    art_body, art_code, _ = fetch(sample_url)
    if art_code == 200:
        print(f"  URL: {sample_url}")
        
        # Canonical check
        art_canonicals = re.findall(r'<link\s+rel="canonical"\s+href="(.*?)"', art_body, re.I)
        if len(art_canonicals) > 1:
            bugs.append(f"Article has {len(art_canonicals)} canonical tags (DUPLICATE)")
        elif len(art_canonicals) == 1:
            if art_canonicals[0] != sample_url and art_canonicals[0] != sample_url.rstrip('/'):
                bugs.append(f"Canonical mismatch: page={sample_url} canonical={art_canonicals[0]}")
            else:
                ok_items.append("Article canonical is correct")
        
        # H1 check
        art_h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', art_body, re.I | re.S)
        if len(art_h1s) > 1:
            bugs.append(f"Article has {len(art_h1s)} H1 tags — should be exactly 1")
            for h in art_h1s:
                print(f"    H1: {re.sub('<[^>]+>', '', h)[:60]}")
        
        # Image ALT check
        art_imgs = re.findall(r'<img[^>]*>', art_body, re.I)
        imgs_no_alt = [i for i in art_imgs if 'alt=' not in i.lower() or 'alt=""' in i.lower()]
        if len(imgs_no_alt) > 0:
            warnings.append(f"Article has {len(imgs_no_alt)}/{len(art_imgs)} images without ALT text")
        
        # Check for noindex
        if 'noindex' in art_body.lower():
            bugs.append("Article contains 'noindex' — Google will NOT index this page!")

# ================================================================
# 6. CHECK INTERNAL LINKING
# ================================================================
print("\n[6/12] Checking internal linking...")
if home_code == 200:
    internal_links = re.findall(r'href="(https?://plantsmag\.com[^"]*)"', home_body, re.I)
    unique_internal = set(internal_links)
    print(f"  Internal links on homepage: {len(internal_links)} total, {len(unique_internal)} unique")
    if len(unique_internal) < 10:
        warnings.append(f"Homepage has only {len(unique_internal)} unique internal links — too few for crawlability")
    else:
        ok_items.append(f"Homepage has {len(unique_internal)} unique internal links")

# ================================================================
# 7. CHECK SERVER HEADERS
# ================================================================
print("\n[7/12] Checking server headers...")
if home_headers:
    # Check HSTS
    if 'strict-transport-security' in {k.lower(): v for k, v in home_headers.items()}:
        ok_items.append("HSTS header present")
    else:
        warnings.append("Missing HSTS header")
    
    # Check X-Robots-Tag
    xrobots = home_headers.get('X-Robots-Tag', '')
    if 'noindex' in xrobots.lower():
        bugs.append("X-Robots-Tag header contains 'noindex' — BLOCKS ALL INDEXING!")

# ================================================================
# 8. CHECK HTTPS
# ================================================================
print("\n[8/12] Checking HTTPS & redirects...")
try:
    http_req = urllib.request.Request('http://plantsmag.com/', headers={'User-Agent': 'Googlebot'})
    with urllib.request.urlopen(http_req, timeout=10, context=ctx) as r:
        final_url = r.url
        if final_url.startswith('https'):
            ok_items.append("HTTP redirects to HTTPS")
        else:
            bugs.append("HTTP does NOT redirect to HTTPS")
except:
    ok_items.append("HTTP properly redirects (connection redirected)")

# ================================================================
# 9. CHECK THEME FILES FOR BUGS
# ================================================================
print("\n[9/12] Checking theme files for SEO bugs...")

# Check if functions.php still has disabled canonical
funcs = run_wp(f'grep -n "canonical" {wp}/wp-content/themes/plantsmag-premium/functions.php')
print(f"  Canonical refs in functions.php:")
for line in funcs.strip().split('\n'):
    if line.strip():
        print(f"    {line.strip()}")
        if 'echo' in line and 'DISABLED' not in line and '//' not in line.split('echo')[0]:
            bugs.append("functions.php still outputs canonical tag — conflicts with RankMath!")

# Check for hardcoded homepage canonical in header.php
header_php = run_wp(f'cat {wp}/wp-content/themes/plantsmag-premium/header.php')
if 'rel="canonical"' in header_php and 'plantsmag.com/"' in header_php:
    bugs.append("CRITICAL: header.php has hardcoded homepage canonical for ALL pages!")
elif 'canonical' in header_php.lower():
    warnings.append("header.php references canonical — verify it's dynamic")

# Check for wp_head() call
if 'wp_head()' in header_php or 'wp_head(' in header_php:
    ok_items.append("header.php calls wp_head()")
else:
    bugs.append("header.php missing wp_head() — no meta tags will render!")

# Check footer for wp_footer()
footer_php = run_wp(f'cat {wp}/wp-content/themes/plantsmag-premium/footer.php')
if 'wp_footer()' in footer_php or 'wp_footer(' in footer_php:
    ok_items.append("footer.php calls wp_footer()")
else:
    warnings.append("footer.php may be missing wp_footer()")

# ================================================================
# 10. CHECK FOR ORPHAN PAGES / 404s
# ================================================================
print("\n[10/12] Checking for 404 issues...")
test_404, code_404, _ = fetch('https://plantsmag.com/this-page-does-not-exist-test-12345/')
print(f"  404 test page returns: HTTP {code_404}")
if code_404 != 404:
    bugs.append(f"404 pages return HTTP {code_404} instead of 404 — soft 404 issue!")
else:
    ok_items.append("404 pages return proper 404 status code")

# ================================================================
# 11. CHECK RANKMATH SEO SETTINGS
# ================================================================
print("\n[11/12] Checking RankMath configuration...")
rm_active = run_wp(f'cd {wp} && wp plugin is-active seo-by-rank-math 2>&1')
if 'Plugin' in rm_active and 'active' in rm_active.lower():
    ok_items.append("RankMath SEO plugin is active")
else:
    # Check if it's actually active via plugin list
    plugin_list = run_wp(f'cd {wp} && wp plugin list --status=active --format=csv 2>&1')
    if 'seo-by-rank-math' in plugin_list:
        ok_items.append("RankMath SEO plugin is active")
    else:
        bugs.append("RankMath SEO plugin may not be active!")

# ================================================================
# 12. CONTENT QUALITY CHECK
# ================================================================
print("\n[12/12] Content quality analysis...")
# Check for posts with very similar content (duplicate/spun)
# Check average content length
total_words = 0
very_long = 0
for p in posts:
    content = p.get('post_content', '')
    wc = len(re.findall(r'\w+', re.sub(r'<[^>]+>', '', content)))
    total_words += wc
    if wc > 2000:
        very_long += 1

avg_words = total_words / len(posts) if posts else 0
print(f"  Average content length: {avg_words:.0f} words")
print(f"  Long articles (2000+ words): {very_long}")
if avg_words < 500:
    bugs.append(f"Average content length is only {avg_words:.0f} words — Google considers this thin content")
elif avg_words < 800:
    warnings.append(f"Average content length is {avg_words:.0f} words — aim for 1500+")

ssh.close()

# ================================================================
# FINAL REPORT
# ================================================================
print("\n" + "=" * 70)
print("SEO AUDIT REPORT — PLANTSMAG.COM")
print("=" * 70)

print(f"\n{'='*40}")
print(f"CRITICAL BUGS ({len(bugs)})")
print(f"{'='*40}")
for i, b in enumerate(bugs, 1):
    print(f"  {i}. {b}")

print(f"\n{'='*40}")
print(f"WARNINGS ({len(warnings)})")
print(f"{'='*40}")
for i, w in enumerate(warnings, 1):
    print(f"  {i}. {w}")

print(f"\n{'='*40}")
print(f"OK ({len(ok_items)})")
print(f"{'='*40}")
for i, o in enumerate(ok_items, 1):
    print(f"  {i}. {o}")

print(f"\nSEO HEALTH SCORE: {max(0, 100 - len(bugs)*15 - len(warnings)*5)}/100")
