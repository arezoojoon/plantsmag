<?php
require_once( dirname(__FILE__) . '/wp-load.php' );

echo "Starting Automated SEO Semantic Interlinking for 10/10 Score...\n";

// Map of Keywords to Target URLs
// We want to link high-value keywords to our tools and pillar pages
$keyword_map = array(
    'watering calculator'    => '/watering-calculator/',
    'watering schedule'      => '/watering-calculator/',
    'when to water'          => '/watering-calculator/',
    'disease finder'         => '/plant-disease-finder/',
    'ai plant doctor'        => '/plant-disease-finder/',
    'fungal disease'         => '/plant-disease-finder/',
    'root rot'               => '/category/diseases/root-rot/',
    'monstera'               => '/category/plants/monstera/',
    'snake plant'            => '/category/plants/snake-plant/',
    'calathea'               => '/category/plants/calathea/',
    'fiddle leaf fig'        => '/category/plants/fiddle-leaf-fig/',
    'indoor jungle'          => '/category/indoor-jungle/'
);

$args = array(
    'posts_per_page' => -1,
    'post_status'    => 'publish',
    'post_type'      => 'post',
);

$query = new WP_Query($args);
$updated_count = 0;
$total_posts = $query->found_posts;

echo "Found $total_posts total posts to scan.\n";

if ( $query->have_posts() ) {
    while ( $query->have_posts() ) {
        $query->the_post();
        $post_id = get_the_ID();
        $content = get_post_field('post_content', $post_id);
        $original_content = $content;

        // Iterate through keyword definitions
        foreach ( $keyword_map as $keyword => $target_url ) {
            // Check if this keyword already has a link pointing to it to prevent nested <a> tags
            // regex checks if keyword exists inside an <a> tag
            $in_a_tag_regex = '/<a[^>]*>(.*?)' . preg_quote($keyword, '/') . '(.*?)<\/a>/vi';
            if ( preg_match($in_a_tag_regex, $content) ) {
                continue; // Skip this keyword for this post, it's already linked
            }

            // Also skip if the post is already linking to that exact URL in general
            if ( strpos($content, $target_url) !== false ) {
                continue; 
            }

            // Replace the *first* occurrence of the keyword that is NOT inside an HTML tag
            // We use a negative lookahead and lookbehind to avoid replacing keywords inside existing HTML tags (like alt="...", href="...")
            $pattern = '/\b(' . preg_quote($keyword, '/') . ')\b(?![^<]*>|[^<>]*<\/a>)/i';
            
            // Only replace 1 limit per keyword per post to avoid spam
            $content = preg_replace($pattern, '<a href="'.esc_attr($target_url).'" class="seo-auto-link" style="color:var(--color-primary-light); font-weight:bold;">$1</a>', $content, 1);
        }

        if ( $content !== $original_content ) {
            $post_update = array(
                'ID'           => $post_id,
                'post_content' => $content
            );
            wp_update_post( $post_update );
            $updated_count++;
            echo "Linked keywords in Post ID: $post_id\n";
        }
    }
    wp_reset_postdata();
    echo "Wiki-Linker Complete. Successfully injected internal links into $updated_count articles.\n";
} else {
    echo "No posts found.\n";
}

// Ensure the permalinks and rewrite rules are flushed for Technical SEO
flush_rewrite_rules(false);
echo "Rewrite Rules Flushed.\n";
?>
