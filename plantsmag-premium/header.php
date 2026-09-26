<?php
/**
 * The premium header for PlantsMag
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
	
	<!-- 🚀 Google Fonts Optimization -->
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
	<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap"></noscript>
	
	<?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<?php if( is_single() ): ?>
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
                $custom_logo_id = get_theme_mod( 'custom_logo' );
                $logo = wp_get_attachment_image_src( $custom_logo_id , 'full' );
                echo '<a href="'.esc_url( home_url( '/' ) ).'" class="brand-link-wrap"><img src="'. esc_url( $logo[0] ) .'" alt="' . get_bloginfo( 'name' ) . '" class="site-logo-img"><span class="brand-text">Plants<span class="text-accent">Mag</span></span></a>';
            else :
                ?>
                <a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home" class="brand-link-wrap">
                    <img src="<?php echo get_template_directory_uri(); ?>/logo.png" class="site-logo-img" alt="PlantsMag Logo">
                    <span class="brand-text">Plants<span class="text-accent">Mag</span></span>
                </a>
                <?php
            endif;
            ?>
        </div><!-- .site-branding -->

        <nav id="site-navigation" class="main-navigation" aria-label="Primary Navigation">
            <?php
            if ( has_nav_menu( 'primary' ) ) {
                wp_nav_menu(
                    array(
                        'theme_location' => 'primary',
                        'menu_id'        => 'primary-menu',
                        'container'      => false,
                    )
                );
            } else {
                echo '<ul id="primary-menu" class="menu">';
                echo '<li><a href="' . esc_url( home_url( '/' ) ) . '">Home</a></li>';
                echo '<li><a href="' . esc_url( home_url( '/plant-guides/' ) ) . '">Plant Guides</a></li>';
                echo '<li><a href="' . esc_url( home_url( '/watering-calculator' ) ) . '">Watering</a></li>';
                echo '<li><a href="' . esc_url( home_url( '/plant-disease-finder' ) ) . '">AI Doctor</a></li>';
                echo '</ul>';
            }
            ?>
            <div class="nav-cta">
                <a href="<?php echo esc_url( home_url( '/plant-disease-finder' ) ); ?>" class="btn btn-primary nav-btn">
                    <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                    AI Plant Doctor
                </a>
            </div>
        </nav><!-- #site-navigation -->

        <!-- Hamburger Button (Mobile) -->
        <button class="nav-hamburger" id="nav-hamburger" aria-label="Toggle navigation" aria-expanded="false">
            <span></span>
            <span></span>
            <span></span>
        </button>
    </div><!-- .container -->

    <!-- Mobile Drawer -->
    <div class="mobile-nav-drawer" id="mobile-nav-drawer" aria-hidden="true">
        <ul class="mobile-menu">
            <li><a href="<?php echo esc_url( home_url( '/' ) ); ?>">🏠 Home</a></li>
            <li><a href="<?php echo esc_url( home_url( '/plant-guides/' ) ); ?>">📖 Plant Guides</a></li>
            <li><a href="<?php echo esc_url( home_url( '/watering-calculator' ) ); ?>">💧 Watering Calculator</a></li>
            <li><a href="<?php echo esc_url( home_url( '/plant-disease-finder' ) ); ?>">🔬 AI Plant Doctor</a></li>
        </ul>
        <a href="<?php echo esc_url( home_url( '/plant-disease-finder' ) ); ?>" class="btn btn-primary" style="width:100%; justify-content:center; margin-top:1rem;">
            Diagnose My Plant Free →
        </a>
    </div>
    <div class="mobile-nav-overlay" id="mobile-nav-overlay"></div>
</header><!-- #masthead -->

<div id="page" class="site">
