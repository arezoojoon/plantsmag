<?php
/**
 * Content Template Part
 *
 * @package PlantsMag
 */

?>

<article id="post-<?php the_ID(); ?>" <?php post_class('pm-card pm-post-card'); ?>>
    <?php if (has_post_thumbnail()): ?>
        <a href="<?php the_permalink(); ?>" class="pm-card-image">
            <?php the_post_thumbnail('plantsmag-card'); ?>
        </a>
    <?php endif; ?>

    <div class="pm-card-content">
        <div class="pm-card-meta">
            <?php
            $categories = get_the_category();
            if ($categories):
                ?>
                <a href="<?php echo esc_url(get_category_link($categories[0]->term_id)); ?>" class="pm-card-cat">
                    <?php echo esc_html($categories[0]->name); ?>
                </a>
            <?php endif; ?>
            <span class="pm-card-date"><?php echo get_the_date(); ?></span>
        </div>

        <h2 class="pm-card-title">
            <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
        </h2>

        <p class="pm-card-excerpt"><?php echo wp_trim_words(get_the_excerpt(), 15); ?></p>

        <a href="<?php the_permalink(); ?>" class="pm-card-link">
            <?php esc_html_e('Read More', 'plantsmag'); ?>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
        </a>
    </div>
</article>