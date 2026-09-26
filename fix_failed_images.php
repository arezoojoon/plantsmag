<?php
require_once( dirname(__FILE__) . '/wp-load.php' );
global $wpdb;

echo "Fetching all published posts...\n";
$posts = $wpdb->get_results("SELECT ID, post_title FROM {$wpdb->posts} WHERE post_type = 'post' AND post_status = 'publish' ORDER BY ID DESC");

// Find shared images
$seen_images = array();
$posts_to_fix_image = array();

echo "Checking for duplicate images among unique posts...\n";
foreach ($posts as $p) {
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

echo "Found " . count($posts_to_fix_image) . " distinct posts sharing an image URL. Fixing with cURL...\n";

require_once(ABSPATH . 'wp-admin/includes/image.php');
require_once(ABSPATH . 'wp-admin/includes/file.php');
require_once(ABSPATH . 'wp-admin/includes/media.php');

$upload_dir = wp_upload_dir();

function download_image($url, $target_file) {
    $ch = curl_init($url);
    $fp = fopen($target_file, 'wb');
    curl_setopt($ch, CURLOPT_FILE, $fp);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)');
    curl_setopt($ch, CURLOPT_TIMEOUT, 60);
    $success = curl_exec($ch);
    curl_close($ch);
    fclose($fp);
    return $success;
}

foreach ($posts_to_fix_image as $p) {
    echo "Fixing image for post {$p->ID}: {$p->post_title}\n";
    $encoded_title = urlencode($p->post_title . " professional nature plant green minimal --no text watermark logo");
    $seed = rand(100000, 999999);
    $image_url = "https://image.pollinations.ai/prompt/{$encoded_title}?width=1200&height=630&model=flux&nologo=true&seed={$seed}";
    
    $local_img_name = 'img_' . $p->ID . '_' . $seed . '.jpg';
    $target_file = $upload_dir['path'] . '/' . $local_img_name;
    
    echo "Downloading new image: $image_url\n";
    
    if (download_image($image_url, $target_file) && filesize($target_file) > 10000) {
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
        echo "Failed to download image for {$p->ID} or file too small\n";
        if(file_exists($target_file)) unlink($target_file);
    }
    sleep(2); // avoid rate limit
}

echo "Flushing cache...\n";
if (function_exists('litespeed_purge_all')) {
    litespeed_purge_all();
}
echo "Done!\n";
?>
