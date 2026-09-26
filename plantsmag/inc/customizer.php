<?php
/**
 * Theme Customizer
 *
 * @package PlantsMag
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Register Customizer Settings
 */
function plantsmag_customize_register($wp_customize)
{

    // ========================================
    // Theme Options Panel
    // ========================================
    $wp_customize->add_panel(
        'plantsmag_theme_options',
        array(
            'title' => __('Theme Options', 'plantsmag'),
            'priority' => 30,
            'description' => __('Customize the theme settings.', 'plantsmag'),
        )
    );

    // ========================================
    // Colors Section
    // ========================================
    $wp_customize->add_section(
        'plantsmag_colors',
        array(
            'title' => __('Theme Colors', 'plantsmag'),
            'panel' => 'plantsmag_theme_options',
            'priority' => 10,
        )
    );

    // Primary Color
    $wp_customize->add_setting(
        'plantsmag_primary_color',
        array(
            'default' => '#2D4A3E',
            'sanitize_callback' => 'sanitize_hex_color',
            'transport' => 'postMessage',
        )
    );

    $wp_customize->add_control(
        new WP_Customize_Color_Control(
            $wp_customize,
            'plantsmag_primary_color',
            array(
                'label' => __('Primary Color', 'plantsmag'),
                'section' => 'plantsmag_colors',
            )
        )
    );

    // Accent Color
    $wp_customize->add_setting(
        'plantsmag_accent_color',
        array(
            'default' => '#C4A35A',
            'sanitize_callback' => 'sanitize_hex_color',
            'transport' => 'postMessage',
        )
    );

    $wp_customize->add_control(
        new WP_Customize_Color_Control(
            $wp_customize,
            'plantsmag_accent_color',
            array(
                'label' => __('Accent Color', 'plantsmag'),
                'section' => 'plantsmag_colors',
            )
        )
    );

    // ========================================
    // Header Section
    // ========================================
    $wp_customize->add_section(
        'plantsmag_header',
        array(
            'title' => __('Header Settings', 'plantsmag'),
            'panel' => 'plantsmag_theme_options',
            'priority' => 20,
        )
    );

    // Sticky Header
    $wp_customize->add_setting(
        'plantsmag_sticky_header',
        array(
            'default' => true,
            'sanitize_callback' => 'plantsmag_sanitize_checkbox',
        )
    );

    $wp_customize->add_control(
        'plantsmag_sticky_header',
        array(
            'label' => __('Enable Sticky Header', 'plantsmag'),
            'section' => 'plantsmag_header',
            'type' => 'checkbox',
        )
    );

    // Header CTA Text
    $wp_customize->add_setting(
        'plantsmag_header_cta_text',
        array(
            'default' => __('Get Started', 'plantsmag'),
            'sanitize_callback' => 'sanitize_text_field',
        )
    );

    $wp_customize->add_control(
        'plantsmag_header_cta_text',
        array(
            'label' => __('Header CTA Button Text', 'plantsmag'),
            'section' => 'plantsmag_header',
            'type' => 'text',
        )
    );

    // Header CTA Link
    $wp_customize->add_setting(
        'plantsmag_header_cta_link',
        array(
            'default' => '#',
            'sanitize_callback' => 'esc_url_raw',
        )
    );

    $wp_customize->add_control(
        'plantsmag_header_cta_link',
        array(
            'label' => __('Header CTA Button Link', 'plantsmag'),
            'section' => 'plantsmag_header',
            'type' => 'url',
        )
    );

    // ========================================
    // Footer Section
    // ========================================
    $wp_customize->add_section(
        'plantsmag_footer',
        array(
            'title' => __('Footer Settings', 'plantsmag'),
            'panel' => 'plantsmag_theme_options',
            'priority' => 30,
        )
    );

    // Copyright Text
    $wp_customize->add_setting(
        'plantsmag_copyright_text',
        array(
            'default' => '',
            'sanitize_callback' => 'wp_kses_post',
        )
    );

    $wp_customize->add_control(
        'plantsmag_copyright_text',
        array(
            'label' => __('Copyright Text', 'plantsmag'),
            'description' => __('Leave empty to use default copyright text.', 'plantsmag'),
            'section' => 'plantsmag_footer',
            'type' => 'textarea',
        )
    );

    // ========================================
    // Social Media Section
    // ========================================
    $wp_customize->add_section(
        'plantsmag_social',
        array(
            'title' => __('Social Media', 'plantsmag'),
            'panel' => 'plantsmag_theme_options',
            'priority' => 40,
        )
    );

    $social_networks = array(
        'facebook' => __('Facebook URL', 'plantsmag'),
        'twitter' => __('Twitter/X URL', 'plantsmag'),
        'instagram' => __('Instagram URL', 'plantsmag'),
        'linkedin' => __('LinkedIn URL', 'plantsmag'),
        'youtube' => __('YouTube URL', 'plantsmag'),
        'pinterest' => __('Pinterest URL', 'plantsmag'),
        'tiktok' => __('TikTok URL', 'plantsmag'),
        'telegram' => __('Telegram URL', 'plantsmag'),
    );

    foreach ($social_networks as $network => $label) {
        $wp_customize->add_setting(
            'plantsmag_social_' . $network,
            array(
                'default' => '',
                'sanitize_callback' => 'esc_url_raw',
            )
        );

        $wp_customize->add_control(
            'plantsmag_social_' . $network,
            array(
                'label' => $label,
                'section' => 'plantsmag_social',
                'type' => 'url',
            )
        );
    }

    // ========================================
    // Homepage Sections
    // ========================================
    $wp_customize->add_section(
        'plantsmag_homepage',
        array(
            'title' => __('Homepage Sections', 'plantsmag'),
            'panel' => 'plantsmag_theme_options',
            'priority' => 50,
            'description' => __('Enable or disable homepage sections.', 'plantsmag'),
        )
    );

    $homepage_sections = array(
        'hero' => __('Hero Section', 'plantsmag'),
        'about' => __('About Section', 'plantsmag'),
        'services' => __('Services Section', 'plantsmag'),
        'portfolio' => __('Portfolio Section', 'plantsmag'),
        'testimonials' => __('Testimonials Section', 'plantsmag'),
        'blog' => __('Blog Section', 'plantsmag'),
        'newsletter' => __('Newsletter Section', 'plantsmag'),
        'cta' => __('Call to Action Section', 'plantsmag'),
    );

    foreach ($homepage_sections as $section => $label) {
        $wp_customize->add_setting(
            'plantsmag_show_' . $section,
            array(
                'default' => true,
                'sanitize_callback' => 'plantsmag_sanitize_checkbox',
            )
        );

        $wp_customize->add_control(
            'plantsmag_show_' . $section,
            array(
                'label' => sprintf(__('Show %s', 'plantsmag'), $label),
                'section' => 'plantsmag_homepage',
                'type' => 'checkbox',
            )
        );
    }

    // ========================================
    // Hero Section Settings
    // ========================================
    $wp_customize->add_section(
        'plantsmag_hero_section',
        array(
            'title' => __('Hero Section', 'plantsmag'),
            'panel' => 'plantsmag_theme_options',
            'priority' => 55,
        )
    );

    // Hero Title
    $wp_customize->add_setting(
        'plantsmag_hero_title',
        array(
            'default' => __('Your Garden Your Passion', 'plantsmag'),
            'sanitize_callback' => 'sanitize_text_field',
        )
    );

    $wp_customize->add_control(
        'plantsmag_hero_title',
        array(
            'label' => __('Hero Title', 'plantsmag'),
            'section' => 'plantsmag_hero_section',
            'type' => 'text',
        )
    );

    // Hero Subtitle
    $wp_customize->add_setting(
        'plantsmag_hero_subtitle',
        array(
            'default' => __('Whether you\'re dreaming of a lush, verdant paradise or a sleek, modern outdoor retreat, we\'ll work closely with you to bring your vision to life.', 'plantsmag'),
            'sanitize_callback' => 'sanitize_textarea_field',
        )
    );

    $wp_customize->add_control(
        'plantsmag_hero_subtitle',
        array(
            'label' => __('Hero Subtitle', 'plantsmag'),
            'section' => 'plantsmag_hero_section',
            'type' => 'textarea',
        )
    );

    // Hero Background Image
    $wp_customize->add_setting(
        'plantsmag_hero_bg',
        array(
            'default' => '',
            'sanitize_callback' => 'esc_url_raw',
        )
    );

    $wp_customize->add_control(
        new WP_Customize_Image_Control(
            $wp_customize,
            'plantsmag_hero_bg',
            array(
                'label' => __('Hero Background Image', 'plantsmag'),
                'section' => 'plantsmag_hero_section',
            )
        )
    );

    // Hero CTA Text
    $wp_customize->add_setting(
        'plantsmag_hero_cta_text',
        array(
            'default' => __('Read More', 'plantsmag'),
            'sanitize_callback' => 'sanitize_text_field',
        )
    );

    $wp_customize->add_control(
        'plantsmag_hero_cta_text',
        array(
            'label' => __('CTA Button Text', 'plantsmag'),
            'section' => 'plantsmag_hero_section',
            'type' => 'text',
        )
    );

    // Hero CTA Link
    $wp_customize->add_setting(
        'plantsmag_hero_cta_link',
        array(
            'default' => '#about',
            'sanitize_callback' => 'esc_url_raw',
        )
    );

    $wp_customize->add_control(
        'plantsmag_hero_cta_link',
        array(
            'label' => __('CTA Button Link', 'plantsmag'),
            'section' => 'plantsmag_hero_section',
            'type' => 'url',
        )
    );
}
add_action('customize_register', 'plantsmag_customize_register');

/**
 * Sanitize Checkbox
 */
function plantsmag_sanitize_checkbox($value)
{
    return (isset($value) && true === $value) ? true : false;
}

/**
 * Output Custom CSS
 */
function plantsmag_customizer_css()
{
    $primary_color = get_theme_mod('plantsmag_primary_color', '#2D4A3E');
    $accent_color = get_theme_mod('plantsmag_accent_color', '#C4A35A');

    if ($primary_color !== '#2D4A3E' || $accent_color !== '#C4A35A') {
        $css = ':root {';
        if ($primary_color !== '#2D4A3E') {
            $css .= '--pm-primary: ' . esc_attr($primary_color) . ';';
        }
        if ($accent_color !== '#C4A35A') {
            $css .= '--pm-accent: ' . esc_attr($accent_color) . ';';
        }
        $css .= '}';

        wp_add_inline_style('plantsmag-style', $css);
    }
}
add_action('wp_enqueue_scripts', 'plantsmag_customizer_css', 20);

/**
 * Customizer Preview JS
 */
function plantsmag_customize_preview_js()
{
    wp_enqueue_script(
        'plantsmag-customizer-preview',
        PLANTSMAG_URI . '/assets/js/customizer-preview.js',
        array('customize-preview'),
        PLANTSMAG_VERSION,
        true
    );
}
add_action('customize_preview_init', 'plantsmag_customize_preview_js');
