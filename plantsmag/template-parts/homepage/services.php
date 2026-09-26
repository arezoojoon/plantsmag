<?php
/**
 * Services Section Template Part
 *
 * @package PlantsMag
 */

// Get services from a custom query or use hardcoded defaults
$services = array(
    array(
        'title' => __('Seasonal Plantings', 'plantsmag'),
        'description' => __('Our team of experienced will work closely with you to create.', 'plantsmag'),
        'icon' => 'planting',
        'image' => PLANTSMAG_URI . '/assets/images/service-1.jpg',
        'link' => '#',
    ),
    array(
        'title' => __('Irrigation System', 'plantsmag'),
        'description' => __('Our team of experienced will work closely with you to create.', 'plantsmag'),
        'icon' => 'water',
        'image' => PLANTSMAG_URI . '/assets/images/service-2.jpg',
        'link' => '#',
    ),
    array(
        'title' => __('Landscape Design', 'plantsmag'),
        'description' => __('Our team of experienced will work closely with you to create.', 'plantsmag'),
        'icon' => 'design',
        'image' => PLANTSMAG_URI . '/assets/images/service-3.jpg',
        'link' => '#',
    ),
    array(
        'title' => __('Garden Renovation', 'plantsmag'),
        'description' => __('Our team of experienced will work closely with you to create.', 'plantsmag'),
        'icon' => 'renovation',
        'image' => PLANTSMAG_URI . '/assets/images/service-4.jpg',
        'link' => '#',
    ),
);

// Icons SVG
$icons = array(
    'planting' => '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2"><path d="M24 42V26"/><path d="M24 26c-4-8-12-10-16-8 2 6 8 12 16 8z"/><path d="M24 26c4-8 12-10 16-8-2 6-8 12-16 8z"/><path d="M24 16c0-6 4-10 8-12-2 6-4 12-8 12z"/><path d="M24 16c0-6-4-10-8-12 2 6 4 12 8 12z"/></svg>',
    'water' => '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2"><path d="M24 6l12 16c3 4 4 8 0 14-4 6-12 8-18 4-6-4-8-10-6-16L24 6z"/></svg>',
    'design' => '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2"><rect x="6" y="6" width="36" height="36" rx="2"/><path d="M6 18h36"/><path d="M18 18v24"/></svg>',
    'renovation' => '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2"><path d="M40 28l-8-8V8H16v12l-8 8v12h32V28z"/><path d="M20 40v-8h8v8"/></svg>',
);
?>

<section id="services" class="pm-section pm-services">
    <div class="pm-section-bg"></div>

    <div class="pm-container">
        <!-- Section Header -->
        <div class="pm-section-header">
            <div class="pm-section-label">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path
                        d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
                </svg>
                <span><?php esc_html_e('Our Services', 'plantsmag'); ?></span>
            </div>
            <h2 class="pm-section-title"><?php esc_html_e('Crafting Outdoor Masterpieces', 'plantsmag'); ?></h2>
        </div>

        <!-- Services Grid -->
        <div class="pm-services-grid">
            <?php foreach ($services as $service): ?>
                <div class="pm-service-card">
                    <div class="pm-service-card-bg">
                        <img src="<?php echo esc_url($service['image']); ?>"
                            alt="<?php echo esc_attr($service['title']); ?>" loading="lazy">
                    </div>
                    <div class="pm-service-card-inner">
                        <div class="pm-service-card-icon">
                            <?php echo isset($icons[$service['icon']]) ? $icons[$service['icon']] : ''; ?>
                        </div>
                        <h3 class="pm-service-card-title"><?php echo esc_html($service['title']); ?></h3>
                        <p class="pm-service-card-text"><?php echo esc_html($service['description']); ?></p>
                        <a href="<?php echo esc_url($service['link']); ?>" class="pm-service-card-link"
                            aria-label="<?php echo esc_attr($service['title']); ?>">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                stroke-width="2">
                                <path d="M5 12h14M12 5l7 7-7 7" />
                            </svg>
                        </a>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>

        <!-- View All Link -->
        <div class="pm-services-footer">
            <p>
                <?php esc_html_e('We are largest independent Gardening company', 'plantsmag'); ?>
                <a href="<?php echo esc_url(get_post_type_archive_link('plant_guide')); ?>" class="pm-link-arrow">
                    <?php esc_html_e('View all Service', 'plantsmag'); ?>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M5 12h14M12 5l7 7-7 7" />
                    </svg>
                </a>
            </p>
        </div>
    </div>
</section>