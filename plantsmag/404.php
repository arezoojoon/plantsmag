<?php
/**
 * 404 Error Page Template
 *
 * @package PlantsMag
 */

get_header();
?>

<main id="primary" class="site-main error-404">
    <div class="pm-container">
        <div class="pm-404-content">
            <div class="pm-404-visual">
                <span class="pm-404-number">404</span>
                <div class="pm-404-plant">
                    <svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="1">
                        <path d="M12 22V12" />
                        <path d="M12 12c-4-6-10-6-10-4 0 4 6 6 10 4z" />
                        <path d="M12 12c4-6 10-6 10-4 0 4-6 6-10 4z" />
                        <path d="M12 8c0-4 3-6 5-7-1 3-2 7-5 7z" />
                        <path d="M12 8c0-4-3-6-5-7 1 3 2 7 5 7z" />
                    </svg>
                </div>
            </div>

            <h1 class="pm-404-title"><?php esc_html_e('Page Not Found', 'plantsmag'); ?></h1>
            <p class="pm-404-text">
                <?php esc_html_e('Oops! It looks like the page you\'re looking for has wilted away. Don\'t worry, let\'s help you find what you need.', 'plantsmag'); ?>
            </p>

            <div class="pm-404-search">
                <?php get_search_form(); ?>
            </div>

            <div class="pm-404-links">
                <p><?php esc_html_e('Or try one of these:', 'plantsmag'); ?></p>
                <ul>
                    <li><a
                            href="<?php echo esc_url(home_url('/')); ?>"><?php esc_html_e('Go to Homepage', 'plantsmag'); ?></a>
                    </li>
                    <li><a
                            href="<?php echo esc_url(get_post_type_archive_link('plant_guide')); ?>"><?php esc_html_e('Browse Plant Guides', 'plantsmag'); ?></a>
                    </li>
                    <li><a
                            href="<?php echo esc_url(get_post_type_archive_link('product_review')); ?>"><?php esc_html_e('Read Product Reviews', 'plantsmag'); ?></a>
                    </li>
                </ul>
            </div>

            <a href="<?php echo esc_url(home_url('/')); ?>" class="pm-btn pm-btn-primary">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
                    <polyline points="9 22 9 12 15 12 15 22" />
                </svg>
                <?php esc_html_e('Back to Home', 'plantsmag'); ?>
            </a>
        </div>
    </div>
</main>

<?php
get_footer();
