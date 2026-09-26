<?php
/**
 * Template part for displaying posts in archive/index loops
 *
 * @package PlantsMag_Premium
 */
?>

<article id="post-<?php the_ID(); ?>" <?php post_class('card'); ?>>
    <header class="entry-header">
        <?php if ( has_post_thumbnail() ) : ?>
            <div class="post-thumbnail mb-4">
                <a href="<?php the_permalink(); ?>">
                    <?php the_post_thumbnail('medium_large', ['style' => 'width:100%; height:auto; border-radius: var(--radius-sm);']); ?>
                </a>
            </div>
        <?php endif; ?>
        
        <?php
        the_title( '<h2 class="entry-title" style="font-size:1.5rem;"><a href="' . esc_url( get_permalink() ) . '" rel="bookmark">', '</a></h2>' );
        ?>
    </header>

    <div class="entry-summary pt-2">
        <?php the_excerpt(); ?>
        <a href="<?php the_permalink(); ?>" class="pm-btn pm-btn-outline mt-4" style="padding: 8px 20px; font-size: 0.9rem;">Read More</a>
    </div>
</article>
