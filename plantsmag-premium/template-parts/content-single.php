<?php
/**
 * Template part for displaying single posts
 *
 * @package PlantsMag_Premium
 */
?>

<article id="post-<?php the_ID(); ?>" <?php post_class('premium-single-article'); ?>>
    
    <?php if ( has_post_thumbnail() ) : ?>
        <div class="article-featured-img">
            <?php the_post_thumbnail('full', ['style' => 'width:100%; height:auto; display:block; border-radius: var(--radius-lg); object-fit: cover; max-height: 600px;', 'fetchpriority' => 'high', 'loading' => 'eager']); ?>
        </div>
    <?php else : ?>
        <div class="article-featured-img-placeholder" style="width:100%; height: 400px; border-radius: var(--radius-lg); margin-bottom: 3rem; background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary-light) 100%); display:flex; align-items:center; justify-content:center; box-shadow: var(--shadow-md);">
            <div style="text-align:center; color:rgba(255,255,255,0.2);">
                <svg width="100" height="100" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                <div style="font-family: var(--font-display); font-size: 1.5rem; font-weight: 700; margin-top: 1rem;">PlantsMag Exclusive</div>
            </div>
        </div>
    <?php endif; ?>

    <div class="article-header" style="margin-bottom: 3rem;">
        <?php
        // Breadcrumbs
        if (function_exists('plantsmag_breadcrumbs')) {
            plantsmag_breadcrumbs();
        }

        $categories = get_the_category();
        if ( ! empty( $categories ) ) {
            echo '<span class="category-badge">' . esc_html( $categories[0]->name ) . '</span>';
        }
        ?>
        
        <?php the_title( '<h1 class="entry-title" style="font-size: clamp(2rem, 4vw, 3.5rem); line-height: 1.1; font-weight: 900; letter-spacing: -0.02em; margin-bottom: 1.5rem;">', '</h1>' ); ?>
        
        <div class="entry-meta" style="display:flex; align-items:center; gap: 1rem; padding: 1.5rem 0; border-top: 1px solid rgba(0,0,0,0.05); border-bottom: 1px solid rgba(0,0,0,0.05);">
            <?php echo get_avatar( get_the_author_meta('ID'), 50, '', '', array('style'=>'border-radius:50%;') ); ?>
            <div>
                <div style="font-weight:700; color:var(--color-text-title);"><?php echo esc_html(get_the_author()); ?></div>
                <div style="font-size: 0.85rem; color:var(--color-text-muted);"><?php echo get_the_date(); ?> • <?php echo reading_time(); ?> min read</div>
            </div>
        </div>
    </div>

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
</article>
