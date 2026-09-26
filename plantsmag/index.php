<?php
/**
 * The main template file
 *
 * @package PlantsMag
 */

get_header();
?>

<main id="primary" class="site-main">
    <div class="pm-container">

        <?php if (have_posts()): ?>

            <?php if (is_home() && !is_front_page()): ?>
                <header class="page-header">
                    <h1 class="page-title"><?php single_post_title(); ?></h1>
                </header>
            <?php endif; ?>

            <div class="pm-posts-grid pm-grid pm-grid-3">
                <?php
                while (have_posts()):
                    the_post();
                    get_template_part('template-parts/content/content', get_post_type());
                endwhile;
                ?>
            </div>

            <?php plantsmag_pagination(); ?>

        <?php else: ?>

            <?php get_template_part('template-parts/content/content', 'none'); ?>

        <?php endif; ?>

    </div>
</main>

<?php
get_sidebar();
get_footer();
