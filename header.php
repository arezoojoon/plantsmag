<?php
/**
 * Header Template
 *
 * @package PlantsMag
 */

?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>

<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link rel="profile" href="https://gmpg.org/xfn/11">

    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
    <?php wp_body_open(); ?>

    <a class="skip-link screen-reader-text" href="#primary">
        <?php esc_html_e('Skip to content', 'plantsmag'); ?>
    </a>

    <header id="masthead" class="site-header">
        <div class="header-inner">
            <div class="pm-container">
                <div class="header-content">

                    <!-- Site Branding -->
                    <div class="site-branding">
                        <?php if (has_custom_logo()): ?>
                            <div class="site-logo">
                                <?php the_custom_logo(); ?>
                            </div>
                        <?php else: ?>
                            <div class="site-identity">
                                <a href="<?php echo esc_url(home_url('/')); ?>" class="site-title-link">
                                    <span class="site-icon">
                                        <svg width="40" height="40" viewBox="0 0 40 40" fill="none"
                                            xmlns="http://www.w3.org/2000/svg">
                                            <circle cx="20" cy="20" r="20" fill="currentColor" />
                                            <path
                                                d="M20 8C14 8 10 14 10 20C10 26 14 32 20 32C22 28 24 24 24 20C24 16 22 12 20 8Z"
                                                fill="white" />
                                            <path
                                                d="M20 8C26 8 30 14 30 20C30 26 26 32 20 32C18 28 16 24 16 20C16 16 18 12 20 8Z"
                                                fill="white" fill-opacity="0.7" />
                                        </svg>
                                    </span>
                                    <span class="site-title-text">
                                        <span class="site-title"><?php bloginfo('name'); ?></span>
                                        <?php
                                        $description = get_bloginfo('description', 'display');
                                        if ($description || is_customize_preview()):
                                            ?>
                                            <span class="site-description"><?php echo $description; ?></span>
                                        <?php endif; ?>
                                    </span>
                                </a>
                            </div>
                        <?php endif; ?>
                    </div>

                    <!-- Primary Navigation -->
                    <nav id="site-navigation" class="main-navigation"
                        aria-label="<?php esc_attr_e('Primary Menu', 'plantsmag'); ?>">
                        <?php
                        wp_nav_menu(
                            array(
                                'theme_location' => 'primary',
                                'menu_id' => 'primary-menu',
                                'menu_class' => 'primary-menu',
                                'container' => false,
                                'fallback_cb' => 'plantsmag_primary_menu_fallback',
                                'depth' => 3,
                            )
                        );
                        ?>
                    </nav>

                    <!-- Header Actions -->
                    <div class="header-actions">
                        <!-- Search Toggle -->
                        <button class="header-search-toggle" type="button"
                            aria-label="<?php esc_attr_e('Search', 'plantsmag'); ?>" data-toggle="search-modal">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <circle cx="11" cy="11" r="8"></circle>
                                <path d="M21 21l-4.35-4.35"></path>
                            </svg>
                        </button>

                        <!-- CTA Button -->
                        <?php
                        $header_cta_text = get_theme_mod('plantsmag_header_cta_text', __('Get Started', 'plantsmag'));
                        $header_cta_link = get_theme_mod('plantsmag_header_cta_link', '#');
                        if ($header_cta_text):
                            ?>
                            <a href="<?php echo esc_url($header_cta_link); ?>" class="pm-btn pm-btn-primary header-cta">
                                <?php echo esc_html($header_cta_text); ?>
                            </a>
                        <?php endif; ?>

                        <!-- Mobile Menu Toggle -->
                        <button class="mobile-menu-toggle" type="button"
                            aria-label="<?php esc_attr_e('Menu', 'plantsmag'); ?>" aria-expanded="false"
                            aria-controls="mobile-menu">
                            <span class="hamburger">
                                <span class="hamburger-line"></span>
                                <span class="hamburger-line"></span>
                                <span class="hamburger-line"></span>
                            </span>
                        </button>
                    </div>

                </div>
            </div>
        </div>

        <!-- Mobile Menu -->
        <div id="mobile-menu" class="mobile-menu" aria-hidden="true">
            <div class="mobile-menu-inner">
                <div class="mobile-menu-header">
                    <span class="mobile-menu-title"><?php esc_html_e('Menu', 'plantsmag'); ?></span>
                    <button class="mobile-menu-close" type="button"
                        aria-label="<?php esc_attr_e('Close menu', 'plantsmag'); ?>">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="2">
                            <path d="M18 6L6 18M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                <nav class="mobile-navigation">
                    <?php
                    wp_nav_menu(
                        array(
                            'theme_location' => 'primary',
                            'menu_id' => 'mobile-primary-menu',
                            'menu_class' => 'mobile-menu-list',
                            'container' => false,
                            'depth' => 2,
                        )
                    );
                    ?>
                </nav>
                <?php if ($header_cta_text): ?>
                    <div class="mobile-menu-cta">
                        <a href="<?php echo esc_url($header_cta_link); ?>" class="pm-btn pm-btn-primary pm-btn-lg">
                            <?php echo esc_html($header_cta_text); ?>
                        </a>
                    </div>
                <?php endif; ?>
            </div>
        </div>

        <!-- Search Modal -->
        <div id="search-modal" class="search-modal" aria-hidden="true">
            <div class="search-modal-overlay"></div>
            <div class="search-modal-content">
                <button class="search-modal-close" type="button"
                    aria-label="<?php esc_attr_e('Close search', 'plantsmag'); ?>">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 6L6 18M6 6l12 12"></path>
                    </svg>
                </button>
                <form role="search" method="get" class="search-form" action="<?php echo esc_url(home_url('/')); ?>">
                    <label class="screen-reader-text"
                        for="search-field"><?php esc_html_e('Search for:', 'plantsmag'); ?></label>
                    <input type="search" id="search-field" class="search-field"
                        placeholder="<?php esc_attr_e('Search...', 'plantsmag'); ?>"
                        value="<?php echo get_search_query(); ?>" name="s" autofocus>
                    <button type="submit" class="search-submit">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="2">
                            <circle cx="11" cy="11" r="8"></circle>
                            <path d="M21 21l-4.35-4.35"></path>
                        </svg>
                        <span class="screen-reader-text"><?php esc_html_e('Search', 'plantsmag'); ?></span>
                    </button>
                </form>
            </div>
        </div>
    </header>