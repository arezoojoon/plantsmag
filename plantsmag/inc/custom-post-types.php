<?php
/**
 * Custom Post Types & Taxonomies
 *
 * @package PlantsMag
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Register Custom Post Types
 */
function plantsmag_register_post_types()
{

    // ========================================
    // Plant Guides CPT
    // ========================================
    $plant_guide_labels = array(
        'name' => _x('Plant Guides', 'Post Type General Name', 'plantsmag'),
        'singular_name' => _x('Plant Guide', 'Post Type Singular Name', 'plantsmag'),
        'menu_name' => __('Plant Guides', 'plantsmag'),
        'name_admin_bar' => __('Plant Guide', 'plantsmag'),
        'archives' => __('Guide Archives', 'plantsmag'),
        'attributes' => __('Guide Attributes', 'plantsmag'),
        'all_items' => __('All Guides', 'plantsmag'),
        'add_new_item' => __('Add New Guide', 'plantsmag'),
        'add_new' => __('Add New', 'plantsmag'),
        'new_item' => __('New Guide', 'plantsmag'),
        'edit_item' => __('Edit Guide', 'plantsmag'),
        'update_item' => __('Update Guide', 'plantsmag'),
        'view_item' => __('View Guide', 'plantsmag'),
        'view_items' => __('View Guides', 'plantsmag'),
        'search_items' => __('Search Guide', 'plantsmag'),
        'not_found' => __('Not found', 'plantsmag'),
        'not_found_in_trash' => __('Not found in Trash', 'plantsmag'),
        'featured_image' => __('Plant Image', 'plantsmag'),
        'set_featured_image' => __('Set plant image', 'plantsmag'),
        'remove_featured_image' => __('Remove plant image', 'plantsmag'),
        'use_featured_image' => __('Use as plant image', 'plantsmag'),
    );

    $plant_guide_args = array(
        'label' => __('Plant Guide', 'plantsmag'),
        'description' => __('Plant care guides and tutorials', 'plantsmag'),
        'labels' => $plant_guide_labels,
        'supports' => array('title', 'editor', 'thumbnail', 'excerpt', 'comments', 'revisions', 'custom-fields'),
        'taxonomies' => array('plant_type', 'difficulty_level'),
        'hierarchical' => false,
        'public' => true,
        'show_ui' => true,
        'show_in_menu' => true,
        'menu_position' => 5,
        'menu_icon' => 'dashicons-palmtree',
        'show_in_admin_bar' => true,
        'show_in_nav_menus' => true,
        'can_export' => true,
        'has_archive' => 'plant-guides',
        'exclude_from_search' => false,
        'publicly_queryable' => true,
        'capability_type' => 'post',
        'show_in_rest' => true,
        'rewrite' => array(
            'slug' => 'plant-guide',
            'with_front' => false,
        ),
    );

    register_post_type('plant_guide', $plant_guide_args);

    // ========================================
    // Product Reviews CPT
    // ========================================
    $review_labels = array(
        'name' => _x('Product Reviews', 'Post Type General Name', 'plantsmag'),
        'singular_name' => _x('Product Review', 'Post Type Singular Name', 'plantsmag'),
        'menu_name' => __('Product Reviews', 'plantsmag'),
        'name_admin_bar' => __('Product Review', 'plantsmag'),
        'archives' => __('Review Archives', 'plantsmag'),
        'all_items' => __('All Reviews', 'plantsmag'),
        'add_new_item' => __('Add New Review', 'plantsmag'),
        'add_new' => __('Add New', 'plantsmag'),
        'new_item' => __('New Review', 'plantsmag'),
        'edit_item' => __('Edit Review', 'plantsmag'),
        'update_item' => __('Update Review', 'plantsmag'),
        'view_item' => __('View Review', 'plantsmag'),
        'search_items' => __('Search Review', 'plantsmag'),
        'not_found' => __('Not found', 'plantsmag'),
        'not_found_in_trash' => __('Not found in Trash', 'plantsmag'),
    );

    $review_args = array(
        'label' => __('Product Review', 'plantsmag'),
        'description' => __('Gardening product reviews', 'plantsmag'),
        'labels' => $review_labels,
        'supports' => array('title', 'editor', 'thumbnail', 'excerpt', 'comments', 'revisions', 'custom-fields'),
        'taxonomies' => array('product_category'),
        'hierarchical' => false,
        'public' => true,
        'show_ui' => true,
        'show_in_menu' => true,
        'menu_position' => 6,
        'menu_icon' => 'dashicons-star-filled',
        'show_in_admin_bar' => true,
        'show_in_nav_menus' => true,
        'can_export' => true,
        'has_archive' => 'reviews',
        'exclude_from_search' => false,
        'publicly_queryable' => true,
        'capability_type' => 'post',
        'show_in_rest' => true,
        'rewrite' => array(
            'slug' => 'review',
            'with_front' => false,
        ),
    );

    register_post_type('product_review', $review_args);

    // ========================================
    // Projects/Portfolio CPT
    // ========================================
    $project_labels = array(
        'name' => _x('Projects', 'Post Type General Name', 'plantsmag'),
        'singular_name' => _x('Project', 'Post Type Singular Name', 'plantsmag'),
        'menu_name' => __('Projects', 'plantsmag'),
        'all_items' => __('All Projects', 'plantsmag'),
        'add_new_item' => __('Add New Project', 'plantsmag'),
        'add_new' => __('Add New', 'plantsmag'),
        'new_item' => __('New Project', 'plantsmag'),
        'edit_item' => __('Edit Project', 'plantsmag'),
        'update_item' => __('Update Project', 'plantsmag'),
        'view_item' => __('View Project', 'plantsmag'),
        'search_items' => __('Search Project', 'plantsmag'),
    );

    $project_args = array(
        'label' => __('Project', 'plantsmag'),
        'description' => __('Portfolio projects', 'plantsmag'),
        'labels' => $project_labels,
        'supports' => array('title', 'editor', 'thumbnail', 'excerpt'),
        'taxonomies' => array('project_category'),
        'hierarchical' => false,
        'public' => true,
        'show_ui' => true,
        'show_in_menu' => true,
        'menu_position' => 7,
        'menu_icon' => 'dashicons-portfolio',
        'has_archive' => 'projects',
        'rewrite' => array('slug' => 'project'),
        'show_in_rest' => true,
    );

    register_post_type('project', $project_args);
}
add_action('init', 'plantsmag_register_post_types', 0);

/**
 * Register Custom Taxonomies
 */
function plantsmag_register_taxonomies()
{

    // ========================================
    // Plant Type Taxonomy
    // ========================================
    $plant_type_labels = array(
        'name' => _x('Plant Types', 'taxonomy general name', 'plantsmag'),
        'singular_name' => _x('Plant Type', 'taxonomy singular name', 'plantsmag'),
        'search_items' => __('Search Plant Types', 'plantsmag'),
        'all_items' => __('All Plant Types', 'plantsmag'),
        'parent_item' => __('Parent Plant Type', 'plantsmag'),
        'parent_item_colon' => __('Parent Plant Type:', 'plantsmag'),
        'edit_item' => __('Edit Plant Type', 'plantsmag'),
        'update_item' => __('Update Plant Type', 'plantsmag'),
        'add_new_item' => __('Add New Plant Type', 'plantsmag'),
        'new_item_name' => __('New Plant Type Name', 'plantsmag'),
        'menu_name' => __('Plant Types', 'plantsmag'),
    );

    register_taxonomy(
        'plant_type',
        array('plant_guide'),
        array(
            'hierarchical' => true,
            'labels' => $plant_type_labels,
            'show_ui' => true,
            'show_admin_column' => true,
            'query_var' => true,
            'rewrite' => array('slug' => 'plant-type'),
            'show_in_rest' => true,
        )
    );

    // ========================================
    // Difficulty Level Taxonomy
    // ========================================
    $difficulty_labels = array(
        'name' => _x('Difficulty Levels', 'taxonomy general name', 'plantsmag'),
        'singular_name' => _x('Difficulty Level', 'taxonomy singular name', 'plantsmag'),
        'search_items' => __('Search Difficulty Levels', 'plantsmag'),
        'all_items' => __('All Difficulty Levels', 'plantsmag'),
        'edit_item' => __('Edit Difficulty Level', 'plantsmag'),
        'update_item' => __('Update Difficulty Level', 'plantsmag'),
        'add_new_item' => __('Add New Difficulty Level', 'plantsmag'),
        'new_item_name' => __('New Difficulty Level Name', 'plantsmag'),
        'menu_name' => __('Difficulty', 'plantsmag'),
    );

    register_taxonomy(
        'difficulty_level',
        array('plant_guide'),
        array(
            'hierarchical' => false,
            'labels' => $difficulty_labels,
            'show_ui' => true,
            'show_admin_column' => true,
            'query_var' => true,
            'rewrite' => array('slug' => 'difficulty'),
            'show_in_rest' => true,
        )
    );

    // ========================================
    // Product Category Taxonomy
    // ========================================
    $product_cat_labels = array(
        'name' => _x('Product Categories', 'taxonomy general name', 'plantsmag'),
        'singular_name' => _x('Product Category', 'taxonomy singular name', 'plantsmag'),
        'menu_name' => __('Categories', 'plantsmag'),
    );

    register_taxonomy(
        'product_category',
        array('product_review'),
        array(
            'hierarchical' => true,
            'labels' => $product_cat_labels,
            'show_ui' => true,
            'show_admin_column' => true,
            'rewrite' => array('slug' => 'product-category'),
            'show_in_rest' => true,
        )
    );

    // ========================================
    // Project Category Taxonomy
    // ========================================
    register_taxonomy(
        'project_category',
        array('project'),
        array(
            'hierarchical' => true,
            'labels' => array(
                'name' => __('Project Categories', 'plantsmag'),
                'singular_name' => __('Project Category', 'plantsmag'),
            ),
            'show_ui' => true,
            'show_admin_column' => true,
            'rewrite' => array('slug' => 'project-category'),
            'show_in_rest' => true,
        )
    );
}
add_action('init', 'plantsmag_register_taxonomies', 0);

/**
 * Add Meta Boxes for Plant Guides
 */
function plantsmag_add_plant_meta_boxes()
{
    add_meta_box(
        'plant_care_details',
        __('Plant Care Details', 'plantsmag'),
        'plantsmag_plant_care_meta_box',
        'plant_guide',
        'side',
        'default'
    );
}
add_action('add_meta_boxes', 'plantsmag_add_plant_meta_boxes');

/**
 * Plant Care Meta Box Callback
 */
function plantsmag_plant_care_meta_box($post)
{
    wp_nonce_field('plantsmag_plant_care_nonce', 'plant_care_nonce');

    $light_needs = get_post_meta($post->ID, '_plant_light_needs', true);
    $water_needs = get_post_meta($post->ID, '_plant_water_needs', true);
    $humidity = get_post_meta($post->ID, '_plant_humidity', true);
    $temperature = get_post_meta($post->ID, '_plant_temperature', true);
    ?>

    <p>
        <label for="plant_light_needs"><strong><?php esc_html_e('Light Needs', 'plantsmag'); ?></strong></label>
        <select id="plant_light_needs" name="plant_light_needs" style="width:100%;">
            <option value=""><?php esc_html_e('Select...', 'plantsmag'); ?></option>
            <option value="low" <?php selected($light_needs, 'low'); ?>><?php esc_html_e('Low Light', 'plantsmag'); ?>
            </option>
            <option value="medium" <?php selected($light_needs, 'medium'); ?>>
                <?php esc_html_e('Medium Light', 'plantsmag'); ?></option>
            <option value="bright-indirect" <?php selected($light_needs, 'bright-indirect'); ?>>
                <?php esc_html_e('Bright Indirect', 'plantsmag'); ?></option>
            <option value="direct" <?php selected($light_needs, 'direct'); ?>>
                <?php esc_html_e('Direct Sunlight', 'plantsmag'); ?></option>
        </select>
    </p>

    <p>
        <label for="plant_water_needs"><strong><?php esc_html_e('Water Needs', 'plantsmag'); ?></strong></label>
        <select id="plant_water_needs" name="plant_water_needs" style="width:100%;">
            <option value=""><?php esc_html_e('Select...', 'plantsmag'); ?></option>
            <option value="low" <?php selected($water_needs, 'low'); ?>>
                <?php esc_html_e('Low (Drought Tolerant)', 'plantsmag'); ?></option>
            <option value="moderate" <?php selected($water_needs, 'moderate'); ?>>
                <?php esc_html_e('Moderate', 'plantsmag'); ?></option>
            <option value="high" <?php selected($water_needs, 'high'); ?>>
                <?php esc_html_e('High (Keep Moist)', 'plantsmag'); ?></option>
        </select>
    </p>

    <p>
        <label for="plant_humidity"><strong><?php esc_html_e('Humidity', 'plantsmag'); ?></strong></label>
        <select id="plant_humidity" name="plant_humidity" style="width:100%;">
            <option value=""><?php esc_html_e('Select...', 'plantsmag'); ?></option>
            <option value="low" <?php selected($humidity, 'low'); ?>><?php esc_html_e('Low', 'plantsmag'); ?></option>
            <option value="average" <?php selected($humidity, 'average'); ?>>
                <?php esc_html_e('Average', 'plantsmag'); ?></option>
            <option value="high" <?php selected($humidity, 'high'); ?>><?php esc_html_e('High', 'plantsmag'); ?>
            </option>
        </select>
    </p>

    <p>
        <label for="plant_temperature"><strong><?php esc_html_e('Temperature Range', 'plantsmag'); ?></strong></label>
        <input type="text" id="plant_temperature" name="plant_temperature" value="<?php echo esc_attr($temperature); ?>"
            style="width:100%;" placeholder="e.g., 18-24°C">
    </p>

    <?php
}

/**
 * Save Plant Care Meta
 */
function plantsmag_save_plant_care_meta($post_id)
{
    if (!isset($_POST['plant_care_nonce']) || !wp_verify_nonce($_POST['plant_care_nonce'], 'plantsmag_plant_care_nonce')) {
        return;
    }

    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return;
    }

    if (!current_user_can('edit_post', $post_id)) {
        return;
    }

    $fields = array('plant_light_needs', 'plant_water_needs', 'plant_humidity', 'plant_temperature');

    foreach ($fields as $field) {
        if (isset($_POST[$field])) {
            update_post_meta($post_id, '_' . $field, sanitize_text_field($_POST[$field]));
        }
    }
}
add_action('save_post_plant_guide', 'plantsmag_save_plant_care_meta');

/**
 * Add Meta Boxes for Product Reviews
 */
function plantsmag_add_review_meta_boxes()
{
    add_meta_box(
        'review_details',
        __('Review Details', 'plantsmag'),
        'plantsmag_review_meta_box',
        'product_review',
        'side',
        'default'
    );
}
add_action('add_meta_boxes', 'plantsmag_add_review_meta_boxes');

/**
 * Review Meta Box Callback
 */
function plantsmag_review_meta_box($post)
{
    wp_nonce_field('plantsmag_review_nonce', 'review_nonce');

    $rating = get_post_meta($post->ID, '_review_rating', true);
    $pros = get_post_meta($post->ID, '_review_pros', true);
    $cons = get_post_meta($post->ID, '_review_cons', true);
    $affiliate_url = get_post_meta($post->ID, '_review_affiliate_url', true);
    $price = get_post_meta($post->ID, '_review_price', true);
    ?>

    <p>
        <label for="review_rating"><strong><?php esc_html_e('Rating (1-5)', 'plantsmag'); ?></strong></label>
        <input type="number" id="review_rating" name="review_rating" value="<?php echo esc_attr($rating); ?>" min="1"
            max="5" step="0.5" style="width:100%;">
    </p>

    <p>
        <label for="review_price"><strong><?php esc_html_e('Price', 'plantsmag'); ?></strong></label>
        <input type="text" id="review_price" name="review_price" value="<?php echo esc_attr($price); ?>"
            style="width:100%;" placeholder="e.g., $29.99">
    </p>

    <p>
        <label for="review_pros"><strong><?php esc_html_e('Pros (one per line)', 'plantsmag'); ?></strong></label>
        <textarea id="review_pros" name="review_pros" style="width:100%;"
            rows="3"><?php echo esc_textarea($pros); ?></textarea>
    </p>

    <p>
        <label for="review_cons"><strong><?php esc_html_e('Cons (one per line)', 'plantsmag'); ?></strong></label>
        <textarea id="review_cons" name="review_cons" style="width:100%;"
            rows="3"><?php echo esc_textarea($cons); ?></textarea>
    </p>

    <p>
        <label for="review_affiliate_url"><strong><?php esc_html_e('Affiliate/Buy URL', 'plantsmag'); ?></strong></label>
        <input type="url" id="review_affiliate_url" name="review_affiliate_url"
            value="<?php echo esc_url($affiliate_url); ?>" style="width:100%;">
    </p>

    <?php
}

/**
 * Save Review Meta
 */
function plantsmag_save_review_meta($post_id)
{
    if (!isset($_POST['review_nonce']) || !wp_verify_nonce($_POST['review_nonce'], 'plantsmag_review_nonce')) {
        return;
    }

    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return;
    }

    if (!current_user_can('edit_post', $post_id)) {
        return;
    }

    if (isset($_POST['review_rating'])) {
        update_post_meta($post_id, '_review_rating', floatval($_POST['review_rating']));
    }

    if (isset($_POST['review_price'])) {
        update_post_meta($post_id, '_review_price', sanitize_text_field($_POST['review_price']));
    }

    if (isset($_POST['review_pros'])) {
        update_post_meta($post_id, '_review_pros', sanitize_textarea_field($_POST['review_pros']));
    }

    if (isset($_POST['review_cons'])) {
        update_post_meta($post_id, '_review_cons', sanitize_textarea_field($_POST['review_cons']));
    }

    if (isset($_POST['review_affiliate_url'])) {
        update_post_meta($post_id, '_review_affiliate_url', esc_url_raw($_POST['review_affiliate_url']));
    }
}
add_action('save_post_product_review', 'plantsmag_save_review_meta');

/**
 * Flush Rewrite Rules on Theme Activation
 */
function plantsmag_rewrite_flush()
{
    plantsmag_register_post_types();
    plantsmag_register_taxonomies();
    flush_rewrite_rules();
}
add_action('after_switch_theme', 'plantsmag_rewrite_flush');
