"""
Sitemap Unification — Find all sitemaps, pick one, fix everything
"""
import paramiko, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

def run(cmd, timeout=30):
    _, o, e = ssh.exec_command(cmd, timeout=timeout)
    return o.read().decode('utf-8', errors='replace'), e.read().decode('utf-8', errors='replace')

wp = '/home/u284669846/domains/plantsmag.com/public_html'

# ================================================================
# STEP 1: Find ALL sitemap files on server
# ================================================================
print("=" * 60)
print("STEP 1: Finding all sitemap files on server")
print("=" * 60)

out, _ = run(f"find {wp} -maxdepth 2 -name '*sitemap*' -type f 2>/dev/null | head -20")
print(out.strip())

# Check each one
for f in ['sitemap.xml', 'sitemap_index.xml', 'wp-sitemap.xml']:
    out, _ = run(f"wc -l {wp}/{f} 2>/dev/null && head -5 {wp}/{f} 2>/dev/null || echo 'NOT FOUND'")
    print(f"\n{f}:")
    print(f"  {out.strip()[:200]}")

# Check what RankMath generates
out, _ = run(f"cd {wp} && wp option get rank_math_modules 2>&1 | head -5")
print(f"\nRankMath modules: {out.strip()[:200]}")

out, _ = run(f"cd {wp} && wp option get rank_math-options-sitemap 2>&1 | head -10")
print(f"\nRankMath sitemap settings: {out.strip()[:300]}")

# Check current robots.txt
out, _ = run(f"cat {wp}/robots.txt 2>/dev/null || echo 'NOT FOUND'")
print(f"\nCurrent robots.txt:\n{out.strip()}")

# ================================================================
# STEP 2: Check what WordPress native sitemap generates
# ================================================================
print("\n" + "=" * 60)
print("STEP 2: Check WP native sitemap status")
print("=" * 60)

out, _ = run(f"cd {wp} && wp rewrite rules list --format=csv 2>&1 | grep -i sitemap | head -5")
print(f"Sitemap rewrite rules: {out.strip()[:300]}")

# Check if RankMath sitemap module is active
out, _ = run(f'''cd {wp} && wp eval 'echo json_encode(get_option("rank_math_modules"));' 2>&1''')
print(f"RankMath active modules: {out.strip()[:300]}")

# ================================================================
# STEP 3: Count URLs in each sitemap
# ================================================================
print("\n" + "=" * 60)
print("STEP 3: URL counts in each sitemap")
print("=" * 60)

for f in ['sitemap.xml', 'wp-sitemap.xml']:
    out, _ = run(f"grep -c '<loc>' {wp}/{f} 2>/dev/null || echo 0")
    print(f"  {f}: {out.strip()} URLs")

out, _ = run(f"grep -c '<loc>' {wp}/wp-sitemap-posts-post-1.xml 2>/dev/null || echo 0")
print(f"  wp-sitemap-posts-post-1.xml: {out.strip()} URLs")

# ================================================================
# STEP 4: Generate ONE definitive sitemap.xml with ALL content
# ================================================================
print("\n" + "=" * 60)
print("STEP 4: Generating definitive sitemap.xml")
print("=" * 60)

sitemap_php = r'''<?php
require_once('/home/u284669846/domains/plantsmag.com/public_html/wp-load.php');

$posts = get_posts(array('post_type'=>'post','post_status'=>'publish','posts_per_page'=>-1,'orderby'=>'date','order'=>'DESC'));
$pages = get_posts(array('post_type'=>'page','post_status'=>'publish','posts_per_page'=>-1));
$cats = get_categories(array('hide_empty'=>true));

$xml = '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
$xml .= '<?xml-stylesheet type="text/xsl" href="/sitemap-style.xsl"?>' . "\n";
$xml .= '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"' . "\n";
$xml .= '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";

// Homepage — highest priority
$xml .= "<url>\n";
$xml .= "  <loc>" . home_url('/') . "</loc>\n";
$xml .= "  <lastmod>" . date('Y-m-d') . "</lastmod>\n";
$xml .= "  <changefreq>daily</changefreq>\n";
$xml .= "  <priority>1.0</priority>\n";
$xml .= "</url>\n";

// Pages (tools, about, etc.)
foreach ($pages as $p) {
    $url = get_permalink($p->ID);
    $mod = get_the_modified_date('Y-m-d', $p->ID);
    $xml .= "<url>\n";
    $xml .= "  <loc>{$url}</loc>\n";
    $xml .= "  <lastmod>{$mod}</lastmod>\n";
    $xml .= "  <changefreq>monthly</changefreq>\n";
    $xml .= "  <priority>0.8</priority>\n";
    $xml .= "</url>\n";
}

// Categories
foreach ($cats as $c) {
    $url = get_category_link($c->term_id);
    $xml .= "<url>\n";
    $xml .= "  <loc>{$url}</loc>\n";
    $xml .= "  <lastmod>" . date('Y-m-d') . "</lastmod>\n";
    $xml .= "  <changefreq>weekly</changefreq>\n";
    $xml .= "  <priority>0.7</priority>\n";
    $xml .= "</url>\n";
}

// Posts
foreach ($posts as $p) {
    $url = get_permalink($p->ID);
    $mod = get_the_modified_date('Y-m-d', $p->ID);
    $img_url = get_the_post_thumbnail_url($p->ID, 'full');
    $xml .= "<url>\n";
    $xml .= "  <loc>{$url}</loc>\n";
    $xml .= "  <lastmod>{$mod}</lastmod>\n";
    $xml .= "  <changefreq>weekly</changefreq>\n";
    $xml .= "  <priority>0.6</priority>\n";
    if ($img_url) {
        $title_esc = htmlspecialchars(wp_strip_all_tags($p->post_title), ENT_XML1, 'UTF-8');
        $xml .= "  <image:image>\n";
        $xml .= "    <image:loc>{$img_url}</image:loc>\n";
        $xml .= "    <image:title>{$title_esc}</image:title>\n";
        $xml .= "  </image:image>\n";
    }
    $xml .= "</url>\n";
}

$xml .= "</urlset>\n";
file_put_contents(ABSPATH . 'sitemap.xml', $xml);
echo "posts=" . count($posts) . " pages=" . count($pages) . " cats=" . count($cats) . " total=" . (count($posts) + count($pages) + count($cats) + 1);
?>'''

sftp = ssh.open_sftp()
with sftp.open(wp + '/gen_sitemap.php', 'w') as f:
    f.write(sitemap_php)
sftp.close()

out, _ = run(f'cd {wp} && php gen_sitemap.php 2>&1', timeout=30)
print(f"  Generated: {out.strip()}")
run(f'rm {wp}/gen_sitemap.php')

# Verify
out, _ = run(f"grep -c '<loc>' {wp}/sitemap.xml 2>/dev/null || echo 0")
print(f"  Verified: {out.strip()} <loc> entries in sitemap.xml")

# ================================================================
# STEP 5: Disable WordPress native sitemap
# ================================================================
print("\n" + "=" * 60)
print("STEP 5: Disabling WP native sitemap (wp-sitemap.xml)")
print("=" * 60)

# Check if already disabled in functions.php
out, _ = run(f"grep -c 'wp_sitemaps_enabled' {wp}/wp-content/themes/plantsmag-premium/functions.php 2>/dev/null || echo 0")
already = out.strip()

if already == '0':
    disable_php = r'''<?php
require_once('/home/u284669846/domains/plantsmag.com/public_html/wp-load.php');
// Read current functions.php
$fpath = get_template_directory() . '/functions.php';
$content = file_get_contents($fpath);

// Add filter to disable WP native sitemap BEFORE the closing tag
$hook = "\n\n// Disable WordPress native sitemap (we use custom sitemap.xml)\nadd_filter( 'wp_sitemaps_enabled', '__return_false' );\n";

// Insert before the last line or at end
if (strpos($content, 'wp_sitemaps_enabled') === false) {
    $content .= $hook;
    file_put_contents($fpath, $content);
    echo "Added wp_sitemaps_enabled filter to functions.php";
} else {
    echo "Already disabled";
}
?>'''
    sftp = ssh.open_sftp()
    with sftp.open(wp + '/disable_native.php', 'w') as f:
        f.write(disable_php)
    sftp.close()
    out, _ = run(f'cd {wp} && php disable_native.php 2>&1')
    print(f"  {out.strip()}")
    run(f'rm {wp}/disable_native.php')
else:
    print("  Already disabled")

# ================================================================
# STEP 6: Write definitive robots.txt
# ================================================================
print("\n" + "=" * 60)
print("STEP 6: Writing unified robots.txt")
print("=" * 60)

robots = """User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

# Sitemap (single source of truth)
Sitemap: https://plantsmag.com/sitemap.xml
"""

sftp = ssh.open_sftp()
with sftp.open(wp + '/robots.txt', 'w') as f:
    f.write(robots)
sftp.close()
print("  Written!")
out, _ = run(f"cat {wp}/robots.txt")
print(out.strip())

# ================================================================
# STEP 7: Update functions.php — IndexNow sitemap URL
# ================================================================
print("\n" + "=" * 60)
print("STEP 7: Verifying IndexNow points to sitemap.xml")
print("=" * 60)

out, _ = run(f"grep 'sitemap' {wp}/wp-content/themes/plantsmag-premium/functions.php | tail -5")
print(out.strip())

# ================================================================
# STEP 8: Flush & verify
# ================================================================
print("\n" + "=" * 60)
print("STEP 8: Flush caches & verify")
print("=" * 60)

run(f'cd {wp} && wp cache flush 2>&1')
run(f'cd {wp} && wp litespeed-purge all 2>&1')
print("  Caches flushed")

# Quick HTTP check
import urllib.request, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for url in ['https://plantsmag.com/sitemap.xml', 'https://plantsmag.com/robots.txt']:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            body = r.read().decode('utf-8')[:200]
            print(f"\n  {url}: {r.status} OK")
            print(f"  {body[:150]}...")
    except Exception as e:
        print(f"\n  {url}: ERROR {e}")

ssh.close()
print(f"\n{'=' * 60}")
print("SITEMAP UNIFICATION COMPLETE!")
print(f"{'=' * 60}")
