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

</body>

</html>