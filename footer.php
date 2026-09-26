<?php
/**
 * Footer Template
 *
 * @package PlantsMag
 */

?>

<footer id="colophon" class="site-footer">

    <!-- Footer Widgets -->
    <?php if (is_active_sidebar('footer-1') || is_active_sidebar('footer-2') || is_active_sidebar('footer-3') || is_active_sidebar('footer-4')): ?>
        <div class="footer-widgets">
            <div class="pm-container">
                <div class="footer-widgets-grid">
                    <?php if (is_active_sidebar('footer-1')): ?>
                        <div class="footer-widget-area">
                            <?php dynamic_sidebar('footer-1'); ?>
                        </div>
                    <?php endif; ?>

                    <?php if (is_active_sidebar('footer-2')): ?>
                        <div class="footer-widget-area">
                            <?php dynamic_sidebar('footer-2'); ?>
                        </div>
                    <?php endif; ?>

                    <?php if (is_active_sidebar('footer-3')): ?>
                        <div class="footer-widget-area">
                            <?php dynamic_sidebar('footer-3'); ?>
                        </div>
                    <?php endif; ?>

                    <?php if (is_active_sidebar('footer-4')): ?>
                        <div class="footer-widget-area">
                            <?php dynamic_sidebar('footer-4'); ?>
                        </div>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    <?php endif; ?>

    <!-- Footer Bottom -->
    <div class="footer-bottom">
        <div class="pm-container">
            <div class="footer-bottom-content">

                <!-- Copyright -->
                <div class="footer-copyright">
                    <?php
                    $copyright_text = get_theme_mod('plantsmag_copyright_text', '');
                    if ($copyright_text) {
                        echo wp_kses_post($copyright_text);
                    } else {
                        printf(
                            /* translators: 1: Current year, 2: Site name */
                            esc_html__('© %1$s %2$s. All rights reserved.', 'plantsmag'),
                            date('Y'),
                            get_bloginfo('name')
                        );
                    }
                    ?>
                </div>

                <!-- Footer Menu -->
                <?php if (has_nav_menu('footer')): ?>
                    <nav class="footer-navigation" aria-label="<?php esc_attr_e('Footer Menu', 'plantsmag'); ?>">
                        <?php
                        wp_nav_menu(
                            array(
                                'theme_location' => 'footer',
                                'menu_class' => 'footer-menu',
                                'container' => false,
                                'depth' => 1,
                            )
                        );
                        ?>
                    </nav>
                <?php endif; ?>

                <!-- Social Links -->
                <div class="footer-social">
                    <?php plantsmag_social_links(); ?>
                </div>

            </div>
        </div>
    </div>

</footer>

<!-- Back to Top Button -->
<button id="back-to-top" class="back-to-top" aria-label="<?php esc_attr_e('Back to top', 'plantsmag'); ?>">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round">
        <polyline points="18 15 12 9 6 15"></polyline>
    </svg>
</button>

<?php wp_footer(); ?>

<!-- App Bottom Navigation (Mobile Only) -->
<nav class="pm-bottom-nav">
    <a href="/" class="pm-nav-item <?php echo is_front_page() ? 'active' : ''; ?>">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
        <span>Home</span>
    </a>
    <a href="/watering-calculator/" class="pm-nav-item <?php echo (is_page('watering-calculator')) ? 'active' : ''; ?>">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>
        </svg>
        <span>Watering</span>
    </a>
    <a href="/plant-disease-finder/" class="pm-nav-item <?php echo (is_page('plant-disease-finder')) ? 'active' : ''; ?>">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
        </svg>
        <span>AI Doctor</span>
    </a>
    <a href="/plant-guides/" class="pm-nav-item <?php echo (is_category() || is_single() || is_page('plant-guides')) ? 'active' : ''; ?>">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
            <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
            <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
        </svg>
        <span>Guides</span>
    </a>
</nav>

</body>

</html>