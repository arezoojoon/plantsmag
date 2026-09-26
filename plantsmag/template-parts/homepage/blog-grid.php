<?php
/**
 * Blog Grid Section Template Part
 *
 * @package PlantsMag
 */

$blog_posts = new WP_Query(
    array(
        'post_type' => 'post',
        'posts_per_page' => 3,
        'orderby' => 'date',
        'order' => 'DESC',
    )
);
?>

<section id="blog" class="pm-section pm-blog-section">
    <div class="pm-container">
        <!-- Section Header -->
        <div class="pm-section-header">
            <div class="pm-section-label">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
                </svg>
                <span><?php esc_html_e('Our Blog', 'plantsmag'); ?></span>
            </div>
            <h2 class="pm-section-title"><?php esc_html_e('Latest Articles & Tips', 'plantsmag'); ?></h2>
            <p class="pm-section-desc">
                <?php esc_html_e('Stay updated with the latest plant care tips, gardening guides, and product reviews.', 'plantsmag'); ?>
            </p>
        </div>

        <!-- Blog Grid -->
        <?php if ($blog_posts->have_posts()): ?>
            <div class="pm-blog-grid pm-grid pm-grid-3">
                <?php
                while ($blog_posts->have_posts()):
                    $blog_posts->the_post();
                    ?>
                    <article class="pm-blog-card">
                        <a href="<?php the_permalink(); ?>" class="pm-blog-card-image">
                            <?php if (has_post_thumbnail()): ?>
                                <?php the_post_thumbnail('plantsmag-card'); ?>
                            <?php else: ?>
                                <img src="<?php echo esc_url(PLANTSMAG_URI . '/assets/images/placeholder.jpg'); ?>"
                                    alt="<?php the_title_attribute(); ?>">
                            <?php endif; ?>
                        </a>
                        <div class="pm-blog-card-content">
                            <div class="pm-blog-card-meta">
                                <span class="pm-blog-card-date"><?php echo get_the_date(); ?></span>
                                <?php
                                $categories = get_the_category();
                                if ($categories):
                                    ?>
                                    <span class="pm-blog-card-cat">
                                        <a href="<?php echo esc_url(get_category_link($categories[0]->term_id)); ?>">
                                            <?php echo esc_html($categories[0]->name); ?>
                                        </a>
                                    </span>
                                <?php endif; ?>
                            </div>
                            <h3 class="pm-blog-card-title">
                                <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                            </h3>
                            <p class="pm-blog-card-excerpt"><?php echo wp_trim_words(get_the_excerpt(), 15); ?></p>
                            <a href="<?php the_permalink(); ?>" class="pm-blog-card-link">
                                <?php esc_html_e('Read More', 'plantsmag'); ?>
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="2">
                                    <path d="M5 12h14M12 5l7 7-7 7" />
                                </svg>
                            </a>
                        </div>
                    </article>
                    <?php
                endwhile;
                wp_reset_postdata();
                ?>
            </div>

            <!-- View All Button -->
            <div class="pm-blog-footer">
                <a href="<?php echo esc_url(get_permalink(get_option('page_for_posts'))); ?>"
                    class="pm-btn pm-btn-secondary">
                    <?php esc_html_e('View All Articles', 'plantsmag'); ?>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M5 12h14M12 5l7 7-7 7" />
                    </svg>
                </a>
            </div>

        <?php else: ?>
            <div class="pm-no-posts">
                <p><?php esc_html_e('No posts found. Start creating some content!', 'plantsmag'); ?></p>
            </div>
        <?php endif; ?>
    </div>
</section>