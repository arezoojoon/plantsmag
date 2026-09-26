<?php
/**
 * Template part for displaying single posts
 *
 * @package PlantsMag_Premium
 */
?>

<article id="post-<?php the_ID(); ?>" <?php post_class('card'); ?> style="padding: 0;">
    
    <?php if ( has_post_thumbnail() ) : ?>
        <div class="article-hero-image" style="width:100%; height: 500px; overflow:hidden; border-radius: var(--radius-md) var(--radius-md) 0 0;">
            <img src="<?php the_post_thumbnail_url('full'); ?>" style="width:100%; height:100%; object-fit:cover;" alt="<?php the_title_attribute(); ?>">
        </div>
    <?php endif; ?>

    <div class="article-content-wrapper" style="padding: 3rem;">
        <header class="article-header">
            <?php
            // Breadcrumbs for SEO
            if (function_exists('rank_math_the_breadcrumbs')) rank_math_the_breadcrumbs();

            $categories = get_the_category();
            if ( ! empty( $categories ) ) {
                echo '<span class="category-badge">' . esc_html( $categories[0]->name ) . '</span>';
            }
            ?>
            <?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>
            <div class="entry-meta" style="margin-top: 1.5rem; display:flex; align-items:center; gap: 1rem; color: var(--color-text-muted);">
                <?php 
                echo get_avatar( get_the_author_meta('ID'), 40, '', '', array('class'=>'author-avatar') );
                echo '<span class="author-name" style="font-weight:600; color:var(--color-primary);">' . get_the_author() . '</span>';
                echo '<span class="post-date"> • ' . get_the_date() . '</span>';
                ?>
            </div>
        </header>

        <div class="entry-content">
            <?php
            the_content();

            wp_link_pages(
                array(
                    'before' => '<div class="page-links">' . esc_html__( 'Pages:', 'plantsmag-premium' ),
                    'after'  => '</div>',
                )
            );
            ?>
        </div>
    </div>
</article>
