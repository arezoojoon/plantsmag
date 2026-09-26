<?php
/**
 * Template Functions
 *
 * @package PlantsMag
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Add Custom Body Classes
 */
function plantsmag_body_classes($classes)
{
    // Adds a class of hfeed to non-singular pages.
    if (!is_singular()) {
        $classes[] = 'hfeed';
    }

    // Adds a class of no-sidebar when there is no sidebar present.
    if (!is_active_sidebar('sidebar-1')) {
        $classes[] = 'no-sidebar';
    }

    // Add class for sticky header
    if (get_theme_mod('plantsmag_sticky_header', true)) {
        $classes[] = 'has-sticky-header';
    }

    // Add page slug
    if (is_singular()) {
        global $post;
        $classes[] = 'page-' . $post->post_name;
    }

    // Add RTL class
    if (is_rtl()) {
        $classes[] = 'rtl';
    }

    return $classes;
}
add_filter('body_class', 'plantsmag_body_classes');

/**
 * Add Custom Post Classes
 */
function plantsmag_post_classes($classes)
{
    $classes[] = 'pm-card';
    return $classes;
}
add_filter('post_class', 'plantsmag_post_classes');

/**
 * Add Pingback Header
 */
function plantsmag_pingback_header()
{
    if (is_singular() && pings_open()) {
        printf('<link rel="pingback" href="%s">', esc_url(get_bloginfo('pingback_url')));
    }
}
add_action('wp_head', 'plantsmag_pingback_header');

/**
 * Custom Excerpt Length
 */
function plantsmag_excerpt_length($length)
{
    if (is_admin()) {
        return $length;
    }
    return 25;
}
add_filter('excerpt_length', 'plantsmag_excerpt_length');

/**
 * Custom Excerpt More
 */
function plantsmag_excerpt_more($more)
{
    if (is_admin()) {
        return $more;
    }
    return '&hellip;';
}
add_filter('excerpt_more', 'plantsmag_excerpt_more');

/**
 * Filter Archive Title
 */
function plantsmag_archive_title($title)
{
    if (is_category()) {
        $title = single_cat_title('', false);
    } elseif (is_tag()) {
        $title = single_tag_title('', false);
    } elseif (is_author()) {
        $title = get_the_author();
    } elseif (is_post_type_archive()) {
        $title = post_type_archive_title('', false);
    } elseif (is_tax()) {
        $title = single_term_title('', false);
    }

    return $title;
}
add_filter('get_the_archive_title', 'plantsmag_archive_title');

/**
 * Add SVG Support
 */
function plantsmag_mime_types($mimes)
{
    $mimes['svg'] = 'image/svg+xml';
    return $mimes;
}
add_filter('upload_mimes', 'plantsmag_mime_types');

/**
 * Wrap Embedded Videos Responsively
 */
function plantsmag_wrap_embed($html, $url, $attr, $post_id)
{
    if (strpos($html, 'youtube') !== false || strpos($html, 'vimeo') !== false) {
        return '<div class="responsive-embed">' . $html . '</div>';
    }
    return $html;
}
add_filter('embed_oembed_html', 'plantsmag_wrap_embed', 10, 4);

/**
 * Add Lazy Loading to Images in Content
 */
function plantsmag_lazy_load_images($content)
{
    if (is_admin() || is_feed()) {
        return $content;
    }
    return $content;
}
add_filter('the_content', 'plantsmag_lazy_load_images');

/**
 * Get Star Rating HTML
 */
function plantsmag_star_rating($rating, $max = 5)
{
    $rating = floatval($rating);
    $full = floor($rating);
    $half = ($rating - $full) >= 0.5 ? 1 : 0;
    $empty = $max - $full - $half;

    $stars = '';

    // Full stars
    for ($i = 0; $i < $full; $i++) {
        $stars .= '<svg class="star star-full" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>';
    }

    // Half star
    if ($half) {
        $stars .= '<svg class="star star-half" width="16" height="16" viewBox="0 0 24 24"><defs><linearGradient id="half"><stop offset="50%" stop-color="currentColor"/><stop offset="50%" stop-color="transparent"/></linearGradient></defs><path fill="url(#half)" stroke="currentColor" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>';
    }

    // Empty stars
    for ($i = 0; $i < $empty; $i++) {
        $stars .= '<svg class="star star-empty" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>';
    }

    return '<div class="star-rating" aria-label="' . sprintf(esc_attr__('Rating: %s out of %s', 'plantsmag'), $rating, $max) . '">' . $stars . '</div>';
}

/**
 * Get Plant Care Icon
 */
function plantsmag_care_icon($type)
{
    $icons = array(
        'light' => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>',
        'water' => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>',
        'humidity' => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/><path d="M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01"/></svg>',
        'temperature' => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg>',
    );

    return isset($icons[$type]) ? $icons[$type] : '';
}
