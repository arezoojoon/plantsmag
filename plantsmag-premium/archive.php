<?php
/**
 * The template for displaying archive pages (and main blog page)
 *
 * @package PlantsMag_Premium
 */

get_header();
?>

<div class="container" style="margin-top: 4rem; margin-bottom: 4rem;">
	<header class="page-header" style="text-align:center; margin-bottom: 4rem;">
		<?php if ( is_home() && ! is_front_page() ) : ?>
            <h1 class="page-title">Latest Articles</h1>
            <div class="archive-description"><p>Expert guides to keep your houseplants thriving.</p></div>
        <?php else : ?>
            <?php
            if ( function_exists('plantsmag_breadcrumbs') ) {
                plantsmag_breadcrumbs();
            }
            the_archive_title( '<h1 class="page-title" style="margin-top: 15px;">', '</h1>' );
            the_archive_description( '<div class="archive-description">', '</div>' );
            ?>
        <?php endif; ?>
	</header><!-- .page-header -->

    <div class="content-sidebar-grid">
        <main id="primary" class="site-main">
            <?php if ( have_posts() ) : ?>
                <div class="archive-grid">
                    <?php
                    while ( have_posts() ) :
                        the_post();
                        get_template_part( 'template-parts/content', 'archive' );
                    endwhile;
                    ?>
                </div>
                
                <?php
                the_posts_pagination(array(
                    'mid_size'  => 2,
                    'prev_text' => '&larr; Previous',
                    'next_text' => 'Next &rarr;',
                ));
                ?>

            <?php else : ?>
                <p>No articles found.</p>
            <?php endif; ?>
        </main>

        <!-- Load Sidebar -->
        <?php get_sidebar(); ?>
    </div>
</div>

<?php
get_footer();
