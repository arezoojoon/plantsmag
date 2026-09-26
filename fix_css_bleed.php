<?php
require_once('wp-load.php');
$post_id = 830;
$post = get_post($post_id);
if($post) {
    // WordPress might have converted <style> to &lt;style&gt; or stripped it leaving just the text.
    // Let's get the raw content.
    $content = $post->post_content;
    
    // First, try removing standard <style> tags
    $new_content = preg_replace('/<style\b[^>]*>(.*?)<\/style>/is', '', $content);
    
    // If it was just raw text dumped at the top (e.g. starting with "/* Basic styling")
    $new_content = preg_replace('/\/\* Basic styling for demonstration purposes \*\/(.*?)cta-button:hover \{[^}]+\}/is', '', $new_content);
    
    // Also try to catch it if it was HTML encoded
    $new_content = preg_replace('/&lt;style&gt;(.*?)&lt;\/style&gt;/is', '', $new_content);
    
    // And if it's just floating there
    $new_content = preg_replace('/\/\* Basic styling.*?\}/is', '', $new_content); // This might be too greedy, let's be careful.
    
    $post->post_content = $new_content;
    wp_update_post($post);
    echo "Post updated successfully.\n";
} else {
    echo "Post not found.\n";
}
