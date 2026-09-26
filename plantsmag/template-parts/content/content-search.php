<?php
/**
 * Content Search Template Part
 *
 * @package PlantsMag
 */

?>

<article id="post-<?php the_ID(); ?>" <?php post_class('pm-search-result'); ?>>
    <div class="pm-search-result-inner">
        <?php if (has_post_thumbnail()): ?>
            <a href="<?php the_permalink(); ?>" class="pm-search-result-image">
                <?php the_post_thumbnail('thumbnail'); ?>
            </a>
        <?php endif; ?>

        <div class="pm-search-result-content">
            <div class="pm-search-result-meta">
                <span
                    class="pm-search-result-type"><?php echo esc_html(get_post_type_object(get_post_type())->labels->singular_name); ?></span>
                <span class="pm-search-result-date"><?php echo get_the_date(); ?></span>
            </div>

            <h2 class="pm-search-result-title">
                <a href="<?php the_permalink(); ?>">
                    <?php the_title(); ?>
                </a>
            </h2>

            <p class="pm-search-result-excerpt">
                <?php echo wp_trim_words(get_the_excerpt(), 25); ?>
            </p>

            <a href="<?php the_permalink(); ?>" class="pm-search-result-link">
                <?php esc_html_e('Read More', 'plantsmag'); ?>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
            </a>
        </div>
    </div>
</article>