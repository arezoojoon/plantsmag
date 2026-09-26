import paramiko, json, sys, io, re, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

def run(cmd):
    _, o, _ = ssh.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace')

wp = '/home/u284669846/domains/plantsmag.com/public_html'

# ================================================================
# FIX 1: JSON Garbage Titles
# ================================================================
print("=" * 60)
print("FIX 1: Cleaning JSON Garbage Titles")
print("=" * 60)

broken_ids = [1185, 1183, 1171, 1165, 1162, 1161, 1160, 1157, 1142, 1135]

ids_str = ",".join(str(x) for x in broken_ids)

# Write PHP file to server using SFTP
php_title_fix = (
    '<?php\n'
    'require_once("/home/u284669846/domains/plantsmag.com/public_html/wp-load.php");\n'
    'global $wpdb;\n'
    '$ids = array(' + ids_str + ');\n'
    'foreach ($ids as $id) {\n'
    '    $title = $wpdb->get_var($wpdb->prepare("SELECT post_title FROM $wpdb->posts WHERE ID = %d", $id));\n'
    '    $decoded = json_decode($title, true);\n'
    '    $real = "";\n'
    '    if ($decoded && isset($decoded["title"])) {\n'
    '        $real = $decoded["title"];\n'
    '    } elseif (preg_match(\'/"title"\\s*:\\s*"([^"]+)"/\', $title, $m)) {\n'
    '        $real = $m[1];\n'
    '    }\n'
    '    if ($real && strlen($real) > 5) {\n'
    '        $slug = sanitize_title($real);\n'
    '        $wpdb->update($wpdb->posts, array("post_title" => $real, "post_name" => $slug), array("ID" => $id));\n'
    '        echo "FIXED #$id: $real\\n";\n'
    '    } else {\n'
    '        echo "SKIP #$id: " . substr($title, 0, 150) . "\\n";\n'
    '    }\n'
    '}\n'
    'wp_cache_flush();\n'
    'echo "\\nDone. Cache flushed.\\n";\n'
    '?>\n'
)

sftp = ssh.open_sftp()
with sftp.open(wp + '/fix_t.php', 'w') as f:
    f.write(php_title_fix)
sftp.close()

out = run('cd ' + wp + ' && php fix_t.php 2>&1')
print(out)
run('rm ' + wp + '/fix_t.php')

# ================================================================
# FIX 2: Static Sitemap
# ================================================================
print("\n" + "=" * 60)
print("FIX 2: Creating Static Sitemap")
print("=" * 60)

# Check htaccess first
htaccess = run('cat ' + wp + '/.htaccess')
print("Current .htaccess:\n" + htaccess[:500])

# Generate static sitemap via PHP
php_sitemap = (
    '<?php\n'
    'require_once("/home/u284669846/domains/plantsmag.com/public_html/wp-load.php");\n'
    '$posts = get_posts(array("post_type" => "post", "post_status" => "publish", "posts_per_page" => -1));\n'
    '$pages = get_posts(array("post_type" => "page", "post_status" => "publish", "posts_per_page" => -1));\n'
    '$all = array_merge($posts, $pages);\n'
    '$xml = \'<?xml version="1.0" encoding="UTF-8"?>\' . "\\n";\n'
    '$xml .= \'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\' . "\\n";\n'
    '$xml .= \'<url><loc>\' . home_url("/") . \'</loc><changefreq>daily</changefreq><priority>1.0</priority></url>\' . "\\n";\n'
    'foreach ($all as $p) {\n'
    '    $url = get_permalink($p->ID);\n'
    '    $mod = get_the_modified_date("Y-m-d", $p->ID);\n'
    '    $pri = ($p->post_type === "page") ? "0.8" : "0.6";\n'
    '    $xml .= "<url><loc>$url</loc><lastmod>$mod</lastmod><changefreq>weekly</changefreq><priority>$pri</priority></url>\\n";\n'
    '}\n'
    '$xml .= \'</urlset>\';\n'
    'file_put_contents(ABSPATH . "sitemap.xml", $xml);\n'
    'echo "sitemap.xml: " . (count($all) + 1) . " URLs\\n";\n'
    '$idx = \'<?xml version="1.0" encoding="UTF-8"?>\' . "\\n";\n'
    '$idx .= \'<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\' . "\\n";\n'
    '$idx .= \'<sitemap><loc>\' . home_url("/sitemap.xml") . \'</loc></sitemap>\' . "\\n";\n'
    '$idx .= \'</sitemapindex>\';\n'
    'file_put_contents(ABSPATH . "sitemap_index.xml", $idx);\n'
    'echo "sitemap_index.xml created\\n";\n'
    '?>\n'
)

sftp = ssh.open_sftp()
with sftp.open(wp + '/gen_sm.php', 'w') as f:
    f.write(php_sitemap)
sftp.close()

out = run('cd ' + wp + ' && php gen_sm.php 2>&1')
print(out.strip())
run('rm ' + wp + '/gen_sm.php')

# Update robots.txt
robots_content = "User-agent: *\nDisallow: /wp-admin/\nAllow: /wp-admin/admin-ajax.php\nAllow: /\n\nSitemap: https://plantsmag.com/sitemap.xml\nSitemap: https://plantsmag.com/sitemap_index.xml\n"
sftp = ssh.open_sftp()
with sftp.open(wp + '/robots.txt', 'w') as f:
    f.write(robots_content)
sftp.close()
print("robots.txt updated")

# Flush LiteSpeed
out = run('cd ' + wp + ' && wp litespeed-purge all 2>&1')
print("LiteSpeed: " + out.strip())

out = run('cd ' + wp + ' && wp rewrite flush --hard 2>&1')
print("Rewrite: " + out.strip())

# Verify files exist
out = run('ls -la ' + wp + '/sitemap.xml ' + wp + '/sitemap_index.xml 2>&1')
print("Files:\n" + out.strip())

# Verify sitemaps accessible
import urllib.request, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

time.sleep(3)
print("\nVerifying sitemaps...")
for url in ['https://plantsmag.com/sitemap.xml', 'https://plantsmag.com/sitemap_index.xml']:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Googlebot', 'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            body = r.read().decode('utf-8', errors='replace')
            loc_count = body.count('<loc>')
            print(f"  {url}: {r.status} OK - {loc_count} URLs")
    except Exception as e:
        print(f"  {url}: {e}")

# IndexNow
try:
    req = urllib.request.Request('https://api.indexnow.org/indexnow?url=https://plantsmag.com/sitemap.xml&key=plantsmag-indexnow-key-2026')
    with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
        print(f"IndexNow ping: {r.status}")
except Exception as e:
    print(f"IndexNow: {e}")

# ================================================================
# VERIFY: Check remaining broken titles
# ================================================================
print("\n" + "=" * 60)
print("VERIFICATION")
print("=" * 60)

for pid in broken_ids:
    t = run(f'cd {wp} && wp post get {pid} --field=post_title 2>&1').strip()
    ok = not t.startswith('{')
    print(f"  [{'OK' if ok else 'BROKEN'}] #{pid}: {t[:70]}")

post_count = run(f'cd {wp} && wp post list --post_type=post --post_status=publish --format=count 2>&1').strip()
print(f"\nTotal published posts: {post_count}")

ssh.close()
print("\nAll fixes complete!")
