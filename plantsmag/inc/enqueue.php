<?php
/**
 * Enqueue Scripts and Styles
 *
 * @package PlantsMag
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Enqueue Frontend Styles and Scripts
 */
function plantsmag_scripts()
{
    // Google Fonts - Outfit & Inter
    wp_enqueue_style(
        'plantsmag-google-fonts',
        'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap',
        array(),
        PLANTSMAG_VERSION
    );

    // Main Stylesheet
    wp_enqueue_style(
        'plantsmag-style',
        get_stylesheet_uri(),
        array(),
        PLANTSMAG_VERSION
    );

    // Additional CSS
    wp_enqueue_style(
        'plantsmag-main',
        PLANTSMAG_URI . '/assets/css/main.css',
        array('plantsmag-style'),
        PLANTSMAG_VERSION
    );

    // Responsive CSS
    wp_enqueue_style(
        'plantsmag-responsive',
        PLANTSMAG_URI . '/assets/css/responsive.css',
        array('plantsmag-main'),
        PLANTSMAG_VERSION
    );

    // Animations CSS
    wp_enqueue_style(
        'plantsmag-animations',
        PLANTSMAG_URI . '/assets/css/animations.css',
        array('plantsmag-main'),
        PLANTSMAG_VERSION
    );

    // RTL Support
    if (is_rtl()) {
        wp_enqueue_style(
            'plantsmag-rtl',
            PLANTSMAG_URI . '/assets/css/rtl.css',
            array('plantsmag-main'),
            PLANTSMAG_VERSION
        );

        // Vazirmatn Font for Persian
        wp_enqueue_style(
            'plantsmag-vazirmatn',
            'https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap',
            array(),
            PLANTSMAG_VERSION
        );
    }

    // Navigation Script
    wp_enqueue_script(
        'plantsmag-navigation',
        PLANTSMAG_URI . '/assets/js/navigation.js',
        array(),
        PLANTSMAG_VERSION,
        true
    );

    // Main Script
    wp_enqueue_script(
        'plantsmag-main',
        PLANTSMAG_URI . '/assets/js/main.js',
        array(),
        PLANTSMAG_VERSION,
        true
    );

    // Add defer attribute to scripts for performance
    add_filter('script_loader_tag', 'plantsmag_defer_scripts', 10, 3);

    // Localize script with data
    wp_localize_script(
        'plantsmag-main',
        'plantsMagData',
        array(
            'ajaxUrl' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('plantsmag-nonce'),
            'homeUrl' => home_url(),
            'themeUrl' => PLANTSMAG_URI,
            'isRTL' => is_rtl(),
            'strings' => array(
                'loading' => esc_html__('Loading...', 'plantsmag'),
                'error' => esc_html__('Something went wrong.', 'plantsmag'),
                'searchLabel' => esc_html__('Search for:', 'plantsmag'),
            ),
        )
    );

    // Comment reply script
    if (is_singular() && comments_open() && get_option('thread_comments')) {
        wp_enqueue_script('comment-reply');
    }
}
add_action('wp_enqueue_scripts', 'plantsmag_scripts');

/**
 * Defer Non-Critical Scripts
 */
function plantsmag_defer_scripts($tag, $handle, $src)
{
    $defer_scripts = array(
        'plantsmag-navigation',
        'plantsmag-main',
    );

    if (in_array($handle, $defer_scripts, true)) {
        return str_replace(' src', ' defer src', $tag);
    }

    return $tag;
}

/**
 * Preload Key Resources
 */
function plantsmag_preload_resources()
{
    ?>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="dns-prefetch" href="//fonts.googleapis.com">
    <link rel="dns-prefetch" href="//fonts.gstatic.com">
    <?php
}
add_action('wp_head', 'plantsmag_preload_resources', 1);

/**
 * Admin Styles
 */
function plantsmag_admin_styles()
{
    wp_enqueue_style(
        'plantsmag-admin',
        PLANTSMAG_URI . '/assets/css/admin.css',
        array(),
        PLANTSMAG_VERSION
    );
}
add_action('admin_enqueue_scripts', 'plantsmag_admin_styles');
