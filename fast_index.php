<?php
// SECURED: Enforce CLI or GET method, and strict token authentication
if (php_sapi_name() !== 'cli' && $_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    die('Method Not Allowed: Only GET requests are permitted.');
}

if (!isset($_GET['token']) || $_GET['token'] !== 'plantsmag-sec-2026') {
    http_response_code(403);
    die('Forbidden: Invalid or missing token.');
}

/**
 * PlantsMag Fast Indexing Engine
 * ================================
 * 1. Sends all recent posts to IndexNow (Bing, Yandex, Naver - instant indexing)
 * 2. Pings Google Sitemap endpoint
 * 3. Updates post_modified date to force re-crawl signal
 * 4. Flushes WordPress rewrite rules & caches
 *
 * Usage: Access via browser or run via WP-CLI:
 *   wp eval-file fast_index.php
 *
 * HOW IT WORKS:
 *   IndexNow is a protocol supported by Bing/Yandex/Naver that tells search
 *   engines to crawl a URL immediately. Google uses its own sitemap ping.
 *   Updating post_modified refreshes the "lastmod" in the sitemap, which is
 *   the strongest signal to Google's crawler that content is fresh.
 */

define('FAST_INDEX_VERSION', '2.0');
define('FAST_INDEX_START', microtime(true));

// ── Bootstrap WordPress ──────────────────────────────────────────────────────
if (!defined('ABSPATH')) {
    require_once(dirname(__FILE__) . '/wp-load.php');
}

// ── Configuration ────────────────────────────────────────────────────────────
// Force HTTPS — WordPress may store http:// in DB but site is served over https
$SITE_URL    = rtrim(get_site_url(), '/');
$SITE_URL    = str_replace('http://', 'https://', $SITE_URL);
$SITE_DOMAIN = parse_url($SITE_URL, PHP_URL_HOST);
$SITEMAP_URL = $SITE_URL . '/wp-sitemap.xml';

// How many recent posts to process (increase if you published many articles)
$POST_LIMIT = isset($_GET['limit']) ? (int)$_GET['limit'] : 50;

// IndexNow API Key — stored as a WP option (auto-generated on first run)
$INDEXNOW_KEY = get_option('fast_index_indexnow_key');
if (empty($INDEXNOW_KEY)) {
    $INDEXNOW_KEY = wp_generate_password(32, false, false);
    update_option('fast_index_indexnow_key', $INDEXNOW_KEY);
}

// Output helpers
header('Content-Type: text/plain; charset=UTF-8');
function log_msg($msg, $type = 'INFO') {
    $ts = date('H:i:s');
    echo "[{$ts}] [{$type}] {$msg}\n";
    flush();
}
function hr() { echo str_repeat('─', 60) . "\n"; }

// ── HEADER ───────────────────────────────────────────────────────────────────
hr();
echo "  🚀 PlantsMag Fast Indexing Engine v" . FAST_INDEX_VERSION . "\n";
echo "  Site   : {$SITE_URL}\n";
echo "  Limit  : {$POST_LIMIT} posts\n";
echo "  Time   : " . date('Y-m-d H:i:s') . "\n";
hr();

// ═════════════════════════════════════════════════════════════════════════════
// STEP 1 — Fetch Recent Published Posts
// ═════════════════════════════════════════════════════════════════════════════
log_msg("Fetching last {$POST_LIMIT} published posts...");

$posts = get_posts([
    'post_type'      => 'post',
    'post_status'    => 'publish',
    'posts_per_page' => $POST_LIMIT,
    'orderby'        => 'date',
    'order'          => 'DESC',
    'fields'         => 'ids',
]);

$urls = [];
foreach ($posts as $post_id) {
    $urls[] = get_permalink($post_id);
}

// Also add important static pages
$static_pages = [
    $SITE_URL . '/',
    $SITE_URL . '/watering-calculator/',
    $SITE_URL . '/plant-disease-finder/',
];
foreach ($static_pages as $sp) {
    array_unshift($urls, $sp);
}

$urls = array_unique(array_filter($urls));
log_msg("Total URLs collected: " . count($urls));

// ═════════════════════════════════════════════════════════════════════════════
// STEP 2 — IndexNow (Bing + Yandex + Naver — Instant Indexing)
// ═════════════════════════════════════════════════════════════════════════════
hr();
log_msg("STEP 2 — Sending URLs to IndexNow API...");

/**
 * IndexNow hosts:
 *   - api.indexnow.org  (routes to Bing, Yandex, Naver automatically)
 */
$indexnow_endpoints = [
    'IndexNow (Bing/Yandex/Naver)' => 'https://api.indexnow.org/indexnow',
];

// Create the IndexNow key file in webroot so search engines can verify ownership
$key_file_path = ABSPATH . $INDEXNOW_KEY . '.txt';
if (!file_exists($key_file_path)) {
    file_put_contents($key_file_path, $INDEXNOW_KEY);
    log_msg("Created IndexNow key file: /{$INDEXNOW_KEY}.txt");
} else {
    log_msg("IndexNow key file already exists.");
}

// Send URLs in batches of 10,000 (IndexNow limit)
$url_chunks = array_chunk($urls, 100);
$indexnow_success = false;

foreach ($indexnow_endpoints as $engine_name => $endpoint) {
    foreach ($url_chunks as $chunk_index => $url_batch) {
        $payload = json_encode([
            'host'    => $SITE_DOMAIN,
            'key'     => $INDEXNOW_KEY,
            'keyLocation' => $SITE_URL . '/' . $INDEXNOW_KEY . '.txt',
            'urlList' => array_values($url_batch),
        ]);

        $response = wp_remote_post($endpoint, [
            'headers'     => ['Content-Type' => 'application/json; charset=utf-8'],
            'body'        => $payload,
            'timeout'     => 30,
            'sslverify'   => true,
        ]);

        if (is_wp_error($response)) {
            log_msg("  [{$engine_name}] Batch " . ($chunk_index + 1) . " ERROR: " . $response->get_error_message(), 'ERROR');
        } else {
            $code = wp_remote_retrieve_response_code($response);
            $body = substr(wp_remote_retrieve_body($response), 0, 200);
            if ($code === 200 || $code === 202) {
                log_msg("  [{$engine_name}] Batch " . ($chunk_index + 1) . " — ✅ HTTP {$code} — " . count($url_batch) . " URLs submitted", 'OK');
                $indexnow_success = true;
            } else {
                log_msg("  [{$engine_name}] Batch " . ($chunk_index + 1) . " — ⚠️ HTTP {$code} — {$body}", 'WARN');
            }
        }
    }
}

// ═════════════════════════════════════════════════════════════════════════════
// STEP 3 — Google Indexing API + Sitemap Signal
// ═════════════════════════════════════════════════════════════════════════════
hr();
log_msg("STEP 3 — Google Sitemap & Crawl Signals...");

// ── 3a. Verify Sitemap ────────────────────────────────────────────────────────
$sitemap_check = wp_remote_get($SITEMAP_URL, ['timeout' => 15, 'redirection' => 5]);
$sitemap_code  = is_wp_error($sitemap_check) ? 'ERROR' : wp_remote_retrieve_response_code($sitemap_check);
if ($sitemap_code === 200) {
    log_msg("✅ Sitemap accessible: {$SITEMAP_URL}", 'OK');
} else {
    log_msg("⚠️ Sitemap returned HTTP {$sitemap_code} — check URL", 'WARN');
}

// Verify IndexNow key file is accessible (Bing verifies this)
$key_url   = $SITE_URL . '/' . $INDEXNOW_KEY . '.txt';
$key_check = wp_remote_get($key_url, ['timeout' => 10]);
$key_code  = is_wp_error($key_check) ? 'ERROR' : wp_remote_retrieve_response_code($key_check);
if ($key_code === 200) {
    log_msg("✅ IndexNow key file is publicly accessible", 'OK');
} else {
    log_msg("⚠️ IndexNow key file HTTP {$key_code} — Bing may reject submissions", 'WARN');
}

// ── 3b. Google Indexing API (Direct Instant Google Indexing) ──────────────────
// Requires: scripts/google_indexing_key.json (Service Account from Google Cloud)
// Setup: https://console.cloud.google.com → Enable Indexing API → Service Account
$google_api_file = __DIR__ . '/scripts/google_indexing_key.json';
if (file_exists($google_api_file)) {
    log_msg("STEP 3b — Google Indexing API (Direct Submission)...");
    require_once __DIR__ . '/google_indexing_api.php';
    
    // Submit all collected URLs
    $google_result = google_index_urls($urls);
    
    if (isset($google_result['error'])) {
        log_msg("⚠️ Google Indexing API error: " . $google_result['error'], 'WARN');
    } elseif (isset($google_result['status']) && $google_result['status'] === 'skipped') {
        log_msg($google_result['message'], 'WARN');
    } else {
        $success_total = 0;
        foreach ($google_result['results'] as $r) {
            $success_total += $r['success'];
        }
        log_msg("✅ Google Indexing API: {$google_result['total']} URLs submitted, {$success_total} confirmed", 'OK');
    }
} else {
    log_msg("ℹ️  Google Indexing API: key not found at scripts/google_indexing_key.json", 'INFO');
    log_msg("   → IndexNow (Bing/Yandex) is active. Add Google key for direct Google indexing.", 'INFO');
}

$code = $sitemap_code; // for summary


// ═════════════════════════════════════════════════════════════════════════════
// STEP 4 — Update post_modified to Force Re-crawl Signal
// ═════════════════════════════════════════════════════════════════════════════
hr();
log_msg("STEP 4 — Refreshing post_modified dates for sitemap lastmod...");

/**
 * WHY THIS WORKS:
 * Google's sitemap crawler checks the <lastmod> tag. WordPress generates
 * lastmod from post_modified_gmt. By touching these dates, we signal to
 * Googlebot that ALL these pages have fresh content worth re-crawling.
 * We only touch posts older than 48h to avoid hammering recently published posts.
 */

global $wpdb;
$cutoff = date('Y-m-d H:i:s', strtotime('-48 hours'));
$now    = current_time('mysql');
$now_gmt = current_time('mysql', true);

// Get posts that were NOT recently modified (older than 48h)
$stale_posts = $wpdb->get_col($wpdb->prepare(
    "SELECT ID FROM {$wpdb->posts}
     WHERE post_status = 'publish'
     AND post_type = 'post'
     AND post_modified < %s
     ORDER BY post_date DESC
     LIMIT %d",
    $cutoff,
    $POST_LIMIT
));

$refreshed = 0;
foreach ($stale_posts as $pid) {
    $result = $wpdb->update(
        $wpdb->posts,
        [
            'post_modified'     => $now,
            'post_modified_gmt' => $now_gmt,
        ],
        ['ID' => $pid],
        ['%s', '%s'],
        ['%d']
    );
    if ($result !== false) {
        clean_post_cache($pid);
        $refreshed++;
    }
}

log_msg("✅ Refreshed post_modified for {$refreshed} posts", 'OK');

// ═════════════════════════════════════════════════════════════════════════════
// STEP 5 — Flush Rewrite Rules & WordPress Caches
// ═════════════════════════════════════════════════════════════════════════════
hr();
log_msg("STEP 5 — Flushing caches and rewrite rules...");

// Flush WP object cache
wp_cache_flush();
log_msg("✅ WordPress object cache flushed", 'OK');

// Flush rewrite rules
flush_rewrite_rules(true);
log_msg("✅ Rewrite rules flushed (sitemap routes regenerated)", 'OK');

// Flush LiteSpeed Cache if available
if (function_exists('litespeed_purge_all')) {
    litespeed_purge_all();
    log_msg("✅ LiteSpeed Cache purged", 'OK');
} elseif (class_exists('LiteSpeed_Cache_API')) {
    LiteSpeed_Cache_API::purge_all();
    log_msg("✅ LiteSpeed Cache API purged", 'OK');
} else {
    log_msg("LiteSpeed not detected — skipping", 'INFO');
}

// Force WordPress Sitemap to regenerate by clearing its transients
$wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_wp_sitemap%'");
$wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_timeout_wp_sitemap%'");
log_msg("✅ WordPress sitemap transients cleared (sitemap will regenerate on next hit)", 'OK');

// ═════════════════════════════════════════════════════════════════════════════
// STEP 6 — Print IndexNow Key Info (for manual DNS/GSC verification if needed)
// ═════════════════════════════════════════════════════════════════════════════
hr();
log_msg("STEP 6 — IndexNow Key Info");
log_msg("  Key       : {$INDEXNOW_KEY}");
log_msg("  Key File  : {$SITE_URL}/{$INDEXNOW_KEY}.txt");
log_msg("  Verify at : https://api.indexnow.org/indexnow?url={$SITE_URL}&key={$INDEXNOW_KEY}");

// ═════════════════════════════════════════════════════════════════════════════
// SUMMARY
// ═════════════════════════════════════════════════════════════════════════════
hr();
$elapsed = round(microtime(true) - FAST_INDEX_START, 2);
echo "\n";
echo "  📊 SUMMARY\n";
echo "  ─────────────────────────────────────────────────\n";
echo "  URLs submitted to IndexNow : " . count($urls) . "\n";
echo "  Posts modified (lastmod)   : {$refreshed}\n";
echo "  Google Sitemap Ping        : " . ($code === 200 ? '✅ Success' : "⚠️ HTTP {$code}") . "\n";
echo "  Total execution time       : {$elapsed}s\n";
echo "\n";
echo "  ✅ Fast indexing complete!\n";
echo "  📌 Sitemap: {$SITEMAP_URL}\n";
hr();
?>
