<?php
/**
 * The template for displaying all pages
 *
 * @package PlantsMag_Premium
 */

get_header();
?>

<main id="primary" class="site-main container" style="padding: 60px 24px; min-height: 60vh;">

	<?php
	while ( have_posts() ) :
		the_post();
		?>

		<article id="post-<?php the_ID(); ?>" <?php post_class('card'); ?>>
			<header class="entry-header">
                <div style="text-align: center; margin-bottom: 2rem;">
                    <?php if (function_exists('rank_math_the_breadcrumbs')) rank_math_the_breadcrumbs(); ?>
                </div>
				<?php the_title( '<h1 class="entry-title text-center mb-4" style="font-size:2.5rem;">', '</h1>' ); ?>
			</header><!-- .entry-header -->

			<?php if ( has_post_thumbnail() ) : ?>
				<div class="post-thumbnail text-center mb-4">
					<?php the_post_thumbnail('large', ['style' => 'border-radius: var(--radius-md); max-width:100%; height:auto;']); ?>
				</div>
			<?php endif; ?>

			<div class="entry-content">
				<?php
				the_content();
				?>
			</div><!-- .entry-content -->
		</article><!-- #post-<?php the_ID(); ?> -->

		<?php
	endwhile; // End of the loop.
	?>

</main><!-- #main -->

<?php
get_footer();
