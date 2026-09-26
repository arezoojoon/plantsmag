<?php
/**
 * WooCommerce Wrapper Template
 *
 * @package PlantsMag
 */

get_header();
?>

<main id="primary" class="site-main woocommerce-page">
    <?php if (!is_front_page() && !is_product()): ?>
        <div class="pm-page-hero">
            <div class="pm-page-hero-overlay"></div>
            <div class="pm-container">
                <div class="pm-page-hero-content">
                    <?php plantsmag_breadcrumbs(); ?>
                    <h1 class="pm-page-title"><?php woocommerce_page_title(); ?></h1>
                </div>
            </div>
        </div>
    <?php endif; ?>

    <div class="pm-container">
        <div class="pm-content-wrapper <?php echo !is_active_sidebar('shop-sidebar') ? 'no-sidebar' : ''; ?>">
            <div class="pm-content">
                <?php woocommerce_content(); ?>
            </div>

            <?php if (is_active_sidebar('shop-sidebar')): ?>
                <aside id="secondary" class="widget-area sidebar shop-sidebar">
                    <?php dynamic_sidebar('shop-sidebar'); ?>
                </aside>
            <?php endif; ?>
        </div>
    </div>
</main>

<?php
get_footer();
