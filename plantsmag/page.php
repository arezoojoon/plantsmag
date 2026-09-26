<?php
/**
 * Default Page Template
 *
 * @package PlantsMag
 */

get_header();
?>

<main id="primary" class="site-main page-template">
    <?php
    while (have_posts()):
        the_post();
        ?>

        <?php if (has_post_thumbnail() && !is_front_page()): ?>
            <div class="pm-page-hero">
                <?php the_post_thumbnail('plantsmag-featured'); ?>
                <div class="pm-page-hero-overlay"></div>
                <div class="pm-container">
                    <div class="pm-page-hero-content">
                        <?php plantsmag_breadcrumbs(); ?>
                        <h1 class="pm-page-title"><?php the_title(); ?></h1>
                    </div>
                </div>
            </div>
        <?php endif; ?>

        <div class="pm-container">
            <?php if (!has_post_thumbnail() || is_front_page()): ?>
                <?php if (!is_front_page()): ?>
                    <?php plantsmag_breadcrumbs(); ?>
                    <header class="pm-page-header">
                        <h1 class="pm-page-title"><?php the_title(); ?></h1>
                    </header>
                <?php endif; ?>
            <?php endif; ?>

            <article id="post-<?php the_ID(); ?>" <?php post_class('pm-page-content'); ?>>
                <div class="entry-content">
                    <?php
                    the_content();

                    wp_link_pages(
                        array(
                            'before' => '<div class="page-links">' . esc_html__('Pages:', 'plantsmag'),
                            'after' => '</div>',
                        )
                    );
                    ?>
                </div>

                <?php if (get_edit_post_link()): ?>
                    <footer class="pm-page-footer">
                        <?php
                        edit_post_link(
                            sprintf(
                                wp_kses(
                                    __('Edit <span class="screen-reader-text">%s</span>', 'plantsmag'),
                                    array('span' => array('class' => array()))
                                ),
                                get_the_title()
                            ),
                            '<span class="edit-link">',
                            '</span>'
                        );
                        ?>
                    </footer>
                <?php endif; ?>
            </article>

            <?php
            // Comments on pages if enabled
            if (comments_open() || get_comments_number()):
                comments_template();
            endif;
            ?>
        </div>

        <?php
    endwhile;
    ?>
</main>

<?php
get_footer();
