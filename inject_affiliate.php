<?php
$LECHUZA_LINK = "https://amzn.to/4tll8BC";
$QRRICA_LINK = "https://amzn.to/4exPwoG";

$box_a_html = <<<HTML
<div class="pm-affiliate-box" style="border: 2px solid #2ecc71; padding: 20px; border-radius: 8px; margin: 20px 0; background-color: #f9f9f9;">
    <h3 style="margin-top: 0; color: #2ecc71;">🌱 Top Recommended Plant Gear</h3>
    <p>Ensure your plants never dry out. We highly recommend the <strong><a href="$LECHUZA_LINK" target="_blank" rel="nofollow noopener" style="color: #e67e22; font-weight: bold;">LECHUZA Self Watering Plant Pot CLASSICO</a></strong> for ultimate moisture control and professional aesthetic.</p>
    <a href="$LECHUZA_LINK" target="_blank" rel="nofollow noopener" style="display: inline-block; background: #f39c12; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Check Price on Amazon</a>
</div>
HTML;

$box_b_html = <<<HTML
<div class="pm-affiliate-box" style="border: 2px solid #2ecc71; padding: 20px; border-radius: 8px; margin: 20px 0; background-color: #f9f9f9;">
    <h3 style="margin-top: 0; color: #2ecc71;">🌱 Great Value Plant Gear</h3>
    <p>Need multiple pots for your growing collection? We recommend the <strong><a href="$QRRICA_LINK" target="_blank" rel="nofollow noopener" style="color: #e67e22; font-weight: bold;">QRRICA Self Watering Pots (Set of 5)</a></strong>. Excellent value and reliable drainage.</p>
    <a href="$QRRICA_LINK" target="_blank" rel="nofollow noopener" style="display: inline-block; background: #f39c12; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Check Price on Amazon</a>
</div>
HTML;

$posts = array(
    784 => $box_a_html, // Bioactive Terrariums
    782 => $box_a_html, // Tissue Culture
    780 => $box_a_html, // Fungus Gnats
    774 => $box_b_html, // Goth Plants
    772 => $box_b_html, // Ficus Audrey
    770 => $box_b_html  // Hydroponics
);

foreach ($posts as $post_id => $affiliate_html) {
    $post = get_post($post_id);
    if (!$post) {
        WP_CLI::warning("Post $post_id not found.");
        continue;
    }
    
    $content = $post->post_content;
    
    // Regex replace
    $new_content = preg_replace('/<div[^>]*class="pm-affiliate-box"[^>]*>.*?<\/div>/s', $affiliate_html, $content);
    
    if ($new_content === $content || $new_content === null) {
        WP_CLI::log("No pm-affiliate-box found in post $post_id. Appending.");
        $new_content = $content . "\n" . $affiliate_html;
    }
    
    $postarr = array(
        'ID' => $post_id,
        'post_content' => $new_content
    );
    
    wp_update_post($postarr);
    WP_CLI::success("Updated Post $post_id.");
}
?>
