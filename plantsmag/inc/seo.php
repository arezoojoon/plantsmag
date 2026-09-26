<?php
/**
 * SEO Functionality
 *
 * @package PlantsMag
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Add SEO Meta Tags
 */
function plantsmag_seo_meta_tags()
{
    // Don't output if Yoast, Rank Math, or AIOSEO is active
    if (defined('WPSEO_VERSION') || defined('RANK_MATH_VERSION') || defined('AIOSEO_VERSION')) {
        return;
    }

    $description = '';
    $title = '';
    $image = '';
    $url = '';

    if (is_singular()) {
        $post = get_queried_object();
        $title = get_the_title();
        $description = has_excerpt() ? get_the_excerpt() : wp_trim_words($post->post_content, 30);
        $url = get_permalink();

        if (has_post_thumbnail()) {
            $image = get_the_post_thumbnail_url(null, 'large');
        }
    } elseif (is_archive()) {
        $title = get_the_archive_title();
        $description = get_the_archive_description();
        $url = get_post_type_archive_link(get_post_type());
    } elseif (is_home()) {
        $title = get_bloginfo('name');
        $description = get_bloginfo('description');
        $url = home_url('/');
    }

    if (empty($description)) {
        $description = get_bloginfo('description');
    }

    $description = wp_strip_all_tags($description);
    $description = str_replace(array("\r", "\n"), ' ', $description);

    // Meta description
    if ($description) {
        echo '<meta name="description" content="' . esc_attr($description) . '">' . "\n";
    }

    // Open Graph
    echo '<meta property="og:locale" content="' . esc_attr(get_locale()) . '">' . "\n";
    echo '<meta property="og:type" content="' . (is_singular() ? 'article' : 'website') . '">' . "\n";

    if ($title) {
        echo '<meta property="og:title" content="' . esc_attr($title) . '">' . "\n";
    }

    if ($description) {
        echo '<meta property="og:description" content="' . esc_attr($description) . '">' . "\n";
    }

    if ($url) {
        echo '<meta property="og:url" content="' . esc_url($url) . '">' . "\n";
    }

    echo '<meta property="og:site_name" content="' . esc_attr(get_bloginfo('name')) . '">' . "\n";

    if ($image) {
        echo '<meta property="og:image" content="' . esc_url($image) . '">' . "\n";
    }

    // Twitter Cards
    echo '<meta name="twitter:card" content="summary_large_image">' . "\n";

    if ($title) {
        echo '<meta name="twitter:title" content="' . esc_attr($title) . '">' . "\n";
    }

    if ($description) {
        echo '<meta name="twitter:description" content="' . esc_attr($description) . '">' . "\n";
    }

    if ($image) {
        echo '<meta name="twitter:image" content="' . esc_url($image) . '">' . "\n";
    }
}
add_action('wp_head', 'plantsmag_seo_meta_tags', 1);

/**
 * Add Schema.org JSON-LD
 */
function plantsmag_schema_markup()
{
    // Don't output if Yoast, Rank Math, or AIOSEO is active
    if (defined('WPSEO_VERSION') || defined('RANK_MATH_VERSION') || defined('AIOSEO_VERSION')) {
        return;
    }

    $schema = array();

    // Organization Schema
    $organization = array(
        '@type' => 'Organization',
        '@id' => home_url('/#organization'),
        'name' => get_bloginfo('name'),
        'url' => home_url('/'),
    );

    if (has_custom_logo()) {
        $logo_id = get_theme_mod('custom_logo');
        $logo_url = wp_get_attachment_image_url($logo_id, 'full');
        if ($logo_url) {
            $organization['logo'] = array(
                '@type' => 'ImageObject',
                'url' => $logo_url,
            );
        }
    }

    // Website Schema
    $website = array(
        '@type' => 'WebSite',
        '@id' => home_url('/#website'),
        'url' => home_url('/'),
        'name' => get_bloginfo('name'),
        'description' => get_bloginfo('description'),
        'publisher' => array('@id' => home_url('/#organization')),
        'potentialAction' => array(
            '@type' => 'SearchAction',
            'target' => home_url('/?s={search_term_string}'),
            'query-input' => 'required name=search_term_string',
        ),
    );

    $schema[] = $organization;
    $schema[] = $website;

    // Single Post/Page Schema
    if (is_singular()) {
        $post = get_queried_object();

        $article = array(
            '@type' => 'Article',
            '@id' => get_permalink() . '#article',
            'isPartOf' => array('@id' => home_url('/#website')),
            'author' => array(
                '@type' => 'Person',
                'name' => get_the_author(),
                'url' => get_author_posts_url(get_the_author_meta('ID')),
            ),
            'headline' => get_the_title(),
            'datePublished' => get_the_date('c'),
            'dateModified' => get_the_modified_date('c'),
            'mainEntityOfPage' => array(
                '@type' => 'WebPage',
                '@id' => get_permalink(),
            ),
            'publisher' => array('@id' => home_url('/#organization')),
        );

        if (has_post_thumbnail()) {
            $article['image'] = get_the_post_thumbnail_url(null, 'large');
        }

        // Plant Guide Schema
        if ('plant_guide' === get_post_type()) {
            $article['@type'] = 'HowTo';
            $article['name'] = get_the_title();
        }

        // Product Review Schema
        if ('product_review' === get_post_type()) {
            $rating = get_post_meta(get_the_ID(), '_review_rating', true);
            $price = get_post_meta(get_the_ID(), '_review_price', true);

            $article['@type'] = 'Review';
            $article['itemReviewed'] = array(
                '@type' => 'Product',
                'name' => get_the_title(),
            );

            if ($rating) {
                $article['reviewRating'] = array(
                    '@type' => 'Rating',
                    'ratingValue' => floatval($rating),
                    'bestRating' => 5,
                );
            }
        }

        $schema[] = $article;
    }

    // Output Schema
    $schema_output = array(
        '@context' => 'https://schema.org',
        '@graph' => $schema,
    );

    echo '<script type="application/ld+json">' . wp_json_encode($schema_output, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";
}
add_action('wp_head', 'plantsmag_schema_markup', 5);

/**
 * Add Canonical URL
 */
function plantsmag_canonical_url()
{
    if (defined('WPSEO_VERSION') || defined('RANK_MATH_VERSION') || defined('AIOSEO_VERSION')) {
        return;
    }

    if (is_singular()) {
        echo '<link rel="canonical" href="' . esc_url(get_permalink()) . '">' . "\n";
    } elseif (is_home() && !is_front_page()) {
        echo '<link rel="canonical" href="' . esc_url(get_permalink(get_option('page_for_posts'))) . '">' . "\n";
    } elseif (is_front_page()) {
        echo '<link rel="canonical" href="' . esc_url(home_url('/')) . '">' . "\n";
    }
}
add_action('wp_head', 'plantsmag_canonical_url', 1);

/**
 * Optimize Title Tag
 */
function plantsmag_document_title_parts($title)
{
    if (is_front_page()) {
        $title['title'] = get_bloginfo('name');
        $title['tagline'] = get_bloginfo('description');
    }

    return $title;
}
add_filter('document_title_parts', 'plantsmag_document_title_parts');

/**
 * Title Separator
 */
function plantsmag_document_title_separator($sep)
{
    return '|';
}
add_filter('document_title_separator', 'plantsmag_document_title_separator');
