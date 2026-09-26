<?php
/**
 * The main template file
 *
 * @package PlantsMag_Premium
 */

get_header();
?>

<main id="primary" class="site-main container" style="padding: 60px 24px; min-height: 60vh;">

	<?php
	if ( have_posts() ) :

		if ( is_home() && ! is_front_page() ) :
			?>
			<header class="page-header mb-4 text-center">
				<h1 class="page-title"><?php single_post_title(); ?></h1>
			</header>
			<?php
		endif;

        echo '<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px;">';
		/* Start the Loop */
		while ( have_posts() ) :
			the_post();

			get_template_part('template-parts/content', 'archive');

		endwhile;
        echo '</div>';

		the_posts_pagination(array(
            'mid_size'  => 2,
            'prev_text' => '&larr; Previous',
            'next_text' => 'Next &rarr;',
        ));

	else :

		echo '<p>No content found.</p>';

	endif;
	?>

</main><!-- #main -->

<?php
get_footer();
