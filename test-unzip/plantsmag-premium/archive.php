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
            <p>Expert guides to keep your houseplants thriving.</p>
        <?php else : ?>
            <?php
            the_archive_title( '<h1 class="page-title">', '</h1>' );
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
                the_posts_navigation(array(
                    'prev_text' => '&larr; Older posts',
                    'next_text' => 'Newer posts &rarr;',
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
