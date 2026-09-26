<?php
/**
 * PlantsMag Premium Functions
 *
 * @package PlantsMag_Premium
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}

/**
 * Theme Setup
 */
function plantsmag_premium_setup() {
	// Add default posts and comments RSS feed links to head.
	add_theme_support( 'automatic-feed-links' );

	// Let WordPress manage the document title.
	add_theme_support( 'title-tag' );

	// Enable support for Post Thumbnails on posts and pages.
	add_theme_support( 'post-thumbnails' );

	// Register Navigation Menus
	register_nav_menus(
		array(
			'primary' => esc_html__( 'Primary Menu', 'plantsmag-premium' ),
			'footer'  => esc_html__( 'Footer Menu', 'plantsmag-premium' ),
		)
	);

	// HTML5 Support
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

	// Add theme support for selective refresh for widgets.
	add_theme_support( 'customize-selective-refresh-widgets' );

	// Add support for core custom logo.
	add_theme_support(
		'custom-logo',
		array(
			'height'      => 80,
			'width'       => 250,
			'flex-width'  => true,
			'flex-height' => true,
		)
	);
}
add_action( 'after_setup_theme', 'plantsmag_premium_setup' );

/**
 * Enqueue scripts and styles.
 */
function plantsmag_premium_scripts() {
	wp_enqueue_style( 'plantsmag-premium-style', get_stylesheet_uri(), array(), wp_get_theme()->get('Version') );
    
    // De-register block library css if you want an ultra light theme, 
    // but we'll leave it in case they use gutenberg tools
	// wp_dequeue_style( 'wp-block-library' );
	// wp_dequeue_style( 'wp-block-library-theme' );
}
add_action( 'wp_enqueue_scripts', 'plantsmag_premium_scripts' );

/**
 * Register widget area.
 */
function plantsmag_premium_widgets_init() {
	register_sidebar(
		array(
			'name'          => esc_html__( 'Footer 1', 'plantsmag-premium' ),
			'id'            => 'footer-1',
			'description'   => esc_html__( 'Add widgets here.', 'plantsmag-premium' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="footer-widget-title">',
			'after_title'   => '</h2>',
		)
	);
    register_sidebar(
		array(
			'name'          => esc_html__( 'Footer 2', 'plantsmag-premium' ),
			'id'            => 'footer-2',
			'description'   => esc_html__( 'Add widgets here.', 'plantsmag-premium' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="footer-widget-title">',
			'after_title'   => '</h2>',
		)
	);
}
add_action( 'widgets_init', 'plantsmag_premium_widgets_init' );

/**
 * Remove WordPress Version Number for Security and SEO
 */
remove_action('wp_head', 'wp_generator');
add_filter('the_generator', '__return_empty_string');

/**
 * 🚀 Advanced SEO & Performance Rizehkari
 */

// Disable Emojis (Saves HTTP requests)
function plantsmag_disable_emojis() {
    remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
    remove_action( 'admin_print_scripts', 'print_emoji_detection_script' );
    remove_action( 'wp_print_styles', 'print_emoji_styles' );
    remove_action( 'admin_print_styles', 'print_emoji_styles' ); 
    remove_filter( 'the_content_feed', 'wp_staticize_emoji' );
    remove_filter( 'comment_text_rss', 'wp_staticize_emoji' ); 
    remove_filter( 'wp_mail', 'wp_staticize_emoji_for_email' );
}
add_action( 'init', 'plantsmag_disable_emojis' );

// Remove XML-RPC (Security & Performance)
add_filter('xmlrpc_enabled', '__return_false');

// Remove extra REST API links from head
remove_action('wp_head', 'rest_output_link_wp_head', 10);
remove_action('wp_head', 'wp_oembed_add_discovery_links', 10);
remove_action('template_redirect', 'rest_output_link_header', 11, 0);

// Add RankMath Breadcrumb Support internally
add_theme_support( 'rank-math-breadcrumbs' );

/**
 * 🚀 Native Integration of Premium Tools
 * Bypassing clunky plugins for 10/10 Speed
 */
require_once get_template_directory() . '/inc/class-watering-calculator.php';
require_once get_template_directory() . '/inc/class-disease-finder.php';

// Add native-like generic fonts for tools directly
function plantsmag_tools_enqueue_global_scripts() {
    wp_enqueue_style('plantsmag-fonts-tools', 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap', array(), null);
}
add_action( 'wp_enqueue_scripts', 'plantsmag_tools_enqueue_global_scripts' );


/**
 * 🛡️ 10/10 Security & Speed Headers
 */
function plantsmag_security_headers() {
    if ( ! is_admin() ) {
        header( 'X-Content-Type-Options: nosniff' );
        header( 'X-Frame-Options: SAMEORIGIN' );
        header( 'X-XSS-Protection: 1; mode=block' );
        header( 'Strict-Transport-Security: max-age=31536000; includeSubDomains' );
    }
}
add_action( 'send_headers', 'plantsmag_security_headers' );

// Force defer on non-essential scripts for 10/10 Speed
function plantsmag_defer_scripts( $tag, $handle, $src ) {
    // Exclude core jQuery from defer to prevent breakage of legacy tools
    if ( 'jquery-core' === $handle || 'jquery-migrate' === $handle ) {
        return $tag;
    }
    // Defer everything else
    if ( strpos( $tag, 'defer' ) === false ) {
        return str_replace( ' src', ' defer="defer" src', $tag );
    }
    return $tag;
}
add_filter( 'script_loader_tag', 'plantsmag_defer_scripts', 10, 3 );
