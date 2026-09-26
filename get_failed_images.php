<?php
require_once( dirname(__FILE__) . '/wp-load.php' );
global $wpdb;

$posts = $wpdb->get_results("SELECT ID, post_title FROM {$wpdb->posts} WHERE post_type = 'post' AND post_status = 'publish' ORDER BY ID DESC");

$seen_images = array();
$posts_to_fix = array();

foreach ($posts as $p) {
    $thumb_id = get_post_thumbnail_id($p->ID);
    if (!$thumb_id) continue;
    $url = wp_get_attachment_url($thumb_id);
    if (!$url) continue;
    
    if (isset($seen_images[$url])) {
        $posts_to_fix[] = array('id' => $p->ID, 'title' => $p->post_title);
    } else {
        $seen_images[$url] = true;
    }
}

echo json_encode($posts_to_fix);
?>
