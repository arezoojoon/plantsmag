<?php
/**
 * PlantsMag SEO Title & Description Optimizer
 * =============================================
 * مشکل Search Console:
 *   - CTR = 0% برای همه queries
 *   - Position 8.5 ولی کلیک نداره
 *
 * راه‌حل:
 *   1. Title Tags → Power words + numbers + emotional triggers
 *   2. Meta Descriptions → excerpt به یک hook جذاب تبدیل میشه
 *   3. FAQ Schema → Rich Snippets → CTR بالاتر
 *
 * Usage: php seo_title_optimizer.php [--dry-run] [--limit=50]
 */

define('SEO_OPT_VERSION', '1.0');
define('SEO_OPT_START', microtime(true));

if (!defined('ABSPATH')) {
    require_once(dirname(__FILE__) . '/wp-load.php');
}

// ── Config ───────────────────────────────────────────────────────────────────
header('Content-Type: text/plain; charset=UTF-8');
$DRY_RUN = isset($_GET['dry']) || in_array('--dry-run', $argv ?? []);
$LIMIT   = isset($_GET['limit']) ? (int)$_GET['limit'] : 100;
$FORCE   = isset($_GET['force']); // re-optimize already-optimized posts

function log_msg($msg, $type = 'INFO') {
    $ts = date('H:i:s');
    echo "[{$ts}] [{$type}] {$msg}\n";
    flush();
}
function hr() { echo str_repeat('─', 60) . "\n"; }

hr();
echo "  🌿 PlantsMag SEO Optimizer v" . SEO_OPT_VERSION . "\n";
echo "  Mode: " . ($DRY_RUN ? '🔍 DRY RUN (no changes)' : '✏️ LIVE') . "\n";
echo "  Limit: {$LIMIT} posts\n";
hr();

// ── Power Word Patterns ───────────────────────────────────────────────────────
/**
 * How titles get enhanced:
 * - Add "The #1 Guide" prefix for how-to titles
 * - Add number prefixes for list-type content
 * - Add emotional triggers: "Without Killing It", "That Actually Works"
 * - Ensure title is 50-60 chars for Google display
 */
function plantsmag_enhance_title($title) {
    $original = $title;
    
    // Already enhanced (has our power words)
    $already_enhanced = [
        'Without Killing', 'That Actually Works', 'The #1', 'Step-by-Step',
        'Proven Method', 'Expert Guide', 'Mistake', 'Secret', 'Trick',
        '#1 Reason', 'Warning', 'Must-Know', 'vs.', 'Pro Tip'
    ];
    foreach ($already_enhanced as $marker) {
        if (stripos($title, $marker) !== false) {
            return $title; // already optimized
        }
    }
    
    $len = strlen($title);
    
    // Pattern 1: "How to X" → "How to X: The Step-by-Step Method That Works"
    if (preg_match('/^how to /i', $title)) {
        if ($len < 42) {
            $title = $title . ': The Step-by-Step Guide';
        }
        return $title;
    }
    
    // Pattern 2: "X vs Y" → keep + add insight
    if (stripos($title, ' vs ') !== false || stripos($title, ' vs. ') !== false) {
        if ($len < 45) {
            $title .= ' (Which Actually Works?)';
        }
        return $title;
    }
    
    // Pattern 3: Titles about problems/fixes
    $problem_words = ['rot', 'dying', 'wilting', 'yellowing', 'yellow', 'brown', 'spots', 'drooping', 'root rot', 'overwatered', 'pest', 'mites', 'bugs', 'killing', 'dead'];
    foreach ($problem_words as $word) {
        if (stripos($title, $word) !== false) {
            if ($len < 45) {
                $title .= ': Fix It Fast';
            }
            return $title;
        }
    }
    
    // Pattern 4: Technique/hack titles
    $technique_words = ['trick', 'hack', 'method', 'technique', 'secret', 'tip', 'way', 'culture', 'debate'];
    foreach ($technique_words as $word) {
        if (stripos($title, $word) !== false) {
            if ($len < 45) {
                $title .= ' (Expert Breakdown)';
            }
            return $title;
        }
    }
    
    // Pattern 5: Plant-specific care titles
    $care_words = ['care', 'growing', 'propagat', 'repot', 'water', 'prune', 'fertiliz', 'soil', 'light', 'humidity', 'temperature'];
    foreach ($care_words as $word) {
        if (stripos($title, $word) !== false) {
            if ($len < 48) {
                $title .= ': What Nobody Tells You';
            }
            return $title;
        }
    }
    
    // Pattern 6: General enhancement - add curiosity gap
    if ($len < 45) {
        $suffixes = [
            ': The Complete Guide',
            ': Proven Methods',
            ': Expert Tips',
            ': What You Need to Know',
        ];
        // Pick based on title hash for consistency
        $suffix = $suffixes[crc32($title) % count($suffixes)];
        $title .= $suffix;
    }
    
    return $title;
}

/**
 * Generate a compelling meta description (155 chars max)
 * Format: [Hook sentence] + [Action/Benefit] + [CTA]
 */
function plantsmag_generate_meta_description($post) {
    // Use existing excerpt if already good quality (>80 chars)
    $existing = trim($post->post_excerpt);
    if (!empty($existing) && strlen($existing) > 80) {
        return substr(wp_strip_all_tags($existing), 0, 155);
    }
    
    // Extract first 2 meaningful sentences from content
    $content = strip_tags(strip_shortcodes($post->post_content));
    $content = preg_replace('/\s+/', ' ', $content);
    $content = trim($content);
    
    // Get first sentence
    $sentences = preg_split('/(?<=[.!?])\s+/', $content, 5);
    
    $desc = '';
    foreach ($sentences as $sentence) {
        $sentence = trim($sentence);
        if (strlen($sentence) > 30) { // meaningful sentence
            $desc .= $sentence . ' ';
            if (strlen($desc) > 100) break;
        }
    }
    
    $desc = trim($desc);
    
    // Truncate to 155 chars at word boundary
    if (strlen($desc) > 155) {
        $desc = substr($desc, 0, 152) . '...';
        $last_space = strrpos($desc, ' ');
        if ($last_space > 100) {
            $desc = substr($desc, 0, $last_space) . '...';
        }
    }
    
    return $desc;
}

// ── Main Processing ───────────────────────────────────────────────────────────
log_msg("Fetching posts...");

global $wpdb;

$posts = get_posts([
    'post_type'      => 'post',
    'post_status'    => 'publish',
    'posts_per_page' => $LIMIT,
    'orderby'        => 'date',
    'order'          => 'DESC',
    'meta_query'     => $FORCE ? [] : [
        [
            'key'     => '_seo_opt_done',
            'compare' => 'NOT EXISTS',
        ]
    ],
]);

log_msg("Found " . count($posts) . " posts to optimize");
hr();

$optimized  = 0;
$skipped    = 0;
$title_changes = 0;
$desc_changes  = 0;

foreach ($posts as $post) {
    $old_title = $post->post_title;
    $new_title = plantsmag_enhance_title($old_title);
    $new_desc  = plantsmag_generate_meta_description($post);
    
    $title_changed = ($new_title !== $old_title);
    $desc_changed  = (!empty($new_desc) && $new_desc !== trim($post->post_excerpt));
    
    if (!$title_changed && !$desc_changed) {
        $skipped++;
        continue;
    }
    
    log_msg("Post #{$post->ID}: " . substr($old_title, 0, 50));
    if ($title_changed) {
        log_msg("  Title: " . substr($new_title, 0, 60), 'TITLE');
        $title_changes++;
    }
    if ($desc_changed) {
        log_msg("  Desc : " . substr($new_desc, 0, 80) . "...", 'DESC');
        $desc_changes++;
    }
    
    if (!$DRY_RUN) {
        // Update post title
        if ($title_changed) {
            $wpdb->update(
                $wpdb->posts,
                ['post_title' => $new_title],
                ['ID' => $post->ID],
                ['%s'],
                ['%d']
            );
        }
        
        // Update excerpt (used as meta description)
        if ($desc_changed) {
            $wpdb->update(
                $wpdb->posts,
                ['post_excerpt' => $new_desc],
                ['ID' => $post->ID],
                ['%s'],
                ['%d']
            );
        }
        
        // Mark as optimized
        update_post_meta($post->ID, '_seo_opt_done', '1');
        update_post_meta($post->ID, '_seo_opt_date', current_time('mysql'));
        
        // Clear cache
        clean_post_cache($post->ID);
    }
    
    $optimized++;
}

// ── FAQ Schema Injection into functions.php ──────────────────────────────────
// This is done via a separate hook, not in this script.
// The FAQ schema is generated dynamically per post in functions.php

// ── Summary ───────────────────────────────────────────────────────────────────
hr();
$elapsed = round(microtime(true) - SEO_OPT_START, 2);
echo "\n";
echo "  📊 SUMMARY\n";
echo "  ─────────────────────────────────────────────────\n";
echo "  Posts processed : {$optimized}\n";
echo "  Posts skipped   : {$skipped} (already optimized)\n";
echo "  Title changes   : {$title_changes}\n";
echo "  Description upd : {$desc_changes}\n";
echo "  Execution time  : {$elapsed}s\n";
echo "  Mode            : " . ($DRY_RUN ? 'DRY RUN — No changes made' : 'LIVE — Changes saved') . "\n";
echo "\n";
if ($DRY_RUN) {
    echo "  💡 Run with ?force to apply changes: /seo_title_optimizer.php\n";
} else {
    echo "  ✅ SEO optimization complete!\n";
    echo "  📌 Flush cache to see changes: /flush_cache.php\n";
}
hr();
?>
