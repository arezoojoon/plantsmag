<?php
/**
 * Performance Optimizations
 *
 * @package PlantsMag
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Remove Emoji Scripts
 */
function plantsmag_disable_emojis()
{
    remove_action('wp_head', 'print_emoji_detection_script', 7);
    remove_action('admin_print_scripts', 'print_emoji_detection_script');
    remove_action('wp_print_styles', 'print_emoji_styles');
    remove_action('admin_print_styles', 'print_emoji_styles');
    remove_filter('the_content_feed', 'wp_staticize_emoji');
    remove_filter('comment_text_rss', 'wp_staticize_emoji');
    remove_filter('wp_mail', 'wp_staticize_emoji_for_email');

    add_filter('tiny_mce_plugins', 'plantsmag_disable_emojis_tinymce');
    add_filter('wp_resource_hints', 'plantsmag_disable_emojis_dns_prefetch', 10, 2);
}
add_action('init', 'plantsmag_disable_emojis');

/**
 * Disable Emoji TinyMCE
 */
function plantsmag_disable_emojis_tinymce($plugins)
{
    if (is_array($plugins)) {
        return array_diff($plugins, array('wpemoji'));
    }
    return array();
}

/**
 * Disable Emoji DNS Prefetch
 */
function plantsmag_disable_emojis_dns_prefetch($urls, $relation_type)
{
    if ('dns-prefetch' === $relation_type) {
        $emoji_svg_url = apply_filters('emoji_svg_url', 'https://s.w.org/images/core/emoji/2/svg/');
        $urls = array_diff($urls, array($emoji_svg_url));
    }
    return $urls;
}

/**
 * Remove jQuery Migrate
 */
function plantsmag_remove_jquery_migrate($scripts)
{
    if (!is_admin() && isset($scripts->registered['jquery'])) {
        $script = $scripts->registered['jquery'];
        if ($script->deps) {
            $script->deps = array_diff($script->deps, array('jquery-migrate'));
        }
    }
}
add_action('wp_default_scripts', 'plantsmag_remove_jquery_migrate');

/**
 * Add Resource Hints
 */
function plantsmag_resource_hints($urls, $relation_type)
{
    if ('dns-prefetch' === $relation_type) {
        $urls[] = '//fonts.googleapis.com';
        $urls[] = '//fonts.gstatic.com';
    }

    if ('preconnect' === $relation_type) {
        $urls[] = array(
            'href' => 'https://fonts.gstatic.com',
            'crossorigin' => 'anonymous',
        );
    }

    return $urls;
}
add_filter('wp_resource_hints', 'plantsmag_resource_hints', 10, 2);

/**
 * Disable WP Embed
 */
function plantsmag_disable_wp_embed()
{
    if (!is_admin()) {
        wp_dequeue_script('wp-embed');
    }
}
add_action('wp_footer', 'plantsmag_disable_wp_embed');

/**
 * Remove WP Version
 */
remove_action('wp_head', 'wp_generator');

/**
 * Remove RSD Link
 */
remove_action('wp_head', 'rsd_link');

/**
 * Remove wlwmanifest Link
 */
remove_action('wp_head', 'wlwmanifest_link');

/**
 * Remove Shortlink
 */
remove_action('wp_head', 'wp_shortlink_wp_head');

/**
 * Disable Self Pingback
 */
function plantsmag_disable_self_pingback(&$links)
{
    $home = get_option('home');
    foreach ($links as $l => $link) {
        if (0 === strpos($link, $home)) {
            unset($links[$l]);
        }
    }
}
add_action('pre_ping', 'plantsmag_disable_self_pingback');

/**
 * Limit Post Revisions
 */
if (!defined('WP_POST_REVISIONS')) {
    define('WP_POST_REVISIONS', 5);
}

/**
 * Add Lazy Loading to iframes
 */
function plantsmag_lazy_load_iframes($content)
{
    if (is_admin() || is_feed()) {
        return $content;
    }

    $content = preg_replace('/<iframe(.*?)(?!loading)>/i', '<iframe loading="lazy"$1>', $content);
    return $content;
}
add_filter('the_content', 'plantsmag_lazy_load_iframes', 15);

/**
 * Optimize Heartbeat API
 */
function plantsmag_optimize_heartbeat($settings)
{
    $settings['interval'] = 60;
    return $settings;
}
add_filter('heartbeat_settings', 'plantsmag_optimize_heartbeat');

/**
 * Add Async/Defer to Scripts
 */
function plantsmag_add_async_defer($tag, $handle, $src)
{
    $async_scripts = array();
    $defer_scripts = array('plantsmag-main', 'plantsmag-navigation');

    if (in_array($handle, $async_scripts, true)) {
        return str_replace(' src', ' async src', $tag);
    }

    if (in_array($handle, $defer_scripts, true)) {
        return str_replace(' src', ' defer src', $tag);
    }

    return $tag;
}
add_filter('script_loader_tag', 'plantsmag_add_async_defer', 10, 3);

/**
 * Preload Critical Fonts
 */
function plantsmag_preload_fonts()
{
    ?>
    <link rel="preload" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap" as="style"
        onload="this.onload=null;this.rel='stylesheet'">
    <noscript>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap">
    </noscript>
    <?php
}
// add_action( 'wp_head', 'plantsmag_preload_fonts', 1 );

/**
 * Remove Query Strings from Static Resources
 */
function plantsmag_remove_query_strings($src)
{
    if (strpos($src, '?ver=')) {
        $src = remove_query_arg('ver', $src);
    }
    return $src;
}
// Uncomment if needed:
// add_filter( 'style_loader_src', 'plantsmag_remove_query_strings', 15, 1 );
// add_filter( 'script_loader_src', 'plantsmag_remove_query_strings', 15, 1 );
