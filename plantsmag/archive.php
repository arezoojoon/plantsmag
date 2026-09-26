<?php
/**
 * Archive Template
 *
 * @package PlantsMag
 */

get_header();
?>

<main id="primary" class="site-main archive-page">
    <!-- Archive Header -->
    <div class="pm-archive-header">
        <div class="pm-container">
            <?php plantsmag_breadcrumbs(); ?>
            <h1 class="pm-archive-title"><?php the_archive_title(); ?></h1>
            <?php the_archive_description('<div class="pm-archive-description">', '</div>'); ?>
        </div>
    </div>

    <div class="pm-container">
        <div class="pm-content-wrapper">
            <div class="pm-content">
                <?php if (have_posts()): ?>

                    <div class="pm-posts-grid pm-grid pm-grid-2">
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

            <?php get_sidebar(); ?>
        </div>
    </div>
</main>

<?php
get_footer();
