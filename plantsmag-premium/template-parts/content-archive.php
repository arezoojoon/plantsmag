<?php
/**
 * Template part for displaying posts in archive/index loops
 *
 * @package PlantsMag_Premium
 */
?>

<article id="post-<?php the_ID(); ?>" <?php post_class('blog-card'); ?>>
    <a href="<?php the_permalink(); ?>" class="blog-card-img-wrap">
        <?php if ( has_post_thumbnail() ) : ?>
            <?php the_post_thumbnail('medium_large', ['class' => 'blog-card-img']); ?>
        <?php else: ?>
            <div class="blog-card-img blog-card-img-placeholder">
                <span style="font-size: 3rem;">🌿</span>
            </div>
        <?php endif; ?>
        
        <?php
        $categories = get_the_category();
        if ( ! empty( $categories ) ) {
            echo '<span class="blog-card-cat">' . esc_html( $categories[0]->name ) . '</span>';
        }
        ?>
    </a>

    <div class="blog-card-body">
        <div class="blog-card-meta">
            <span class="meta-date"><?php echo get_the_date(); ?></span>
            <span class="meta-dot">•</span>
            <span class="meta-author"><?php the_author(); ?></span>
        </div>
        
        <h3 class="blog-card-title">
            <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
        </h3>
        
        <a href="<?php the_permalink(); ?>" class="blog-card-link">
            Read Guide 
            <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
    </div>
</article>
