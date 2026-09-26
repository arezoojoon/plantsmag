<?php
/**
 * PlantsMag — Google Indexing API Integration
 * ============================================
 * Uses Google's official Indexing API to request immediate crawling.
 * This is the ONLY direct path to Google indexing (not via IndexNow).
 *
 * SETUP REQUIRED:
 *   1. Go to https://console.cloud.google.com
 *   2. Create project → Enable "Indexing API"
 *   3. Create Service Account → Download JSON key
 *   4. Save JSON key to: scripts/google_indexing_key.json
 *   5. In Google Search Console → Settings → Users → add Service Account email as Owner
 *
 * Usage:
 *   require_once 'google_indexing_api.php';
 *   $result = google_index_urls(['https://plantsmag.com/your-post/']);
 */

define('GOOGLE_INDEXING_KEY_PATH', __DIR__ . '/scripts/google_indexing_key.json');
define('GOOGLE_INDEXING_SCOPE', 'https://www.googleapis.com/auth/indexing');
define('GOOGLE_INDEXING_ENDPOINT', 'https://indexing.googleapis.com/v3/urlNotifications:publish');
define('GOOGLE_INDEXING_BATCH', 'https://indexing.googleapis.com/batch');

/**
 * Generate JWT token for Google Service Account authentication
 */
function google_indexing_get_jwt() {
    if (!file_exists(GOOGLE_INDEXING_KEY_PATH)) {
        return ['error' => 'Key file not found: ' . GOOGLE_INDEXING_KEY_PATH];
    }

    $key_data = json_decode(file_get_contents(GOOGLE_INDEXING_KEY_PATH), true);
    if (!$key_data || !isset($key_data['private_key'])) {
        return ['error' => 'Invalid key file format'];
    }

    $now = time();
    $header = base64_encode(json_encode(['alg' => 'RS256', 'typ' => 'JWT']));
    $header = rtrim(strtr($header, '+/', '-_'), '=');

    $claim = base64_encode(json_encode([
        'iss'   => $key_data['client_email'],
        'scope' => GOOGLE_INDEXING_SCOPE,
        'aud'   => 'https://oauth2.googleapis.com/token',
        'exp'   => $now + 3600,
        'iat'   => $now,
    ]));
    $claim = rtrim(strtr($claim, '+/', '-_'), '=');

    $sig_input = $header . '.' . $claim;
    $private_key = openssl_pkey_get_private($key_data['private_key']);
    if (!$private_key) {
        return ['error' => 'Failed to load private key'];
    }

    openssl_sign($sig_input, $signature, $private_key, 'SHA256');
    $sig = rtrim(strtr(base64_encode($signature), '+/', '-_'), '=');

    return $header . '.' . $claim . '.' . $sig;
}

/**
 * Exchange JWT for OAuth2 access token
 */
function google_indexing_get_token() {
    static $cached_token = null;
    static $token_expiry = 0;

    if ($cached_token && time() < $token_expiry) {
        return $cached_token;
    }

    $jwt = google_indexing_get_jwt();
    if (is_array($jwt) && isset($jwt['error'])) {
        return $jwt;
    }

    $ch = curl_init('https://oauth2.googleapis.com/token');
    curl_setopt_array($ch, [
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => http_build_query([
            'grant_type' => 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion'  => $jwt,
        ]),
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 15,
        CURLOPT_HTTPHEADER     => ['Content-Type: application/x-www-form-urlencoded'],
    ]);
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    $data = json_decode($response, true);
    if ($http_code !== 200 || !isset($data['access_token'])) {
        return ['error' => "Token exchange failed: HTTP {$http_code} — " . ($data['error_description'] ?? $response)];
    }

    $cached_token = $data['access_token'];
    $token_expiry = time() + $data['expires_in'] - 60;
    return $cached_token;
}

/**
 * Submit URLs to Google Indexing API using batch requests
 * 
 * @param array  $urls  List of URLs to submit
 * @param string $type  'URL_UPDATED' or 'URL_DELETED'
 * @return array        Results per URL
 */
function google_index_urls(array $urls, $type = 'URL_UPDATED') {
    if (empty($urls)) {
        return ['error' => 'No URLs provided'];
    }

    // Check if key file exists
    if (!file_exists(GOOGLE_INDEXING_KEY_PATH)) {
        return [
            'status'  => 'skipped',
            'message' => '⚠️ Google Indexing API: Key file not found. See setup instructions in google_indexing_api.php',
            'key_path' => GOOGLE_INDEXING_KEY_PATH
        ];
    }

    $token = google_indexing_get_token();
    if (is_array($token) && isset($token['error'])) {
        return $token;
    }

    // Google Indexing API allows max 100 URLs per request
    // Use batch HTTP to send multiple in one request
    $chunks = array_chunk($urls, 100);
    $all_results = [];

    foreach ($chunks as $chunk) {
        // Build batch request body
        $boundary = 'batch_plantsmag_' . uniqid();
        $batch_body = '';

        foreach ($chunk as $i => $url) {
            $batch_body .= "--{$boundary}\r\n";
            $batch_body .= "Content-Type: application/http\r\n";
            $batch_body .= "Content-ID: <item{$i}:plantsmag>\r\n\r\n";
            $batch_body .= "POST /v3/urlNotifications:publish HTTP/1.1\r\n";
            $batch_body .= "Content-Type: application/json\r\n\r\n";
            $batch_body .= json_encode(['url' => $url, 'type' => $type]) . "\r\n";
        }
        $batch_body .= "--{$boundary}--\r\n";

        $ch = curl_init(GOOGLE_INDEXING_BATCH);
        curl_setopt_array($ch, [
            CURLOPT_POST           => true,
            CURLOPT_POSTFIELDS     => $batch_body,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT        => 30,
            CURLOPT_HTTPHEADER     => [
                "Authorization: Bearer {$token}",
                "Content-Type: multipart/mixed; boundary={$boundary}",
            ],
        ]);

        $response  = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        // Parse batch response to count successes
        $success_count = substr_count($response, 'HTTP/1.1 200');
        $already_count = substr_count($response, 'HTTP/1.1 429'); // quota exceeded

        $all_results[] = [
            'urls_submitted' => count($chunk),
            'http_code'      => $http_code,
            'success'        => $success_count,
            'quota_exceeded' => $already_count,
            'raw'            => substr($response, 0, 500),
        ];
    }

    return [
        'status'  => 'submitted',
        'total'   => count($urls),
        'chunks'  => count($chunks),
        'results' => $all_results,
    ];
}

// ── Standalone runner (when called directly) ──────────────────────────────────
if (basename(__FILE__) === basename($_SERVER['SCRIPT_FILENAME'] ?? '') || php_sapi_name() === 'cli') {
    if (!defined('ABSPATH')) {
        // Find WordPress
        $wp_load = __DIR__ . '/wp-load.php';
        if (!file_exists($wp_load)) {
            $wp_load = dirname(__DIR__) . '/wp-load.php';
        }
        if (file_exists($wp_load)) {
            require_once $wp_load;
        }
    }

    header('Content-Type: text/plain; charset=UTF-8');

    echo "🔍 Google Indexing API — PlantsMag\n";
    echo str_repeat('─', 50) . "\n\n";

    // Check key file
    if (!file_exists(GOOGLE_INDEXING_KEY_PATH)) {
        echo "⚠️  Key file NOT found at: " . GOOGLE_INDEXING_KEY_PATH . "\n\n";
        echo "SETUP INSTRUCTIONS:\n";
        echo "1. Go to https://console.cloud.google.com\n";
        echo "2. Create project → Enable 'Indexing API'\n";
        echo "3. Create Service Account → Download JSON key\n";
        echo "4. mkdir " . dirname(GOOGLE_INDEXING_KEY_PATH) . "\n";
        echo "5. Upload JSON file to: " . GOOGLE_INDEXING_KEY_PATH . "\n";
        echo "6. In GSC → Settings → Users → add Service Account email as Owner\n\n";
        echo "Once key is in place, run this script again.\n";
        exit(0);
    }

    // Get recent published posts
    global $wpdb;
    $posts = $wpdb->get_col(
        "SELECT ID FROM {$wpdb->posts}
         WHERE post_status = 'publish' AND post_type = 'post'
         ORDER BY post_modified DESC LIMIT 100"
    );

    $urls = [];
    foreach ($posts as $id) {
        $urls[] = get_permalink($id);
    }

    // Add homepage and sitemap
    $urls[] = home_url('/');

    echo "📋 Submitting " . count($urls) . " URLs to Google Indexing API...\n\n";

    $result = google_index_urls($urls);

    if (isset($result['error'])) {
        echo "❌ ERROR: " . $result['error'] . "\n";
    } elseif (isset($result['status']) && $result['status'] === 'skipped') {
        echo $result['message'] . "\n";
    } else {
        echo "✅ Submitted: {$result['total']} URLs\n";
        echo "   Chunks: {$result['chunks']}\n";
        foreach ($result['results'] as $i => $r) {
            echo "   Batch " . ($i + 1) . ": HTTP {$r['http_code']} — {$r['success']} success\n";
        }
    }

    echo "\n" . str_repeat('─', 50) . "\n";
}
