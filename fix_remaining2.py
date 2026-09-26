import paramiko, json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

def run(cmd):
    _, o, _ = ssh.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace')

wp = '/home/u284669846/domains/plantsmag.com/public_html'

# ================================================================
# FIX TITLES: Get raw titles from DB, extract real title, update
# ================================================================
print("=" * 60)
print("FIXING JSON GARBAGE TITLES")
print("=" * 60)

# Get exact title content from database
broken_ids = [1185, 1183, 1171, 1165, 1162, 1161, 1160, 1157, 1142, 1135]

for pid in broken_ids:
    # Get raw title from DB
    raw = run(f"cd {wp} && wp post get {pid} --field=post_title 2>&1")
    raw = raw.strip()
    
    print(f"\n  Post #{pid}:")
    print(f"  Raw title (first 100): {raw[:100]}")
    
    # Try to extract title using regex on raw text
    match = re.search(r'"title"\s*:\s*"([^"]+)"', raw)
    if match:
        real_title = match.group(1)
        # Unescape any HTML entities
        real_title = real_title.replace('&amp;', '&').replace('&#8217;', "'").replace('&#8220;', '"').replace('&#8221;', '"')
        print(f"  Extracted: {real_title}")
        
        # Generate clean slug
        clean_slug = re.sub(r'[^a-z0-9]+', '-', real_title.lower()).strip('-')[:60]
        
        # Write PHP file to do the update (avoids shell escaping)
        php_code = f'''<?php
require_once('{wp}/wp-load.php');
wp_update_post(array(
    'ID' => {pid},
    'post_title' => '{real_title.replace("'", "\\'")}',
    'post_name' => '{clean_slug}',
));
echo "Updated #{pid}";
?>'''
        sftp = ssh.open_sftp()
        with sftp.open(f'{wp}/fix_one.php', 'w') as f:
            f.write(php_code)
        sftp.close()
        
        result = run(f'cd {wp} && php fix_one.php 2>&1')
        print(f"  Result: {result.strip()}")
        run(f'rm {wp}/fix_one.php')
    else:
        print(f"  Could not extract title from: {raw[:200]}")

# Verify
print("\n" + "=" * 60)
print("VERIFYING TITLES")
print("=" * 60)

for pid in broken_ids:
    new_title = run(f"cd {wp} && wp post get {pid} --field=post_title 2>&1").strip()
    is_ok = not new_title.startswith('{')
    status = "OK" if is_ok else "STILL BROKEN"
    print(f"  [{status}] #{pid}: {new_title[:70]}")

# ================================================================
# FIX SITEMAP: Check what sitemap plugin/system is actually active
# ================================================================
print("\n" + "=" * 60)
print("FIXING SITEMAP")
print("=" * 60)

# Check RankMath sitemap settings
result = run(f"cd {wp} && wp option get rank_math_modules 2>&1")
print(f"RankMath modules: {result.strip()[:300]}")

# Check if RankMath sitemap module is enabled
result = run(f"""cd {wp} && wp eval 'print_r(get_option("rank_math_modules"));' 2>&1""")
print(f"Modules detail: {result.strip()[:300]}")

# Enable sitemap in RankMath if disabled
sitemap_php = '''<?php
require_once('/home/u284669846/domains/plantsmag.com/public_html/wp-load.php');

// Check RankMath active modules
$modules = get_option('rank_math_modules', array());
echo "Current modules: " . implode(', ', $modules) . "\\n";

// Enable sitemap if not active
if (!in_array('sitemap', $modules)) {
    $modules[] = 'sitemap';
    update_option('rank_math_modules', $modules);
    echo "Sitemap module ENABLED\\n";
} else {
    echo "Sitemap module already active\\n";
}

// Check WP native sitemap status
echo "WP native sitemaps: " . (class_exists('WP_Sitemaps') ? "Available" : "Not Available") . "\\n";

// Flush rewrite rules to regenerate sitemap URLs
flush_rewrite_rules(true);
echo "Rewrite rules flushed\\n";

// Check sitemap URL
$sitemap_url = home_url('/sitemap_index.xml');
echo "Expected sitemap URL: $sitemap_url\\n";

// Also check RankMath sitemap settings
$rm_general = get_option('rank_math-options-general', array());
$rm_sitemap_post = isset($rm_general['pt_post_sitemap']) ? $rm_general['pt_post_sitemap'] : 'not set';
echo "RankMath post sitemap: $rm_sitemap_post\\n";

// Enable post type in RankMath sitemap
$rm_general['pt_post_sitemap'] = 'on';
$rm_general['pt_page_sitemap'] = 'on';
update_option('rank_math-options-general', $rm_general);
echo "Post/Page sitemap enabled in RankMath\\n";

// Force flush
flush_rewrite_rules(true);
echo "Final rewrite flush done\\n";
?>'''

sftp = ssh.open_sftp()
with sftp.open(f'{wp}/fix_sitemap2.php', 'w') as f:
    f.write(sitemap_php)
sftp.close()

result = run(f'cd {wp} && php fix_sitemap2.php 2>&1')
print(result.strip())

run(f'rm {wp}/fix_sitemap2.php')

# Flush LiteSpeed
run(f'cd {wp} && wp litespeed-purge all 2>&1')
run(f'cd {wp} && wp rewrite flush 2>&1')

# Update robots.txt to point to correct sitemap
print("\nChecking robots.txt sitemap reference...")
robots = run(f'cat {wp}/robots.txt 2>&1')
print(f"Current robots.txt:\n{robots}")

# robots.txt points to wp-sitemap.xml (WordPress native)
# but RankMath should create sitemap_index.xml
# Let's check which one actually works
import urllib.request, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

import time
time.sleep(3)

for sitemap_url in ['https://plantsmag.com/sitemap_index.xml', 
                     'https://plantsmag.com/wp-sitemap.xml',
                     'https://plantsmag.com/sitemap.xml',
                     'https://plantsmag.com/post-sitemap.xml']:
    try:
        req = urllib.request.Request(sitemap_url, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            body = r.read().decode('utf-8', errors='replace')
            urls = re.findall(r'<loc>(.*?)</loc>', body)
            print(f"  {sitemap_url}: {r.status} OK — {len(urls)} URLs")
    except Exception as e:
        print(f"  {sitemap_url}: {e}")

ssh.close()
print("\nDone!")
