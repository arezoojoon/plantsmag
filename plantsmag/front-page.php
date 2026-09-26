<?php
/**
 * Front Page Template
 *
 * @package PlantsMag
 */

get_header();
?>

<main id="primary" class="site-main front-page">

    <?php
    // Hero Section
    if (get_theme_mod('plantsmag_show_hero', true)) {
        get_template_part('template-parts/homepage/hero');
    }

    // About Section
    if (get_theme_mod('plantsmag_show_about', true)) {
        get_template_part('template-parts/homepage/about');
    }

    // Services Section
    if (get_theme_mod('plantsmag_show_services', true)) {
        get_template_part('template-parts/homepage/services');
    }

    // Portfolio Section
    if (get_theme_mod('plantsmag_show_portfolio', true)) {
        get_template_part('template-parts/homepage/portfolio');
    }

    // Testimonials Section
    if (get_theme_mod('plantsmag_show_testimonials', true)) {
        get_template_part('template-parts/homepage/testimonials');
    }

    // Blog Section
    if (get_theme_mod('plantsmag_show_blog', true)) {
        get_template_part('template-parts/homepage/blog-grid');
    }

    // Newsletter Section
    if (get_theme_mod('plantsmag_show_newsletter', true)) {
        get_template_part('template-parts/homepage/newsletter');
    }

    // CTA Section
    if (get_theme_mod('plantsmag_show_cta', true)) {
        get_template_part('template-parts/homepage/cta');
    }
    ?>

</main>

<?php
get_footer();
