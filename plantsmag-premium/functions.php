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
	wp_enqueue_style( 'plantsmag-premium-style', get_stylesheet_uri(), array(), time() );

    // ── Phase 2: Lead Magnet CSS ──────────────────────────────
    wp_enqueue_style(
        'pm-lead-magnet',
        get_template_directory_uri() . '/assets/css/lead-magnet.css',
        array( 'plantsmag-premium-style' ),
        '1.0.0'
    );
}
add_action( 'wp_enqueue_scripts', 'plantsmag_premium_scripts' );

// ── Phase 2: Load Lead Capture REST API ───────────────────────
require_once get_template_directory() . '/inc/lead-capture.php';

/**
 * 🔴 Title Override — Force "PlantsMag" in all browser tab titles
 * WP blogname may be incorrectly set to "Your Smart Indoor Jungle Starts Here".
 * This ensures Google always indexes the correct brand name in <title> tags.
 */
function plantsmag_force_title( $title_parts ) {
    $title_parts['site'] = 'PlantsMag';
    return $title_parts;
}
add_filter( 'document_title_parts', 'plantsmag_force_title', 99 );
add_filter( 'document_title_separator', function() { return '—'; }, 99 );


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
 * 🚀 Mobile Navigation Support
 * Hamburger menu toggle via JS
 */
function plantsmag_enqueue_nav_script() {
    wp_add_inline_script( 'plantsmag-premium-style', '' ); // Ensure style is loaded first
}
add_action( 'wp_enqueue_scripts', 'plantsmag_enqueue_nav_script' );

// NOTE: Tool classes are loaded by the plantsmag-tools Plugin only.
// DO NOT require them here to avoid Fatal Error (duplicate class definition).


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

/**
 * 🚀 Native Metadata & Open Graph SEO Engine (No Plugins Needed)
 * Enhanced with AI Search Visibility (Gemini, ChatGPT, Perplexity)
 */
function plantsmag_dynamic_seo_meta_tags() {
    global $post;
    
    // Canonical URL
    if ( is_singular() ) {
        echo '<link rel="canonical" href="' . esc_url( get_permalink() ) . '" />' . "\n";
    } elseif ( is_front_page() || is_home() ) {
        echo '<link rel="canonical" href="' . esc_url( home_url( '/' ) ) . '" />' . "\n";
    }

    if ( is_front_page() || is_home() ) {
        // Homepage meta
        $home_desc = 'PlantsMag — Expert plant care guides, AI-powered disease diagnosis, and evidence-based watering schedules for 200+ houseplant species.';
        echo '<meta name="description" content="' . esc_attr($home_desc) . '" />' . "\n";
        echo '<meta property="og:title" content="PlantsMag — Expert Plant Care & Disease Diagnosis" />' . "\n";
        echo '<meta property="og:description" content="' . esc_attr($home_desc) . '" />' . "\n";
        echo '<meta property="og:type" content="website" />' . "\n";
        echo '<meta property="og:url" content="' . esc_url( home_url('/') ) . '" />' . "\n";
        echo '<meta property="og:site_name" content="PlantsMag" />' . "\n";
    } elseif ( is_single() || is_page() ) {
        // Default Site Info
        $site_name = get_bloginfo('name');
        
        // Generate Description
        $excerpt = $post->post_excerpt;
        if ( empty(trim($excerpt)) ) {
            $excerpt = wp_trim_words( strip_shortcodes( strip_tags( $post->post_content ) ), 35, '' );
        }
        if ( empty(trim($excerpt)) ) {
            $excerpt = 'Read the complete guide on ' . get_the_title() . ' at PlantsMag. We provide expert care tips, watering schedules, and disease prevention.';
        }
        $description = esc_attr( wp_strip_all_tags( $excerpt ) );
        echo '<meta name="description" content="' . $description . '" />' . "\n";
        
        // Open Graph — enhanced for social sharing + AI crawlers
        echo '<meta property="og:title" content="' . esc_attr( get_the_title() ) . '" />' . "\n";
        echo '<meta property="og:description" content="' . $description . '" />' . "\n";
        echo '<meta property="og:type" content="article" />' . "\n";
        echo '<meta property="og:url" content="' . esc_url( get_permalink() ) . '" />' . "\n";
        echo '<meta property="og:site_name" content="' . esc_attr( $site_name ) . '" />' . "\n";
        echo '<meta property="article:published_time" content="' . esc_attr( get_the_date('c') ) . '" />' . "\n";
        echo '<meta property="article:modified_time" content="' . esc_attr( get_the_modified_date('c') ) . '" />' . "\n";
        echo '<meta property="article:author" content="PlantsMag Editorial Team" />' . "\n";
        
        if ( has_post_thumbnail() ) {
            $thumbnail_src = wp_get_attachment_image_src( get_post_thumbnail_id( $post->ID ), 'large' );
            if ($thumbnail_src) {
                echo '<meta property="og:image" content="' . esc_url( $thumbnail_src[0] ) . '" />' . "\n";
                echo '<meta property="og:image:width" content="' . esc_attr($thumbnail_src[1]) . '" />' . "\n";
                echo '<meta property="og:image:height" content="' . esc_attr($thumbnail_src[2]) . '" />' . "\n";
                echo '<meta name="twitter:card" content="summary_large_image" />' . "\n";
                echo '<meta name="twitter:image" content="' . esc_url( $thumbnail_src[0] ) . '" />' . "\n";
            }
        }
        
        // Twitter / X optimization
        echo '<meta name="twitter:title" content="' . esc_attr( get_the_title() ) . '" />' . "\n";
        echo '<meta name="twitter:description" content="' . $description . '" />' . "\n";
        echo '<meta name="twitter:site" content="@plantsmag" />' . "\n";
        
    }
    
    // 🌐 Hreflang Tags for International Targeting (US primary, UAE secondary)
    $current_url = home_url( $_SERVER['REQUEST_URI'] );
    $current_url = strtok($current_url, '?'); // Clean query strings
    
    echo '<link rel="alternate" hreflang="en-US" href="' . esc_url( $current_url ) . '" />' . "\n";
    echo '<link rel="alternate" hreflang="en-AE" href="' . esc_url( $current_url ) . '" />' . "\n";
    echo '<link rel="alternate" hreflang="x-default" href="' . esc_url( $current_url ) . '" />' . "\n";
    
    // 🤖 AI Crawler hints
    echo '<link rel="author" href="' . esc_url( home_url('/about/') ) . '" />' . "\n";

    // 🛑 Noindex for feeds, categories, and paginated pages
    if ( is_feed() || is_category() || is_paged() ) {
        echo '<meta name="robots" content="noindex, follow" />' . "\n";
    }
}
add_action( 'wp_head', 'plantsmag_dynamic_seo_meta_tags', 1 );

/**
 * 🌐 Organization + WebSite Schema (AI Search Visibility)
 * Makes PlantsMag appear in Gemini, ChatGPT, and Perplexity knowledge graphs.
 * WebSite schema with SearchAction allows Google to show sitelinks search box.
 */
function plantsmag_organization_schema() {
    // Only on homepage
    if ( ! is_front_page() && ! is_home() ) return;
    
    $schema = [
        '@context' => 'https://schema.org',
        '@graph'   => [
            [
                '@type'       => 'Organization',
                '@id'         => home_url('/#organization'),
                'name'        => 'PlantsMag',
                'url'         => home_url('/'),
                'logo'        => [
                    '@type' => 'ImageObject',
                    'url'   => home_url('/wp-content/uploads/logo.png'),
                ],
                'description' => 'Expert plant care authority providing AI-powered disease diagnosis, watering calculators, and evidence-based guides for 200+ plant species.',
                'sameAs'      => [
                    'https://www.pinterest.com/plantsmag',
                    'https://www.instagram.com/plantsmag',
                ],
                'areaServed'  => ['US', 'AE', 'GB', 'CA', 'AU'],
                'knowsAbout'  => [
                    'Plant care', 'Plant disease diagnosis', 'Houseplant watering',
                    'Tropical plants', 'Succulent care', 'Orchid care',
                    'Plant propagation', 'Soil and fertilizer for plants',
                ],
            ],
            [
                '@type'            => 'WebSite',
                '@id'              => home_url('/#website'),
                'name'             => 'PlantsMag',
                'url'              => home_url('/'),
                'publisher'        => ['@id' => home_url('/#organization')],
                'inLanguage'       => 'en-US',
                'potentialAction'  => [
                    '@type'       => 'SearchAction',
                    'target'      => [
                        '@type'       => 'EntryPoint',
                        'urlTemplate' => home_url('/?s={search_term_string}'),
                    ],
                    'query-input' => 'required name=search_term_string',
                ],
            ],
        ],
    ];
    
    echo '<script type="application/ld+json">'
        . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE)
        . '</script>' . "\n";
}
add_action('wp_head', 'plantsmag_organization_schema', 2);

/**
 * 🤖 Speakable Schema — Makes Content Readable by Google Assistant & AI
 * Google uses this to identify which article sections are suitable for
 * text-to-speech and AI assistant summaries (key for Gemini visibility).
 */
function plantsmag_speakable_schema() {
    if ( ! is_single() ) return;
    
    global $post;
    
    // Mark the article headline and first section as speakable
    $schema = [
        '@context'  => 'https://schema.org',
        '@type'     => 'Article',
        '@id'       => get_permalink() . '#article',
        'headline'  => get_the_title(),
        'speakable' => [
            '@type'   => 'SpeakableSpecification',
            'cssSelector' => ['.entry-title', '.entry-content p:first-of-type', 'h2:first-of-type'],
        ],
        'url'       => get_permalink(),
        'author'    => [
            '@type' => 'Person',
            'name'  => 'PlantsMag Editorial Team',
            'url'   => home_url('/about/'),
            'jobTitle' => 'Plant Care Specialist',
            'knowsAbout' => ['Plant care', 'Houseplants', 'Plant diseases', 'Horticulture'],
        ],
        'publisher' => [
            '@id' => home_url('/#organization'),
        ],
        'datePublished'  => get_the_date('c'),
        'dateModified'   => get_the_modified_date('c'),
        'inLanguage'     => 'en-US',
        'isAccessibleForFree' => true,
    ];
    
    // Add image if available
    if ( has_post_thumbnail() ) {
        $img = wp_get_attachment_image_src( get_post_thumbnail_id( $post->ID ), 'large' );
        if ($img) {
            $schema['image'] = [
                '@type'  => 'ImageObject',
                'url'    => $img[0],
                'width'  => $img[1],
                'height' => $img[2],
            ];
        }
    }
    
    echo '<script type="application/ld+json">'
        . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE)
        . '</script>' . "\n";
}
add_action('wp_head', 'plantsmag_speakable_schema', 3);



/**
 * 🚀 High-Performance Pagination & Archive Grid
 */
function plantsmag_archive_posts_per_page( $query ) {
    if ( ! is_admin() && $query->is_main_query() && ( is_archive() || is_home() || is_search() ) ) {
        $query->set( 'posts_per_page', 24 ); // Massive grid for fast crawling
    }
}
add_action( 'pre_get_posts', 'plantsmag_archive_posts_per_page' );

/**
 * 🚀 Native Breadcrumbs & Schema.org JSON-LD
 */
function plantsmag_breadcrumbs() {
    if ( is_front_page() ) return;
    
    global $post;
    
    $crumbs = array();
    $crumbs[] = array(
        'name' => 'Home',
        'url'  => home_url( '/' )
    );

    if ( is_category() || is_single() ) {
        $category = get_the_category();
        if ( ! empty( $category ) ) {
            $crumbs[] = array(
                'name' => $category[0]->name,
                'url'  => get_category_link( $category[0]->term_id )
            );
        }
    }
    
    if ( is_single() ) {
        $crumbs[] = array(
            'name' => get_the_title(),
            'url'  => get_permalink()
        );
    } elseif ( is_page() ) {
        $crumbs[] = array(
            'name' => get_the_title(),
            'url'  => get_permalink()
        );
    } elseif ( is_archive() && ! is_category() ) {
        $crumbs[] = array(
            'name' => get_the_archive_title(),
            'url'  => ''
        );
    }
    
    // 1. Generate Schema.org JSON-LD
    $schema_items = array();
    $position = 1;
    foreach ( $crumbs as $crumb ) {
        $crumb_name = empty( $crumb['name'] ) ? ucwords( str_replace( '-', ' ', trim( parse_url( $crumb['url'], PHP_URL_PATH ), '/' ) ) ) : $crumb['name'];
        if ( empty( $crumb_name ) ) $crumb_name = 'Page';
        
        $item = array(
            '@type'    => 'ListItem',
            'position' => $position,
            'name'     => $crumb_name
        );
        if ( ! empty( $crumb['url'] ) ) {
            $item['item'] = $crumb['url'];
        }
        $schema_items[] = $item;
        $position++;
    }
    
    $schema = array(
        '@context'        => 'https://schema.org',
        '@type'           => 'BreadcrumbList',
        'itemListElement' => $schema_items
    );
    
    // Inject JSON-LD into the head
    add_action( 'wp_head', function() use ( $schema ) {
        echo '<script type="application/ld+json">' . wp_json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . '</script>' . "\n";
    });

    // 2. Output HTML Breadcrumbs
    echo '<nav class="plantsmag-breadcrumbs" aria-label="breadcrumb">';
    echo '<ol itemscope itemtype="https://schema.org/BreadcrumbList">';
    
    $pos = 1;
    $total = count($crumbs);
    foreach ( $crumbs as $crumb ) {
        $crumb_name = empty( $crumb['name'] ) ? ucwords( str_replace( '-', ' ', trim( parse_url( $crumb['url'], PHP_URL_PATH ), '/' ) ) ) : $crumb['name'];
        if ( empty( $crumb_name ) ) $crumb_name = 'Page';
        
        echo '<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">';
        if ( ! empty( $crumb['url'] ) && $pos < $total ) {
            echo '<a itemprop="item" href="' . esc_url( $crumb['url'] ) . '"><span itemprop="name">' . esc_html( $crumb_name ) . '</span></a>';
        } else {
            echo '<span itemprop="name" class="breadcrumb-active" aria-current="page">' . esc_html( $crumb_name ) . '</span>';
        }
        echo '<meta itemprop="position" content="' . $pos . '" />';
        echo '</li>';
        
        if ( $pos < $total ) {
            echo '<li class="breadcrumb-separator"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></li>';
        }
        $pos++;
    }
    
    echo '</ol>';
    echo '</nav>';
}

/**
 * Helper: Calculate reading time
 */
if (!function_exists('reading_time')) {
    function reading_time() {
        $content = get_post_field( 'post_content', get_the_ID() );
        $word_count = str_word_count( strip_tags( $content ) );
        $readingtime = ceil($word_count / 200);
        return $readingtime;
    }
}

/**
 * 🚀 Schema.org JSON-LD for BlogPosting
 */
function plantsmag_add_json_ld_schema() {
    if ( is_single() ) {
        global $post;
        $schema = array(
            "@context" => "https://schema.org",
            "@type" => "BlogPosting",
            "headline" => get_the_title(),
            "image" => get_the_post_thumbnail_url(),
            "author" => array(
                "@type" => "Person",
                "name" => get_the_author()
            ),
            "datePublished" => get_the_date('c'),
            "dateModified" => get_the_modified_date('c')
        );
        echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";
    }
}
add_action('wp_head', 'plantsmag_add_json_ld_schema');

/**
 * 🚀 FAQ Schema JSON-LD — Generates Rich Snippets in Google (CTR Boost)
 * Extracts H2 headings and their following paragraph as Q&A pairs.
 * This makes Google show expandable FAQ dropdowns in search results → MORE CLICKS.
 */
function plantsmag_add_faq_schema() {
    if ( ! is_single() ) return;

    global $post;
    $content = $post->post_content;

    // Extract H2 headings and following paragraph text
    // Pattern: <h2>Question</h2> followed by <p>Answer</p>
    preg_match_all(
        '/<h2[^>]*>(.*?)<\/h2>\s*(?:<[^>]+>)*\s*<p[^>]*>(.*?)<\/p>/is',
        $content,
        $matches,
        PREG_SET_ORDER
    );

    if ( empty($matches) ) return;

    // Limit to first 5 Q&A pairs (Google shows max 5)
    $faq_items = [];
    $count = 0;
    foreach ( $matches as $match ) {
        $question = wp_strip_all_tags( $match[1] );
        $answer   = wp_strip_all_tags( $match[2] );

        // Skip very short or generic headings
        if ( strlen($question) < 10 || strlen($answer) < 20 ) continue;

        // Clean up
        $question = trim( html_entity_decode($question) );
        $answer   = trim( html_entity_decode($answer) );

        // Truncate answer to 250 chars for schema
        if ( strlen($answer) > 250 ) {
            $answer = substr($answer, 0, 247) . '...';
        }

        $faq_items[] = [
            '@type'          => 'Question',
            'name'           => $question,
            'acceptedAnswer' => [
                '@type' => 'Answer',
                'text'  => $answer,
            ],
        ];

        $count++;
        if ( $count >= 5 ) break;
    }

    if ( empty($faq_items) ) return;

    $schema = [
        '@context'   => 'https://schema.org',
        '@type'      => 'FAQPage',
        'mainEntity' => $faq_items,
    ];

    echo '<script type="application/ld+json">'
        . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE)
        . '</script>' . "\n";
}
add_action('wp_head', 'plantsmag_add_faq_schema', 5);

/**
 * 🚀 Handle Deleted Product Redirects (Fixing 404s)
 */
function plantsmag_deleted_product_redirects() {
    $redirects = array(
        '/product/sansevieria-golden-flame/' => '/',
        '/zz-plant-care-guide-beginners-2/' => '/zz-plant-care-guide-beginners/'
    );

    $current_url = $_SERVER['REQUEST_URI'];
    
    // Strip query string for exact matching if necessary
    $path = parse_url($current_url, PHP_URL_PATH);

    if ( array_key_exists( $path, $redirects ) ) {
        wp_redirect( home_url( $redirects[$path] ), 301 );
        exit;
    }
}
add_action( 'template_redirect', 'plantsmag_deleted_product_redirects' );

/**
 * 🚀 Fix N8N Bot Rendering Bugs (Raw CSS & Duplicate Title)
 */
function plantsmag_fix_bot_content_bugs( $content ) {
    if ( ! is_single() ) {
        return $content;
    }
    
    // 1. Remove raw CSS injected by bot that WordPress stripped <style> tags from
    $css_to_remove = array(
        '.pm-affiliate-box h3 { margin-top: 0; color: #2e8b57; }',
        '.pm-affiliate-box h3 {margin-top: 0; color: #2e8b57;}',
        '.cta-button { display: inline-block; padding: 12px 25px; background-color: #ff9900; /* Amazon Orange */ color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 5px; text-align: center; margin-top: 15px; transition: background-color 0.3s ease; }',
        '.cta-button:hover { background-color: #e68a00; }'
    );
    $content = str_replace( $css_to_remove, '', $content );
    
    // Fallback regex to clean up any remaining weird CSS chunks related to affiliate box
    $content = preg_replace('/\.pm-affiliate-box\s*\{[^}]+\}/is', '', $content);
    $content = preg_replace('/\.pm-affiliate-box\s*h3\s*\{[^}]+\}/is', '', $content);
    $content = preg_replace('/\.cta-button\s*\{[^}]+\}/is', '', $content);
    $content = preg_replace('/\.cta-button:hover\s*\{[^}]+\}/is', '', $content);
    
    // 2. Remove duplicate H1 tag at the beginning of the content if it matches the title
    // The theme already outputs the H1 title in content-single.php
    $post_title = get_the_title();
    // Pattern matches <h1>Title</h1> or <h1 class="...">Title</h1> at the start of content
    $pattern = '/^\s*(?:<p>)?\s*<h1[^>]*>\s*' . preg_quote( $post_title, '/' ) . '\s*<\/h1>\s*(?:<\/p>)?\s*/isu';
    $content = preg_replace( $pattern, '', $content );
    
    // General H1 removal: remove ANY h1 in the post content since the theme handles the H1
    $content = preg_replace('/<h1[^>]*>.*?<\/h1>/isu', '', $content);

    return $content;
}
add_filter( 'the_content', 'plantsmag_fix_bot_content_bugs', 99 );

/**
 * 🚀 Fix RankMath "Unnamed item" Breadcrumb & Empty Titles
 * Ensures Pages without titles don't break Google Search Console schemas.
 */
add_filter( 'rank_math/frontend/breadcrumb/items', function( $crumbs, $class ) {
    foreach ( $crumbs as &$crumb ) {
        // If the breadcrumb name is empty
        if ( empty( $crumb[0] ) || trim( $crumb[0] ) === '' ) {
            if ( ! empty( $crumb[1] ) ) {
                $path = parse_url( $crumb[1], PHP_URL_PATH );
                $slug = trim( $path, '/' );
                $slug = str_replace( '-', ' ', $slug );
                $crumb[0] = ucwords( $slug );
            } else {
                $crumb[0] = 'Page';
            }
        }
    }
    return $crumbs;
}, 10, 2 );

add_filter( 'rank_math/frontend/title', function( $title ) {
    if ( empty( trim( str_replace( array( '-', 'Your Smart Indoor Jungle Starts Here', 'PlantsMag' ), '', $title ) ) ) ) {
        // If the title is just the separator and site name, inject a proper name
        global $post;
        if ( $post && $post->post_name ) {
            $slug_title = ucwords( str_replace( '-', ' ', $post->post_name ) );
            return $slug_title . ' — PlantsMag';
        }
    }
    // Also enforce "PlantsMag" branding instead of "Your Smart Indoor Jungle Starts Here"
    $title = str_replace( 'Your Smart Indoor Jungle Starts Here', 'PlantsMag', $title );
    return $title;
} );




/**
 * 🚀 Instant Indexing (IndexNow) on Post Publish
 * Automatically notify Bing, Yandex (via IndexNow) and Google (via Sitemap Ping)
 */
function plantsmag_instant_indexing_on_publish( $new_status, $old_status, $post ) {
    if ( 'publish' !== $new_status || 'publish' === $old_status || 'post' !== $post->post_type ) {
        return;
    }

    $post_url = get_permalink( $post->ID );
    $host_name = parse_url( home_url(), PHP_URL_HOST );
    $key = 'plantsmag-indexnow-key-2026';
    
    $payload = array(
        'host' => $host_name,
        'key'  => $key,
        'keyLocation' => home_url( '/' . $key . '.txt' ),
        'urlList' => array( $post_url )
    );
    
    $args = array(
        'body'        => wp_json_encode( $payload ),
        'headers'     => array( 'Content-Type' => 'application/json; charset=utf-8' ),
        'data_format' => 'body',
        'timeout'     => 10,
        'blocking'    => false, // Non-blocking
    );
    
    // Ping IndexNow
    wp_remote_post( 'https://api.indexnow.org/indexnow', $args );
    wp_remote_post( 'https://www.bing.com/indexnow', $args );
    
    // Ping Google Sitemap
    $sitemap_url = home_url( '/sitemap_index.xml' );
    wp_remote_get( 'https://www.google.com/ping?sitemap=' . urlencode( $sitemap_url ), array( 'blocking' => false ) );
}
add_action( 'transition_post_status', 'plantsmag_instant_indexing_on_publish', 10, 3 );

/**
 * Virtual Endpoint for IndexNow Key verification
 */
function plantsmag_indexnow_key_endpoint() {
    $request_uri = $_SERVER['REQUEST_URI'];
    $key = 'plantsmag-indexnow-key-2026';
    if ( strpos( $request_uri, '/' . $key . '.txt' ) !== false ) {
        header( 'Content-Type: text/plain' );
        echo $key;
        exit;
    }
}
add_action( 'init', 'plantsmag_indexnow_key_endpoint' );
