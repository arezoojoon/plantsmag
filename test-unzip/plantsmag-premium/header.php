<?php
/**
 * The premium header for our theme
 *
 * @package PlantsMag_Premium
 */
?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="profile" href="https://gmpg.org/xfn/11">
	<?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<?php if(is_single()): ?>
<!-- Reading Progress Bar for Articles -->
<div class="reading-progress-container">
    <div class="reading-progress-bar" id="reading-progress"></div>
</div>
<?php endif; ?>

<header id="masthead" class="site-header">
    <div class="container header-grid">
        <div class="site-branding">
            <?php
            if ( has_custom_logo() ) :
                // Apply our premium sizing to the native custom logo
                $custom_logo_id = get_theme_mod( 'custom_logo' );
                $logo = wp_get_attachment_image_src( $custom_logo_id , 'full' );
                echo '<a href="'.esc_url( home_url( '/' ) ).'" class="brand-link-wrap"><img src="'. esc_url( $logo[0] ) .'" alt="' . get_bloginfo( 'name' ) . '" class="site-logo-img"><span class="brand-text">Plants<span class="text-accent">Mag</span></span></a>';
            else :
                ?>
                <h1 class="site-title"><a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home" class="brand-link-wrap"><img src="<?php echo get_template_directory_uri(); ?>/logo.png" class="site-logo-img" alt="PlantsMag Logo"> <span class="brand-text">Plants<span class="text-accent">Mag</span></span></a></h1>
                <?php
            endif;
            ?>
        </div><!-- .site-branding -->

        <nav id="site-navigation" class="main-navigation">
            <?php
            wp_nav_menu(
                array(
                    'theme_location' => 'primary',
                    'menu_id'        => 'primary-menu',
                    'fallback_cb'    => false,
                    'container'      => false,
                )
            );
            ?>
            <div class="nav-cta">
                <a href="<?php echo esc_url( home_url( '/watering-calculator' ) ); ?>" class="btn btn-outline">Smart Tools</a>
            </div>
        </nav><!-- #site-navigation -->
    </div><!-- .container -->
</header><!-- #masthead -->

<div id="page" class="site">
