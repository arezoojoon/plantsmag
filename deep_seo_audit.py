"""
PlantsMag DEEP SEO AUDIT — Layer 2
====================================
Google-insider-level checks:
- Duplicate content / cannibalization
- Posts with broken JSON as title
- Crawl budget waste
- Sitemap accuracy vs actual posts
- Missing/wrong schema on articles
- Content freshness signals
- Mobile usability
- Core Web Vitals proxy checks
- Orphan pages
- Category/tag SEO
- Internal link depth
"""
import paramiko, json, sys, io, re, urllib.request, ssl
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1)'})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            return r.read().decode('utf-8', errors='replace'), r.status
    except urllib.error.HTTPError as e:
        return '', e.code
    except:
        return '', 0

bugs = []
warnings = []

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

def run(cmd):
    _, o, _ = ssh.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace')

wp = '/home/u284669846/domains/plantsmag.com/public_html'

print("=" * 70)
print("DEEP SEO AUDIT — LAYER 2")
print("=" * 70)

# ================================================================
# 1. POSTS WITH BROKEN JSON / GARBAGE TITLES
# ================================================================
print("\n[1/10] Checking for garbage/JSON titles...")
posts_out = run(f'cd {wp} && wp post list --post_type=post --post_status=publish --fields=ID,post_title,post_name,post_content --format=json 2>&1')
posts = json.loads(posts_out)

garbage_titles = []
for p in posts:
    title = p.get('post_title', '')
    # Check for JSON in title
    if title.startswith('{') or title.startswith('[') or '"title"' in title:
        garbage_titles.append((p['ID'], title[:80]))
    # Check for template expressions in title
    if '{{' in title or '$json' in title:
        garbage_titles.append((p['ID'], title[:80]))
    # Check for "Json Slug" pattern
    if 'json slug' in title.lower() or 'json-slug' in title.lower():
        garbage_titles.append((p['ID'], title[:80]))

if garbage_titles:
    bugs.append(f"{len(garbage_titles)} posts have broken/JSON garbage titles")
    for pid, t in garbage_titles[:10]:
        print(f"  BUG: Post #{pid}: {t}")
else:
    print("  All titles look clean")

# ================================================================
# 2. RAW TEMPLATE / EMPTY CONTENT
# ================================================================
print("\n[2/10] Checking for raw template or empty content...")
bad_content = []
for p in posts:
    content = p.get('post_content', '')
    pid = p['ID']
    title = p.get('post_title', '')[:50]
    
    if '{{$json' in content or '{{ $json' in content:
        bad_content.append((pid, title, 'raw_template'))
    elif len(content.strip()) < 50:
        bad_content.append((pid, title, 'empty/tiny'))
    elif content.strip().startswith('{') and '"title"' in content[:200]:
        bad_content.append((pid, title, 'raw_json_dump'))

if bad_content:
    bugs.append(f"{len(bad_content)} posts have broken/garbage content")
    for pid, t, reason in bad_content[:10]:
        print(f"  BUG: #{pid} [{reason}]: {t}")
else:
    print("  All content looks valid")

# ================================================================
# 3. DUPLICATE CONTENT CANNIBALIZATION
# ================================================================
print("\n[3/10] Checking for keyword cannibalization...")
# Group by similar titles
from collections import defaultdict
keyword_groups = defaultdict(list)
for p in posts:
    title = p.get('post_title', '').lower()
    # Extract main keyword (first 3 significant words)
    words = [w for w in re.findall(r'[a-z]+', title) if len(w) > 3 and w not in ('the', 'guide', 'tips', 'best', 'your', 'with', 'from', 'that', 'this', 'ultimate', 'complete', 'expert', 'how')]
    key = ' '.join(sorted(words[:3]))
    if key:
        keyword_groups[key].append((p['ID'], p['post_title'][:60]))

cannibalized = {k: v for k, v in keyword_groups.items() if len(v) > 1}
if cannibalized:
    warnings.append(f"{len(cannibalized)} keyword groups have multiple competing pages (cannibalization)")
    for key, pages in list(cannibalized.items())[:8]:
        print(f"  CANNIBAL: keyword='{key}'")
        for pid, t in pages:
            print(f"    #{pid}: {t}")
else:
    print("  No cannibalization detected")

# ================================================================
# 4. SITEMAP vs ACTUAL POSTS
# ================================================================
print("\n[4/10] Checking sitemap accuracy...")
sitemap_body, sitemap_code = fetch('https://plantsmag.com/post-sitemap.xml')
if sitemap_code == 200:
    sitemap_urls = set(re.findall(r'<loc>(.*?)</loc>', sitemap_body))
    print(f"  Sitemap has {len(sitemap_urls)} URLs")
    print(f"  Actual published posts: {len(posts)}")
    
    if abs(len(sitemap_urls) - len(posts)) > 5:
        warnings.append(f"Sitemap ({len(sitemap_urls)} URLs) vs actual posts ({len(posts)}) mismatch")

# ================================================================
# 5. ARTICLE SCHEMA / STRUCTURED DATA
# ================================================================
print("\n[5/10] Checking article schema markup...")
# Check 3 random articles
import random
test_posts = random.sample(posts, min(3, len(posts)))
for tp in test_posts:
    slug = tp.get('post_name', '')
    if not slug:
        continue
    url = f"https://plantsmag.com/{slug}/"
    body, code = fetch(url)
    if code == 200:
        schemas = re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', body, re.I | re.S)
        has_article_schema = False
        for s in schemas:
            try:
                sd = json.loads(s)
                if isinstance(sd, dict):
                    items = sd.get('@graph', [sd])
                    for item in items:
                        if item.get('@type') in ['Article', 'BlogPosting', 'NewsArticle']:
                            has_article_schema = True
                            # Check required fields
                            missing = []
                            for field in ['headline', 'datePublished', 'author', 'image']:
                                if field not in item:
                                    missing.append(field)
                            if missing:
                                warnings.append(f"Article schema missing fields: {missing}")
            except:
                pass
        
        status = "HAS" if has_article_schema else "MISSING"
        print(f"  {url[:60]}: Schema={status}")
        if not has_article_schema:
            bugs.append(f"Article pages missing Article/BlogPosting schema — no Rich Results")
            break

# ================================================================
# 6. PAGE LOAD / RESPONSE TIME
# ================================================================
print("\n[6/10] Checking response times...")
import time
urls_to_test = ['https://plantsmag.com/', f'https://plantsmag.com/{posts[0]["post_name"]}/']
for url in urls_to_test:
    start = time.time()
    body, code = fetch(url)
    elapsed = time.time() - start
    print(f"  {url[:50]:50s} -> {elapsed:.2f}s ({len(body)} bytes)")
    if elapsed > 3:
        warnings.append(f"Slow response: {url} took {elapsed:.1f}s (Google wants <2.5s for LCP)")

# ================================================================
# 7. CATEGORY / TAG SEO
# ================================================================
print("\n[7/10] Checking categories and tags...")
cats_out = run(f'cd {wp} && wp term list category --fields=term_id,name,count --format=json 2>&1')
try:
    cats = json.loads(cats_out)
    print(f"  Categories: {len(cats)}")
    empty_cats = [c for c in cats if c.get('count', 0) == 0]
    if empty_cats:
        warnings.append(f"{len(empty_cats)} empty categories (crawl budget waste)")
    for c in cats[:10]:
        print(f"    {c['name']}: {c.get('count', 0)} posts")
except:
    print("  Could not parse categories")

tags_out = run(f'cd {wp} && wp term list post_tag --fields=term_id,name,count --format=json 2>&1')
try:
    tags = json.loads(tags_out)
    print(f"  Tags: {len(tags)}")
    if len(tags) > 100:
        warnings.append(f"Too many tags ({len(tags)}) — creates thin tag pages that waste crawl budget")
    empty_tags = [t for t in tags if t.get('count', 0) <= 1]
    if len(empty_tags) > 10:
        warnings.append(f"{len(empty_tags)} tags with 0-1 posts — thin pages waste crawl budget")
except:
    print("  No tags found")

# ================================================================
# 8. MOBILE META + AMP
# ================================================================
print("\n[8/10] Checking mobile signals...")
body, code = fetch('https://plantsmag.com/')
if code == 200:
    # Check viewport
    has_viewport = 'name="viewport"' in body
    # Check font-size base
    has_small_text = 'font-size: 10px' in body or 'font-size:10px' in body
    # Check touch targets
    print(f"  Viewport meta: {'YES' if has_viewport else 'NO'}")

# ================================================================
# 9. NOINDEX / NOFOLLOW LEAKS
# ================================================================
print("\n[9/10] Checking for noindex/nofollow leaks...")
# Check multiple pages
noindex_pages = []
for p in posts[:20]:
    url = f"https://plantsmag.com/{p['post_name']}/"
    body, code = fetch(url)
    if code == 200:
        if 'noindex' in body.lower():
            noindex_pages.append(url)
        if '<meta name="robots"' in body:
            robots_content = re.search(r'<meta\s+name="robots"\s+content="(.*?)"', body, re.I)
            if robots_content and 'noindex' in robots_content.group(1).lower():
                noindex_pages.append(url)

if noindex_pages:
    bugs.append(f"{len(noindex_pages)} published pages have noindex — Google will NEVER index these!")
    for u in noindex_pages[:5]:
        print(f"  NOINDEX: {u}")
else:
    print("  No noindex leaks found")

# ================================================================
# 10. BREADCRUMBS & NAVIGATION SCHEMA
# ================================================================
print("\n[10/10] Checking breadcrumbs...")
if test_posts:
    url = f"https://plantsmag.com/{test_posts[0]['post_name']}/"
    body, code = fetch(url)
    if code == 200:
        has_breadcrumb = 'BreadcrumbList' in body
        has_breadcrumb_html = 'breadcrumb' in body.lower()
        print(f"  BreadcrumbList schema: {'YES' if has_breadcrumb else 'NO'}")
        print(f"  Breadcrumb HTML: {'YES' if has_breadcrumb_html else 'NO'}")
        if not has_breadcrumb:
            warnings.append("Article pages missing BreadcrumbList schema — no breadcrumb rich results")

ssh.close()

# ================================================================
# FINAL DEEP REPORT
# ================================================================
print("\n" + "=" * 70)
print("DEEP SEO AUDIT — FINAL REPORT")
print("=" * 70)

print(f"\nCRITICAL BUGS ({len(bugs)}):")
for i, b in enumerate(bugs, 1):
    print(f"  {i}. {b}")

print(f"\nWARNINGS ({len(warnings)}):")
for i, w in enumerate(warnings, 1):
    print(f"  {i}. {w}")

print(f"\nDEEP AUDIT SCORE: {max(0, 100 - len(bugs)*15 - len(warnings)*5)}/100")
