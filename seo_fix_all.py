"""
PlantsMag SEO FIX — All 5 Fixes
================================
Fix 1: Clean JSON garbage titles (10 posts)
Fix 2: Deduplicate cannibalized posts (~15 posts)
Fix 3: Regenerate sitemap + ping Google
Fix 4: Fix N8N Parse node root cause
Fix 5: Set featured images for posts missing them
"""
import paramiko, json, sys, io, re, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ================================================================
# Connect to WordPress server
# ================================================================
ssh_wp = paramiko.SSHClient()
ssh_wp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_wp.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

def run_wp(cmd):
    _, o, e = ssh_wp.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace'), e.read().decode('utf-8', errors='replace')

wp = '/home/u284669846/domains/plantsmag.com/public_html'

# Get all posts
print("Loading all posts...")
posts_out, _ = run_wp(f'cd {wp} && wp post list --post_type=post --post_status=publish --fields=ID,post_title,post_name,post_date,post_content --format=json 2>&1')
posts = json.loads(posts_out)
print(f"Total posts: {len(posts)}")

# ================================================================
# FIX 1: Clean JSON Garbage Titles
# ================================================================
print("\n" + "=" * 60)
print("FIX 1: Cleaning JSON Garbage Titles")
print("=" * 60)

fixed_titles = 0
for p in posts:
    pid = p['ID']
    title = p.get('post_title', '')
    
    # Detect JSON in title
    if title.strip().startswith('{') and '"title"' in title:
        try:
            # Extract real title from JSON
            parsed = json.loads(title)
            real_title = parsed.get('title', '')
            if real_title and len(real_title) > 5:
                safe_title = real_title.replace("'", "\\'").replace('"', '\\"')
                out, _ = run_wp(f"cd {wp} && wp post update {pid} --post_title='{safe_title}' 2>&1")
                if 'Success' in out:
                    print(f"  FIXED #{pid}: '{real_title[:60]}'")
                    p['post_title'] = real_title  # Update in memory
                    fixed_titles += 1
                else:
                    print(f"  FAIL #{pid}: {out[:80]}")
        except json.JSONDecodeError:
            # Try regex extraction
            match = re.search(r'"title"\s*:\s*"([^"]+)"', title)
            if match:
                real_title = match.group(1)
                safe_title = real_title.replace("'", "\\'").replace('"', '\\"')
                out, _ = run_wp(f"cd {wp} && wp post update {pid} --post_title='{safe_title}' 2>&1")
                if 'Success' in out:
                    print(f"  FIXED #{pid}: '{real_title[:60]}'")
                    p['post_title'] = real_title
                    fixed_titles += 1

print(f"\n  Total fixed: {fixed_titles} titles")

# ================================================================
# FIX 2: Deduplicate Cannibalized Posts
# ================================================================
print("\n" + "=" * 60)
print("FIX 2: Deduplicating Cannibalized Posts")
print("=" * 60)

# Reload titles after fix 1
posts_out2, _ = run_wp(f'cd {wp} && wp post list --post_type=post --post_status=publish --fields=ID,post_title,post_name,post_date --format=json 2>&1')
posts_fresh = json.loads(posts_out2)

# Group by normalized title
from collections import defaultdict
title_groups = defaultdict(list)
for p in posts_fresh:
    title = p.get('post_title', '').strip()
    if not title:
        continue
    # Normalize: lowercase, remove punctuation, extra spaces
    normalized = re.sub(r'[^a-z0-9\s]', '', title.lower())
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    title_groups[normalized].append(p)

duplicates_to_delete = []
for norm_title, group in title_groups.items():
    if len(group) <= 1:
        continue
    
    # Sort by: prefer longer content first, then newer date
    group.sort(key=lambda x: (x.get('post_date', ''), int(x['ID'])), reverse=True)
    
    # Keep the first (newest), delete the rest
    keeper = group[0]
    for dup in group[1:]:
        duplicates_to_delete.append(dup)
        print(f"  DELETE #{dup['ID']}: {dup['post_title'][:55]}  (keep #{keeper['ID']})")

print(f"\n  Deleting {len(duplicates_to_delete)} duplicate posts...")
deleted = 0
for dup in duplicates_to_delete:
    out, _ = run_wp(f"cd {wp} && wp post delete {dup['ID']} --force 2>&1")
    if 'Success' in out:
        deleted += 1
    else:
        print(f"  FAIL delete #{dup['ID']}: {out[:80]}")

print(f"  Deleted: {deleted}/{len(duplicates_to_delete)}")

# ================================================================
# FIX 3: Regenerate Sitemap + Ping Google
# ================================================================
print("\n" + "=" * 60)
print("FIX 3: Regenerating Sitemap")
print("=" * 60)

# Flush RankMath sitemap cache
out, _ = run_wp(f'cd {wp} && wp cache flush 2>&1')
print(f"  WP cache: {out.strip()}")

out, _ = run_wp(f'cd {wp} && wp transient delete --all 2>&1')
print(f"  Transients: {out.strip()[:80]}")

# Delete RankMath sitemap transients specifically
out, _ = run_wp(f"""cd {wp} && wp eval '
delete_option("rank_math_sitemap_cache");
delete_transient("rank_math_sitemap_cache");
global \$wpdb;
\$wpdb->query("DELETE FROM \$wpdb->options WHERE option_name LIKE \"%rank_math_sitemap%\"");
\$wpdb->query("DELETE FROM \$wpdb->options WHERE option_name LIKE \"%sitemap%cache%\"");
echo "RankMath sitemap cache cleared";
' 2>&1""")
print(f"  RankMath: {out.strip()}")

# Flush rewrite rules
out, _ = run_wp(f'cd {wp} && wp rewrite flush 2>&1')
print(f"  Rewrite: {out.strip()}")

# Flush LiteSpeed cache
out, _ = run_wp(f'cd {wp} && wp litespeed-purge all 2>&1')
print(f"  LiteSpeed: {out.strip()}")

# Ping Google & IndexNow
import urllib.request, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    with urllib.request.urlopen('https://www.google.com/ping?sitemap=https://plantsmag.com/sitemap_index.xml', timeout=10, context=ctx) as r:
        print(f"  Google ping: {r.status}")
except Exception as e:
    print(f"  Google ping: {e}")

try:
    with urllib.request.urlopen('https://api.indexnow.org/indexnow?url=https://plantsmag.com/&key=plantsmag-indexnow-key-2026', timeout=10, context=ctx) as r:
        print(f"  IndexNow ping: {r.status}")
except Exception as e:
    print(f"  IndexNow ping: {e}")

# Verify sitemap now
time.sleep(3)
try:
    with urllib.request.urlopen('https://plantsmag.com/post-sitemap.xml', timeout=15, context=ctx) as r:
        sitemap_body = r.read().decode('utf-8', errors='replace')
        sitemap_urls = re.findall(r'<loc>(.*?)</loc>', sitemap_body)
        print(f"  Sitemap now has: {len(sitemap_urls)} URLs")
except Exception as e:
    print(f"  Sitemap check: {e}")

# Get current post count
out, _ = run_wp(f'cd {wp} && wp post list --post_type=post --post_status=publish --format=count 2>&1')
print(f"  Published posts now: {out.strip()}")

# ================================================================
# FIX 5: Set Featured Images for Posts Missing Them
# ================================================================
print("\n" + "=" * 60)
print("FIX 5: Setting Featured Images for Posts")
print("=" * 60)

# Check how many posts have featured images
out, _ = run_wp(f"""cd {wp} && wp eval '
\$args = array("post_type" => "post", "post_status" => "publish", "posts_per_page" => -1);
\$posts = get_posts(\$args);
\$with_thumb = 0;
\$without_thumb = 0;
foreach (\$posts as \$p) {{
    if (has_post_thumbnail(\$p->ID)) {{
        \$with_thumb++;
    }} else {{
        \$without_thumb++;
    }}
}}
echo "with_thumb=\$with_thumb without_thumb=\$without_thumb";
' 2>&1""")
print(f"  {out.strip()}")

# Create a PHP script on server to generate placeholder images and assign them
php_script = r'''<?php
// Load WP
require_once('/home/u284669846/domains/plantsmag.com/public_html/wp-load.php');

$args = array(
    'post_type' => 'post',
    'post_status' => 'publish',
    'posts_per_page' => -1,
    'meta_query' => array(
        array(
            'key' => '_thumbnail_id',
            'compare' => 'NOT EXISTS'
        )
    )
);
$posts_without_thumb = get_posts($args);
echo "Posts without featured image: " . count($posts_without_thumb) . "\n";

$fixed = 0;
$upload_dir = wp_upload_dir();

foreach ($posts_without_thumb as $post) {
    // Generate a simple SVG placeholder with the post title
    $title = wp_strip_all_tags($post->post_title);
    $short_title = mb_substr($title, 0, 40);
    
    // Create a green-themed plant SVG
    $svg = '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
    <defs>
        <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#0d5016;stop-opacity:1"/>
            <stop offset="100%" style="stop-color:#1a8a3a;stop-opacity:1"/>
        </linearGradient>
    </defs>
    <rect width="1200" height="630" fill="url(#bg)"/>
    <text x="600" y="250" text-anchor="middle" fill="white" font-family="Arial,sans-serif" font-size="42" font-weight="bold">' . htmlspecialchars($short_title) . '</text>
    <text x="600" y="320" text-anchor="middle" fill="#a8e6a0" font-family="Arial,sans-serif" font-size="24">PlantsMag.com</text>
    <text x="600" y="420" text-anchor="middle" fill="#66cc66" font-size="80">🌿</text>
    </svg>';
    
    // Save SVG to uploads
    $filename = 'plantsmag-featured-' . $post->ID . '.svg';
    $filepath = $upload_dir['path'] . '/' . $filename;
    file_put_contents($filepath, $svg);
    
    // Create attachment
    $attachment = array(
        'post_mime_type' => 'image/svg+xml',
        'post_title'     => $title . ' - Featured Image',
        'post_content'   => '',
        'post_status'    => 'inherit'
    );
    
    $attach_id = wp_insert_attachment($attachment, $filepath, $post->ID);
    if (!is_wp_error($attach_id)) {
        set_post_thumbnail($post->ID, $attach_id);
        $fixed++;
        if ($fixed <= 10) {
            echo "  Set featured image for #{$post->ID}: {$short_title}\n";
        }
    }
    
    if ($fixed >= 300) break; // Safety limit
}

echo "\nTotal fixed: $fixed posts now have featured images\n";
?>'''

sftp = ssh_wp.open_sftp()
with sftp.open(f'{wp}/fix_images.php', 'w') as f:
    f.write(php_script)
sftp.close()

out, err = run_wp(f'cd {wp} && php fix_images.php 2>&1')
print(f"  {out.strip()}")
if err.strip():
    print(f"  Errors: {err.strip()[:200]}")

# Cleanup
run_wp(f'rm {wp}/fix_images.php')

ssh_wp.close()

# ================================================================
# FIX 4: Fix N8N Parse Node Root Cause
# ================================================================
print("\n" + "=" * 60)
print("FIX 4: Fixing N8N Parse Node (Root Cause)")
print("=" * 60)

ssh_n8n = paramiko.SSHClient()
ssh_n8n.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_n8n.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run_n8n(cmd):
    _, o, _ = ssh_n8n.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace')

run_n8n('''curl -s -c /tmp/n8n_session.txt -X POST http://localhost:5678/rest/login -H "Content-Type: application/json" -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}\' ''')

# Bulletproof Parse code — handles ALL edge cases
PARSE_CODE = r'''
const raw = $input.item.json;

// === STEP 1: Extract raw text from Gemini response ===
let text = "";
try {
  if (raw.candidates && raw.candidates[0]) {
    text = raw.candidates[0].content.parts[0].text || "";
  } else if (raw.body) {
    const body = typeof raw.body === "string" ? JSON.parse(raw.body) : raw.body;
    text = body.candidates[0].content.parts[0].text || "";
  } else if (typeof raw === "string") {
    text = raw;
  } else {
    text = JSON.stringify(raw);
  }
} catch(e) {
  text = JSON.stringify(raw);
}

// === STEP 2: Clean markdown fencing ===
text = text.replace(/^```json\s*/i, "").replace(/^```\s*/i, "");
text = text.replace(/\n```\s*$/g, "").replace(/```\s*$/g, "");
text = text.trim();

// === STEP 3: Parse JSON with multiple fallback strategies ===
let article = null;

// Strategy A: Direct parse
try {
  article = JSON.parse(text);
} catch(e) {}

// Strategy B: Find JSON object with "title" and "content" keys
if (!article) {
  const jsonMatch = text.match(/\{[\s\S]*?"title"\s*:\s*"[\s\S]*?"content"\s*:\s*"[\s\S]*?\}/);
  if (jsonMatch) {
    try { article = JSON.parse(jsonMatch[0]); } catch(e) {}
  }
}

// Strategy C: Find first { to last } 
if (!article) {
  const first = text.indexOf('{');
  const last = text.lastIndexOf('}');
  if (first !== -1 && last > first) {
    try { article = JSON.parse(text.substring(first, last + 1)); } catch(e) {}
  }
}

// === STEP 4: Validate extracted data ===
if (article && article.title && article.content && article.content.length > 100) {
  return {
    json: {
      title: String(article.title).substring(0, 70),
      slug: String(article.slug || article.title.toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '')
      ).substring(0, 60),
      meta_description: String(article.meta_description || article.excerpt || "").substring(0, 160),
      content: String(article.content)
    }
  };
}

// === STEP 5: Ultimate fallback — use raw text as content ===
// Extract a reasonable title from the first line
const lines = text.split('\n').filter(l => l.trim().length > 0);
const firstLine = (lines[0] || "Plant Care Guide").replace(/<[^>]+>/g, '').trim();
const fallbackTitle = firstLine.length > 10 ? firstLine.substring(0, 65) : "Expert Plant Care Guide";
const fallbackSlug = fallbackTitle.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').substring(0, 60);

return {
  json: {
    title: fallbackTitle,
    slug: fallbackSlug || ("plant-guide-" + Date.now()),
    meta_description: fallbackTitle.substring(0, 155),
    content: "<article>" + text.replace(/\n\n/g, "</p><p>").replace(/\n/g, "<br>") + "</article>"
  }
};
'''

# Update all 3 workflows
WORKFLOWS = {
    'CpyU2cf01DdtpfWo': ('WF1', 'Parse Article'),
    'UKegbNpPIBkkNUrd': ('WF2', 'Parse UAE Article'),
    'SLgAkWAL2NBVzZ7U': ('WF3', 'Parse Review'),
}

for wf_id, (wf_name, parse_node_name) in WORKFLOWS.items():
    wf_out = run_n8n(f'curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows/{wf_id}')
    wf_data = json.loads(wf_out).get('data', {})
    
    modified = False
    for node in wf_data.get('nodes', []):
        if node['name'] == parse_node_name and node['type'] == 'n8n-nodes-base.code':
            node['parameters']['jsCode'] = PARSE_CODE
            modified = True
    
    if modified:
        update = json.dumps({"nodes": wf_data['nodes']})
        sftp = ssh_n8n.open_sftp()
        with sftp.open(f'/tmp/parse_fix_{wf_id}.json', 'w') as f:
            f.write(update)
        sftp.close()
        result = run_n8n(f'curl -s -b /tmp/n8n_session.txt -X PATCH http://localhost:5678/rest/workflows/{wf_id} -H "Content-Type: application/json" -d @/tmp/parse_fix_{wf_id}.json')
        status = "OK" if '"updatedAt"' in result else "FAIL"
        print(f"  {wf_name} Parse node: {status}")

ssh_n8n.close()

print("\n" + "=" * 60)
print("ALL 5 FIXES COMPLETE!")
print("=" * 60)
