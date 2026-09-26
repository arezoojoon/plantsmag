<?php
/**
 * One Click Demo Import Support
 *
 * @package PlantsMag
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Import Config
 */
function plantsmag_ocdi_import_files()
{
    return array(
        array(
            'import_file_name' => __('PlantsMag Demo', 'plantsmag'),
            'categories' => array('Gardening', 'Plants'),
            'import_file_url' => PLANTSMAG_URI . '/demo-content/content.xml',
            'import_widget_file_url' => PLANTSMAG_URI . '/demo-content/widgets.wie',
            'import_customizer_file_url' => PLANTSMAG_URI . '/demo-content/customizer.dat',
            'import_preview_image_url' => PLANTSMAG_URI . '/screenshot.png',
            'import_notice' => __('After you import this demo, you will have to setup the slider separately.', 'plantsmag'),
            'preview_url' => 'https://plantsmag.com/demo',
        ),
    );
}
add_filter('pt-ocdi/import_files', 'plantsmag_ocdi_import_files');

/**
 * After Import Setup
 */
function plantsmag_ocdi_after_import_setup()
{
    // Assign menus to their locations.
    $main_menu = get_term_by('name', 'Main Menu', 'nav_menu');
    $footer_menu = get_term_by('name', 'Footer Menu', 'nav_menu');

    set_theme_mod(
        'nav_menu_locations',
        array(
            'primary' => $main_menu->term_id,
            'footer' => $footer_menu->term_id,
        )
    );

    // Assign front page and posts page (blog page).
    $front_page_id = get_page_by_title('Home');
    $blog_page_id = get_page_by_title('Blog');

    update_option('show_on_front', 'page');
    update_option('page_on_front', $front_page_id->ID);
    update_option('page_for_posts', $blog_page_id->ID);
}
add_action('pt-ocdi/after_import', 'plantsmag_ocdi_after_import_setup');

/**
 * Disable Branding
 */
add_filter('pt-ocdi/disable_pt_branding', '__return_true');
