<?php
require_once( dirname(__FILE__) . '/wp-load.php' );
global $wpdb;

echo "Fetching all published posts...\n";
$posts = $wpdb->get_results("SELECT ID, post_title FROM {$wpdb->posts} WHERE post_type = 'post' AND post_status = 'publish' ORDER BY ID DESC");

$seen_titles = array();
$posts_to_delete = array();
$unique_posts = array();

// 1. Find duplicates by title
foreach ($posts as $post) {
    $title = strtolower(trim($post->post_title));
    if (isset($seen_titles[$title])) {
        $posts_to_delete[] = $post->ID;
    } else {
        $seen_titles[$title] = true;
        $unique_posts[] = $post;
    }
}

if (!empty($posts_to_delete)) {
    echo "Deleting " . count($posts_to_delete) . " duplicate articles (same title)...\n";
    foreach ($posts_to_delete as $del_id) {
        wp_delete_post($del_id, true);
    }
    echo "Deleted duplicate articles.\n";
}

// 2. Find shared images
$seen_images = array();
$posts_to_fix_image = array();

echo "Checking for duplicate images among unique posts...\n";
foreach ($unique_posts as $p) {
    $thumb_id = get_post_thumbnail_id($p->ID);
    if (!$thumb_id) {
        continue;
    }
    $url = wp_get_attachment_url($thumb_id);
    if (!$url) {
        continue;
    }
    
    // Check if URL is already used
    if (isset($seen_images[$url])) {
        $posts_to_fix_image[] = $p;
    } else {
        $seen_images[$url] = true;
    }
}

if (empty($posts_to_fix_image)) {
    echo "No duplicate images found!\n";
    exit;
}

echo "Found " . count($posts_to_fix_image) . " distinct posts sharing an image URL. Fixing...\n";

require_once(ABSPATH . 'wp-admin/includes/image.php');
require_once(ABSPATH . 'wp-admin/includes/file.php');
require_once(ABSPATH . 'wp-admin/includes/media.php');

$upload_dir = wp_upload_dir();

foreach ($posts_to_fix_image as $p) {
    echo "Fixing image for post {$p->ID}: {$p->post_title}\n";
    $encoded_title = urlencode($p->post_title . " professional nature plant green minimal --no text watermark logo");
    $seed = rand(100000, 999999);
    $image_url = "https://image.pollinations.ai/prompt/{$encoded_title}?width=1200&height=630&model=flux&nologo=true&seed={$seed}";
    
    $local_img_name = 'img_' . $p->ID . '_' . $seed . '.jpg';
    $target_file = $upload_dir['path'] . '/' . $local_img_name;
    
    echo "Downloading new image: $image_url\n";
    $image_data = file_get_contents($image_url);
    if ($image_data) {
        file_put_contents($target_file, $image_data);
        
        $wp_filetype = wp_check_filetype($local_img_name, null);
        $attachment = array(
            'post_mime_type' => $wp_filetype['type'],
            'post_title'     => sanitize_file_name($p->post_title),
            'post_content'   => '',
            'post_status'    => 'publish'
        );
        
        $attachment_id = wp_insert_attachment($attachment, $target_file);
        if (!is_wp_error($attachment_id)) {
            $attach_data = wp_generate_attachment_metadata($attachment_id, $target_file);
            wp_update_attachment_metadata($attachment_id, $attach_data);
            
            // Delete old thumbnail mapping and set new
            delete_post_thumbnail($p->ID);
            set_post_thumbnail($p->ID, $attachment_id);
            echo "Successfully updated image for {$p->ID}\n";
        } else {
            echo "Failed to insert attachment for {$p->ID}\n";
        }
    } else {
        echo "Failed to download image for {$p->ID}\n";
    }
    sleep(2); // avoid rate limit
}

echo "Flushing cache...\n";
if (function_exists('litespeed_purge_all')) {
    litespeed_purge_all();
}
echo "Done!\n";
?>
