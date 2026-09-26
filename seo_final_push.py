"""
Final push: Fix last 2 issues
1. Post #1249 broken JSON title
2. 53 posts without internal links
Target: 95+/100
"""
import paramiko, json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

def run(cmd, timeout=60):
    _, o, _ = ssh.exec_command(cmd, timeout=timeout)
    return o.read().decode('utf-8', errors='replace')

wp = '/home/u284669846/domains/plantsmag.com/public_html'

# ================================================================
# FIX 1: Post #1249 broken title
# ================================================================
print("=" * 60)
print("FIX 1: Post #1249 broken JSON title")
print("=" * 60)

fix_1249 = '''<?php
require_once('/home/u284669846/domains/plantsmag.com/public_html/wp-load.php');
global $wpdb;
$title = $wpdb->get_var("SELECT post_title FROM wp_posts WHERE ID = 1249");
echo "Before: " . substr($title, 0, 100) . "\\n";
if (preg_match('/"title"\\s*:\\s*"(.+)/', $title, $m)) {
    $real = rtrim($m[1], '"\\\\  },');
    $real = trim($real);
    $slug = sanitize_title($real);
    $wpdb->update('wp_posts', array('post_title'=>$real, 'post_name'=>$slug), array('ID'=>1249));
    echo "After: $real\\n";
} else {
    echo "Regex failed\\n";
}
?>'''

sftp = ssh.open_sftp()
with sftp.open(wp + '/fix1249.php', 'w') as f:
    f.write(fix_1249)
sftp.close()
out = run(f'cd {wp} && php fix1249.php 2>&1')
print(out.strip())
run(f'rm {wp}/fix1249.php')

# ================================================================
# FIX 2: Internal links for 53 posts
# ================================================================
print("\n" + "=" * 60)
print("FIX 2: Adding internal links to 53 posts")
print("=" * 60)

link_php = r'''<?php
require_once('/home/u284669846/domains/plantsmag.com/public_html/wp-load.php');
global $wpdb;

// Get ALL posts with their URLs
$all_posts = get_posts(array('post_type'=>'post','post_status'=>'publish','posts_per_page'=>-1));

// Build keyword-to-URL map
$link_map = array();
foreach ($all_posts as $p) {
    $title = strtolower(wp_strip_all_tags($p->post_title));
    $url = get_permalink($p->ID);
    // Extract significant words
    $words = preg_split('/[\s:,\-|!?()]+/', $title);
    $stop = array('the','a','an','in','on','for','and','or','of','to','is','are','your','how','why','what','best','top','vs','with','guide','ultimate','complete','tips','review','2026','new');
    $keywords = array();
    foreach ($words as $w) {
        $w = trim($w);
        if (strlen($w) > 3 && !in_array($w, $stop)) {
            $keywords[] = $w;
        }
    }
    // Use 2-word combos as link anchors
    for ($i = 0; $i < count($keywords) - 1; $i++) {
        $combo = $keywords[$i] . ' ' . $keywords[$i+1];
        if (!isset($link_map[$combo])) {
            $link_map[$combo] = array('url' => $url, 'post_id' => $p->ID);
        }
    }
    // Also single important words
    foreach ($keywords as $kw) {
        if (strlen($kw) > 5 && !isset($link_map[$kw])) {
            $link_map[$kw] = array('url' => $url, 'post_id' => $p->ID);
        }
    }
}

// Find posts without internal links
$no_links = array();
foreach ($all_posts as $p) {
    $content = $p->post_content;
    if (stripos($content, 'plantsmag.com') === false && stripos($content, 'href="/') === false) {
        $no_links[] = $p;
    }
}

echo "Posts without internal links: " . count($no_links) . "\n";
echo "Link map entries: " . count($link_map) . "\n\n";

$fixed = 0;
foreach ($no_links as $p) {
    $content = $p->post_content;
    $content_lower = strtolower($content);
    $links_added = 0;
    $used_urls = array();
    
    // Try to find keyword matches in content
    foreach ($link_map as $keyword => $link_data) {
        if ($links_added >= 3) break;
        if ($link_data['post_id'] == $p->ID) continue; // Don't self-link
        if (in_array($link_data['url'], $used_urls)) continue;
        
        $pos = stripos($content, $keyword);
        if ($pos !== false) {
            // Make sure we're not inside an existing tag
            $before = substr($content, max(0, $pos-10), 10);
            if (strpos($before, '<a') !== false || strpos($before, 'href') !== false) continue;
            
            $original = substr($content, $pos, strlen($keyword));
            $link_html = '<a href="' . $link_data['url'] . '" title="' . ucwords($keyword) . '">' . $original . '</a>';
            
            // Replace only first occurrence
            $content = substr_replace($content, $link_html, $pos, strlen($keyword));
            $used_urls[] = $link_data['url'];
            $links_added++;
        }
    }
    
    if ($links_added > 0) {
        $wpdb->update($wpdb->posts, array('post_content' => $content), array('ID' => $p->ID));
        $fixed++;
        if ($fixed <= 10) {
            echo "  #{$p->ID}: +{$links_added} links | " . mb_substr($p->post_title, 0, 50) . "\n";
        }
    }
}

echo "\nTotal: $fixed posts got internal links\n";
wp_cache_flush();
?>'''

sftp = ssh.open_sftp()
with sftp.open(wp + '/fix_links.php', 'w') as f:
    f.write(link_php)
sftp.close()
out = run(f'cd {wp} && php fix_links.php 2>&1', timeout=120)
print(out.strip())
run(f'rm {wp}/fix_links.php')

# Flush caches
run(f'cd {wp} && wp litespeed-purge all 2>&1')

# ================================================================
# VERIFY
# ================================================================
print("\n" + "=" * 60)
print("VERIFICATION")
print("=" * 60)

# Check title
t = run(f'cd {wp} && wp post get 1249 --field=post_title 2>&1').strip()
print(f"  Post #1249 title: [{('OK' if not t.startswith('{') else 'BROKEN')}] {t[:60]}")

# Count remaining no-link posts
verify_php = '''<?php
require_once('/home/u284669846/domains/plantsmag.com/public_html/wp-load.php');
$posts = get_posts(array('post_type'=>'post','post_status'=>'publish','posts_per_page'=>-1));
$no_links = 0;
foreach ($posts as $p) {
    $c = $p->post_content;
    if (stripos($c, 'plantsmag.com') === false && stripos($c, 'href="/') === false) {
        $no_links++;
    }
}
echo "no_links=$no_links total=" . count($posts);
?>'''
sftp = ssh.open_sftp()
with sftp.open(wp + '/verify.php', 'w') as f:
    f.write(verify_php)
sftp.close()
out = run(f'cd {wp} && php verify.php 2>&1')
print(f"  {out.strip()}")
run(f'rm {wp}/verify.php')

ssh.close()
print("\nDone!")
