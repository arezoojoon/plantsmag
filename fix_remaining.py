"""
Fix remaining issues:
1. JSON garbage titles (using PHP on server to avoid escaping issues)
2. Sitemap regeneration via RankMath
"""
import paramiko, json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

def run(cmd):
    _, o, e = ssh.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace'), e.read().decode('utf-8', errors='replace')

wp = '/home/u284669846/domains/plantsmag.com/public_html'

# ================================================================
# FIX 1: Clean JSON garbage titles via PHP script on server
# ================================================================
print("=" * 60)
print("FIX 1: Cleaning JSON Garbage Titles (via PHP)")
print("=" * 60)

php_fix_titles = '''<?php
require_once('/home/u284669846/domains/plantsmag.com/public_html/wp-load.php');

$args = array(
    'post_type' => 'post',
    'post_status' => 'publish',
    'posts_per_page' => -1,
);
$posts = get_posts($args);
$fixed = 0;

foreach ($posts as $post) {
    $title = $post->post_title;
    
    // Check if title starts with { and contains "title"
    if (preg_match('/^\\s*\\{/', $title) && strpos($title, '"title"') !== false) {
        // Try to extract real title from JSON
        $decoded = json_decode($title, true);
        if ($decoded && isset($decoded['title'])) {
            $real_title = $decoded['title'];
        } else {
            // Regex fallback
            if (preg_match('/"title"\\s*:\\s*"([^"]+)"/', $title, $matches)) {
                $real_title = $matches[1];
            } else {
                continue;
            }
        }
        
        if (strlen($real_title) > 5) {
            wp_update_post(array(
                'ID' => $post->ID,
                'post_title' => $real_title,
            ));
            
            // Also fix the slug if needed
            $new_slug = sanitize_title($real_title);
            wp_update_post(array(
                'ID' => $post->ID,
                'post_name' => $new_slug,
            ));
            
            echo "FIXED #{$post->ID}: {$real_title}\\n";
            $fixed++;
        }
    }
}

echo "\\nTotal fixed: $fixed titles\\n";
?>'''

sftp = ssh.open_sftp()
with sftp.open(f'{wp}/fix_titles.php', 'w') as f:
    f.write(php_fix_titles)
sftp.close()

out, err = run(f'cd {wp} && php fix_titles.php 2>&1')
print(out.strip())
if 'Error' in out or 'error' in out.lower():
    print(f"  Errors: {err.strip()[:200]}")

run(f'rm {wp}/fix_titles.php')

# ================================================================
# FIX 2: Force RankMath sitemap regeneration
# ================================================================
print("\n" + "=" * 60)
print("FIX 2: Forcing Sitemap Regeneration")
print("=" * 60)

php_fix_sitemap = '''<?php
require_once('/home/u284669846/domains/plantsmag.com/public_html/wp-load.php');

global $wpdb;

// Delete ALL sitemap-related options and transients
$deleted = $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '%sitemap%'");
echo "Deleted $deleted sitemap options\\n";

$deleted2 = $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '%rank_math%sitemap%'");
echo "Deleted $deleted2 RankMath sitemap options\\n";

// Force RankMath to rebuild sitemap
if (class_exists('RankMath\\Sitemap\\Cache')) {
    RankMath\\Sitemap\\Cache::invalidate_storage();
    echo "RankMath sitemap cache invalidated\\n";
}

// Also clear object cache
wp_cache_flush();
echo "Object cache flushed\\n";

// Count published posts
$count = $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type='post' AND post_status='publish'");
echo "Published posts: $count\\n";
?>'''

sftp = ssh.open_sftp()
with sftp.open(f'{wp}/fix_sitemap.php', 'w') as f:
    f.write(php_fix_sitemap)
sftp.close()

out, err = run(f'cd {wp} && php fix_sitemap.php 2>&1')
print(out.strip())

run(f'rm {wp}/fix_sitemap.php')

# Flush LiteSpeed cache too
out, _ = run(f'cd {wp} && wp litespeed-purge all 2>&1')
print(f"LiteSpeed: {out.strip()}")

# Wait and check sitemap
import time, urllib.request, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

time.sleep(5)

# Check the sitemap
try:
    req = urllib.request.Request('https://plantsmag.com/post-sitemap.xml', 
                                 headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
        body = r.read().decode('utf-8', errors='replace')
        urls = re.findall(r'<loc>(.*?)</loc>', body)
        print(f"\nSitemap post count: {len(urls)} URLs")
except Exception as e:
    print(f"Sitemap check failed: {e}")

# Also check if there's a wp-sitemap (WordPress native)
try:
    req2 = urllib.request.Request('https://plantsmag.com/wp-sitemap-posts-post-1.xml',
                                  headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req2, timeout=15, context=ctx) as r:
        body2 = r.read().decode('utf-8', errors='replace')
        urls2 = re.findall(r'<loc>(.*?)</loc>', body2)
        print(f"WP native sitemap page 1: {len(urls2)} URLs")
except Exception as e:
    print(f"WP native sitemap: {e}")

# Check robots.txt sitemap reference
try:
    req3 = urllib.request.Request('https://plantsmag.com/robots.txt')
    with urllib.request.urlopen(req3, timeout=10, context=ctx) as r:
        robots = r.read().decode('utf-8', errors='replace')
        print(f"\nrobots.txt sitemap lines:")
        for line in robots.split('\n'):
            if 'sitemap' in line.lower():
                print(f"  {line.strip()}")
except:
    pass

# ================================================================
# Verify: List remaining titles that are still broken
# ================================================================
print("\n" + "=" * 60)
print("VERIFICATION: Checking for remaining issues")
print("=" * 60)

out, _ = run(f'cd {wp} && wp post list --post_type=post --post_status=publish --fields=ID,post_title --format=json 2>&1')
posts = json.loads(out)

still_broken = []
for p in posts:
    t = p.get('post_title', '')
    if t.strip().startswith('{') and '"title"' in t:
        still_broken.append((p['ID'], t[:60]))

if still_broken:
    print(f"  Still {len(still_broken)} broken titles:")
    for pid, t in still_broken:
        print(f"    #{pid}: {t}")
else:
    print("  All titles are clean!")

print(f"  Total posts: {len(posts)}")

ssh.close()
print("\nDone!")
