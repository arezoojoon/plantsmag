<?php
/**
 * The template for displaying all single posts
 *
 * @package PlantsMag_Premium
 */

get_header();
?>

<div class="container" style="margin-top: 4rem; margin-bottom: 4rem;">
	<?php
	while ( have_posts() ) :
		the_post();
		?>
        <div class="content-sidebar-grid">
            <main id="primary" class="site-main">
                <?php
                get_template_part( 'template-parts/content', 'single' );
                ?>

                <?php
                if ( comments_open() || get_comments_number() ) :
                    comments_template();
                endif;
                ?>
            </main>

            <!-- Load Sidebar -->
            <?php get_sidebar(); ?>
        </div>
		<?php
	endwhile;
	?>
</div>

<?php
get_footer();
