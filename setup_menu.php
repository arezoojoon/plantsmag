<?php
if ( !defined('ABSPATH') ) {
    require_once('wp-load.php');
}

// 1. Set Tool Pages to use 'page-tools.php' template
function set_template_by_slug($slug, $template) {
    global $wpdb;
    $id = $wpdb->get_var( $wpdb->prepare("SELECT ID FROM $wpdb->posts WHERE post_name = %s AND post_type = 'page'", $slug) );
    if($id) {
        update_post_meta($id, '_wp_page_template', $template);
    }
}
set_template_by_slug('watering-calculator', 'page-tools.php');
set_template_by_slug('plant-disease-finder', 'page-tools.php');

// 2. Create Primary Menu if it doesn't exist
$menu_name = 'Main Navigation';
$menu_exists = wp_get_nav_menu_object( $menu_name );

if( !$menu_exists ) {
    $menu_id = wp_create_nav_menu($menu_name);
    
    // Add Home
    wp_update_nav_menu_item($menu_id, 0, array(
        'menu-item-title' => 'Home',
        'menu-item-url' => home_url('/'),
        'menu-item-status' => 'publish',
        'menu-item-type' => 'custom'
    ));

    // Add Articles
    wp_update_nav_menu_item($menu_id, 0, array(
        'menu-item-title' => 'Houseplant Guides',
        'menu-item-url' => home_url('/blog'), // Assuming blog or default archive
        'menu-item-status' => 'publish',
        'menu-item-type' => 'custom'
    ));

    // Map it to theme location
    $locations = get_theme_mod('nav_menu_locations');
    $locations['primary'] = $menu_id;
    set_theme_mod('nav_menu_locations', $locations);
}

echo "TEMPLATE AND MENU SETUP SUCCESSFUL";
?>
