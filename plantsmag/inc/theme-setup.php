<?php
/**
 * Theme Setup
 *
 * @package PlantsMag
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Setup Theme Features
 */
function plantsmag_setup()
{
    // Make theme available for translation
    load_theme_textdomain('plantsmag', PLANTSMAG_DIR . '/languages');

    // Add default posts and comments RSS feed links to head
    add_theme_support('automatic-feed-links');

    // Let WordPress manage the document title
    add_theme_support('title-tag');

    // Enable support for Post Thumbnails
    add_theme_support('post-thumbnails');

    // Custom image sizes
    add_image_size('plantsmag-featured', 1200, 630, true);
    add_image_size('plantsmag-card', 600, 400, true);
    add_image_size('plantsmag-thumbnail', 300, 200, true);
    add_image_size('plantsmag-square', 600, 600, true);

    // Register Navigation Menus
    register_nav_menus(
        array(
            'primary' => esc_html__('Primary Menu', 'plantsmag'),
            'footer' => esc_html__('Footer Menu', 'plantsmag'),
            'social' => esc_html__('Social Menu', 'plantsmag'),
        )
    );

    // Switch default core markup for forms to output valid HTML5
    add_theme_support(
        'html5',
        array(
            'search-form',
            'comment-form',
            'comment-list',
            'gallery',
            'caption',
            'style',
            'script',
        )
    );

    // Custom logo support
    add_theme_support(
        'custom-logo',
        array(
            'height' => 100,
            'width' => 300,
            'flex-width' => true,
            'flex-height' => true,
        )
    );

    // Custom background support
    add_theme_support(
        'custom-background',
        array(
            'default-color' => 'ffffff',
        )
    );

    // Add support for responsive embeds
    add_theme_support('responsive-embeds');

    // Add support for Block Editor (Gutenberg)
    add_theme_support('align-wide');
    add_theme_support('wp-block-styles');
    add_theme_support('editor-styles');
    add_editor_style('assets/css/editor-style.css');

    // Add support for selective refresh for widgets
    add_theme_support('customize-selective-refresh-widgets');

    // WooCommerce support
    add_theme_support('woocommerce');
    add_theme_support('wc-product-gallery-zoom');
    add_theme_support('wc-product-gallery-lightbox');
    add_theme_support('wc-product-gallery-slider');
}
add_action('after_setup_theme', 'plantsmag_setup');

/**
 * Register Widget Areas
 */
function plantsmag_widgets_init()
{
    // Sidebar
    register_sidebar(
        array(
            'name' => esc_html__('Sidebar', 'plantsmag'),
            'id' => 'sidebar-1',
            'description' => esc_html__('Add widgets here to appear in the sidebar.', 'plantsmag'),
            'before_widget' => '<section id="%1$s" class="widget %2$s">',
            'after_widget' => '</section>',
            'before_title' => '<h3 class="widget-title">',
            'after_title' => '</h3>',
        )
    );

    // Footer Widget Areas
    for ($i = 1; $i <= 4; $i++) {
        register_sidebar(
            array(
                'name' => sprintf(esc_html__('Footer %d', 'plantsmag'), $i),
                'id' => 'footer-' . $i,
                'description' => sprintf(esc_html__('Add widgets here to appear in footer column %d.', 'plantsmag'), $i),
                'before_widget' => '<div id="%1$s" class="widget %2$s">',
                'after_widget' => '</div>',
                'before_title' => '<h4 class="widget-title">',
                'after_title' => '</h4>',
            )
        );
    }

    // Header Widget Area
    register_sidebar(
        array(
            'name' => esc_html__('Header Widget', 'plantsmag'),
            'id' => 'header-widget',
            'description' => esc_html__('Add widgets here to appear in the header area.', 'plantsmag'),
            'before_widget' => '<div id="%1$s" class="header-widget %2$s">',
            'after_widget' => '</div>',
            'before_title' => '<span class="screen-reader-text">',
            'after_title' => '</span>',
        )
    );
}
add_action('widgets_init', 'plantsmag_widgets_init');
