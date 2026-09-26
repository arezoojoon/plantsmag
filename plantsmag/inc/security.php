<?php
/**
 * Security Hardening
 *
 * @package PlantsMag
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Remove WordPress Version
 */
function plantsmag_remove_version()
{
    return '';
}
add_filter('the_generator', 'plantsmag_remove_version');

/**
 * Remove Version from Scripts and Styles
 */
function plantsmag_remove_version_scripts_styles($src)
{
    if (strpos($src, 'ver=')) {
        $src = remove_query_arg('ver', $src);
    }
    return $src;
}
// add_filter( 'style_loader_src', 'plantsmag_remove_version_scripts_styles', 9999 );
// add_filter( 'script_loader_src', 'plantsmag_remove_version_scripts_styles', 9999 );

/**
 * Disable XML-RPC
 */
add_filter('xmlrpc_enabled', '__return_false');

/**
 * Remove XML-RPC from HTTP Headers
 */
function plantsmag_remove_x_pingback($headers)
{
    unset($headers['X-Pingback']);
    return $headers;
}
add_filter('wp_headers', 'plantsmag_remove_x_pingback');

/**
 * Disable Author Archives for Bots
 */
function plantsmag_disable_author_archive()
{
    if (is_author()) {
        global $wp_query;
        $wp_query->set_404();
        status_header(404);
        nocache_headers();
    }
}
// Uncomment to enable:
// add_action( 'template_redirect', 'plantsmag_disable_author_archive' );

/**
 * Add Security Headers
 */
function plantsmag_security_headers()
{
    if (!is_admin()) {
        header('X-Content-Type-Options: nosniff');
        header('X-Frame-Options: SAMEORIGIN');
        header('X-XSS-Protection: 1; mode=block');
        header('Referrer-Policy: strict-origin-when-cross-origin');
    }
}
add_action('send_headers', 'plantsmag_security_headers');

/**
 * Disable File Editing in Admin
 */
if (!defined('DISALLOW_FILE_EDIT')) {
    define('DISALLOW_FILE_EDIT', true);
}

/**
 * Sanitize File Uploads
 */
function plantsmag_sanitize_file_name($filename)
{
    $info = pathinfo($filename);
    $ext = empty($info['extension']) ? '' : '.' . $info['extension'];
    $name = basename($filename, $ext);

    // Remove special characters
    $name = sanitize_file_name($name);

    return $name . $ext;
}
add_filter('sanitize_file_name', 'plantsmag_sanitize_file_name', 10);

/**
 * Limit Login Attempts Message
 */
function plantsmag_login_errors()
{
    return __('Invalid login credentials.', 'plantsmag');
}
add_filter('login_errors', 'plantsmag_login_errors');

/**
 * Disable REST API for Non-Logged Users (Optional)
 */
function plantsmag_rest_api_authentication($result)
{
    if (!empty($result)) {
        return $result;
    }

    if (!is_user_logged_in()) {
        // Allow specific endpoints
        $allowed = array(
            '/wp/v2/posts',
            '/wp/v2/pages',
            '/wp/v2/categories',
            '/wp/v2/tags',
        );

        $current = isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '';

        foreach ($allowed as $endpoint) {
            if (strpos($current, $endpoint) !== false) {
                return $result;
            }
        }
    }

    return $result;
}
// Uncomment to enable:
// add_filter( 'rest_authentication_errors', 'plantsmag_rest_api_authentication' );

/**
 * Remove User Enumeration
 */
function plantsmag_disable_user_enumeration()
{
    if (!is_admin()) {
        if (isset($_REQUEST['author']) && is_numeric($_REQUEST['author'])) {
            wp_die(__('Author archives have been disabled.', 'plantsmag'), 403);
        }
    }
}
add_action('init', 'plantsmag_disable_user_enumeration');

/**
 * Add Nonce to Forms
 */
function plantsmag_add_nonce_field()
{
    wp_nonce_field('plantsmag_form_action', 'plantsmag_form_nonce');
}

/**
 * Verify Nonce
 */
function plantsmag_verify_nonce()
{
    if (!isset($_POST['plantsmag_form_nonce']) || !wp_verify_nonce($_POST['plantsmag_form_nonce'], 'plantsmag_form_action')) {
        return false;
    }
    return true;
}

/**
 * Escape Output Helper
 */
function plantsmag_esc($string, $type = 'html')
{
    switch ($type) {
        case 'attr':
            return esc_attr($string);
        case 'url':
            return esc_url($string);
        case 'js':
            return esc_js($string);
        case 'textarea':
            return esc_textarea($string);
        case 'html':
        default:
            return esc_html($string);
    }
}
