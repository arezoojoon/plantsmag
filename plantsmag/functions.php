<?php
/**
 * PlantsMag Theme Functions
 *
 * @package PlantsMag
 * @version 1.0.0
 */

// Prevent direct access
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Theme Version
 */
define( 'PLANTSMAG_VERSION', '1.0.0' );
define( 'PLANTSMAG_DIR', get_template_directory() );
define( 'PLANTSMAG_URI', get_template_directory_uri() );

/**
 * Include Required Files
 */
require_once PLANTSMAG_DIR . '/inc/theme-setup.php';
require_once PLANTSMAG_DIR . '/inc/enqueue.php';
require_once PLANTSMAG_DIR . '/inc/customizer.php';
require_once PLANTSMAG_DIR . '/inc/custom-post-types.php';
require_once PLANTSMAG_DIR . '/inc/widgets.php';
require_once PLANTSMAG_DIR . '/inc/template-tags.php';
require_once PLANTSMAG_DIR . '/inc/template-functions.php';
require_once PLANTSMAG_DIR . '/inc/seo.php';
require_once PLANTSMAG_DIR . '/inc/performance.php';
require_once PLANTSMAG_DIR . '/inc/security.php';

/**
 * Content Width
 */
if ( ! isset( $content_width ) ) {
    $content_width = 1200;
}
