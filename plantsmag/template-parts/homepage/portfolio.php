<?php
/**
 * Portfolio Section Template Part
 *
 * @package PlantsMag
 */

// Get project categories
$categories = get_terms(
    array(
        'taxonomy' => 'project_category',
        'hide_empty' => true,
    )
);

// Get projects
$projects = new WP_Query(
    array(
        'post_type' => 'project',
        'posts_per_page' => 6,
        'orderby' => 'date',
        'order' => 'DESC',
    )
);
?>

<section id="portfolio" class="pm-section pm-portfolio">
    <div class="pm-container">
        <!-- Section Header -->
        <div class="pm-section-header">
            <div class="pm-section-label">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                    <circle cx="8.5" cy="8.5" r="1.5" />
                    <polyline points="21 15 16 10 5 21" />
                </svg>
                <span><?php esc_html_e('Project', 'plantsmag'); ?></span>
            </div>
            <h2 class="pm-section-title"><?php esc_html_e('Our Best Work', 'plantsmag'); ?></h2>
        </div>

        <!-- Portfolio Filters -->
        <?php if (!empty($categories) && !is_wp_error($categories)): ?>
            <div class="pm-portfolio-filters">
                <button class="pm-filter-btn active" data-filter="*">
                    <?php esc_html_e('All', 'plantsmag'); ?>
                </button>
                <?php foreach ($categories as $category): ?>
                    <button class="pm-filter-btn" data-filter="<?php echo esc_attr($category->slug); ?>">
                        <?php echo esc_html($category->name); ?>
                    </button>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>

        <!-- Portfolio Grid -->
        <?php if ($projects->have_posts()): ?>
            <div class="pm-portfolio-grid">
                <?php
                while ($projects->have_posts()):
                    $projects->the_post();
                    $terms = get_the_terms(get_the_ID(), 'project_category');
                    $term_slugs = $terms ? wp_list_pluck($terms, 'slug') : array();
                    ?>
                    <div class="pm-portfolio-item" data-category="<?php echo esc_attr(implode(' ', $term_slugs)); ?>">
                        <a href="<?php the_permalink(); ?>" class="pm-portfolio-link">
                            <div class="pm-portfolio-image">
                                <?php if (has_post_thumbnail()): ?>
                                    <?php the_post_thumbnail('plantsmag-card'); ?>
                                <?php else: ?>
                                    <img src="<?php echo esc_url(PLANTSMAG_URI . '/assets/images/placeholder.jpg'); ?>"
                                        alt="<?php the_title_attribute(); ?>">
                                <?php endif; ?>
                            </div>
                            <div class="pm-portfolio-overlay">
                                <h3 class="pm-portfolio-title"><?php the_title(); ?></h3>
                                <?php if ($terms): ?>
                                    <span class="pm-portfolio-cat"><?php echo esc_html($terms[0]->name); ?></span>
                                <?php endif; ?>
                            </div>
                        </a>
                    </div>
                    <?php
                endwhile;
                wp_reset_postdata();
                ?>
            </div>
        <?php else: ?>
            <!-- Fallback Portfolio Items -->
            <div class="pm-portfolio-grid">
                <?php
                $placeholder_items = array(
                    array('title' => __('Garden Care', 'plantsmag'), 'cat' => __('Garden Care', 'plantsmag')),
                    array('title' => __('Lawn Maintenance', 'plantsmag'), 'cat' => __('Lawn Care', 'plantsmag')),
                    array('title' => __('Plant Installation', 'plantsmag'), 'cat' => __('Planting', 'plantsmag')),
                    array('title' => __('Landscape Design', 'plantsmag'), 'cat' => __('Design', 'plantsmag')),
                    array('title' => __('Seasonal Care', 'plantsmag'), 'cat' => __('Garden Care', 'plantsmag')),
                    array('title' => __('Irrigation Setup', 'plantsmag'), 'cat' => __('Lawn Care', 'plantsmag')),
                );

                foreach ($placeholder_items as $index => $item):
                    ?>
                    <div class="pm-portfolio-item" data-category="<?php echo esc_attr(sanitize_title($item['cat'])); ?>">
                        <div class="pm-portfolio-link">
                            <div class="pm-portfolio-image">
                                <img src="<?php echo esc_url(PLANTSMAG_URI . '/assets/images/portfolio-' . ($index + 1) . '.jpg'); ?>"
                                    alt="<?php echo esc_attr($item['title']); ?>" loading="lazy">
                            </div>
                            <div class="pm-portfolio-overlay">
                                <h3 class="pm-portfolio-title"><?php echo esc_html($item['title']); ?></h3>
                                <span class="pm-portfolio-cat"><?php echo esc_html($item['cat']); ?></span>
                            </div>
                        </div>
                    </div>
                    <?php
                endforeach;
                ?>
            </div>
        <?php endif; ?>

        <!-- View All Button -->
        <div class="pm-portfolio-footer">
            <a href="<?php echo esc_url(get_post_type_archive_link('project')); ?>" class="pm-btn pm-btn-secondary">
                <?php esc_html_e('View All Projects', 'plantsmag'); ?>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
            </a>
        </div>
    </div>
</section>