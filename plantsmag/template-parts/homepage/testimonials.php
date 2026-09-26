<?php
/**
 * Testimonials Section Template Part
 *
 * @package PlantsMag
 */

$testimonials = array(
    array(
        'content' => __('PlantsMag transformed our backyard into a beautiful oasis. Their attention to detail and plant care knowledge is exceptional!', 'plantsmag'),
        'author' => __('Sarah Johnson', 'plantsmag'),
        'role' => __('Homeowner', 'plantsmag'),
        'avatar' => PLANTSMAG_URI . '/assets/images/testimonial-1.jpg',
        'rating' => 5,
    ),
    array(
        'content' => __('The best plant care guides I have ever found online. Their articles helped me save my dying ZZ Plant!', 'plantsmag'),
        'author' => __('Michael Chen', 'plantsmag'),
        'role' => __('Plant Enthusiast', 'plantsmag'),
        'avatar' => PLANTSMAG_URI . '/assets/images/testimonial-2.jpg',
        'rating' => 5,
    ),
    array(
        'content' => __('Amazing product reviews! I always check PlantsMag before buying any gardening equipment.', 'plantsmag'),
        'author' => __('Emily Rodriguez', 'plantsmag'),
        'role' => __('Urban Gardener', 'plantsmag'),
        'avatar' => PLANTSMAG_URI . '/assets/images/testimonial-3.jpg',
        'rating' => 5,
    ),
);
?>

<section id="testimonials" class="pm-section pm-testimonials">
    <div class="pm-container">
        <div class="pm-testimonials-wrapper">
            <!-- Section Header -->
            <div class="pm-section-header">
                <div class="pm-section-label">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                    </svg>
                    <span><?php esc_html_e('Testimonials', 'plantsmag'); ?></span>
                </div>
                <h2 class="pm-section-title"><?php esc_html_e('What Our Clients Say', 'plantsmag'); ?></h2>
            </div>

            <!-- Testimonials Slider -->
            <div class="pm-testimonials-slider" data-slider="testimonials">
                <div class="pm-testimonials-track">
                    <?php foreach ($testimonials as $testimonial): ?>
                        <div class="pm-testimonial-card">
                            <div class="pm-testimonial-rating">
                                <?php echo plantsmag_star_rating($testimonial['rating']); ?>
                            </div>
                            <blockquote class="pm-testimonial-content">
                                <?php echo esc_html($testimonial['content']); ?>
                            </blockquote>
                            <div class="pm-testimonial-author">
                                <div class="pm-testimonial-avatar">
                                    <img src="<?php echo esc_url($testimonial['avatar']); ?>"
                                        alt="<?php echo esc_attr($testimonial['author']); ?>" loading="lazy">
                                </div>
                                <div class="pm-testimonial-info">
                                    <h4 class="pm-testimonial-name"><?php echo esc_html($testimonial['author']); ?></h4>
                                    <span class="pm-testimonial-role"><?php echo esc_html($testimonial['role']); ?></span>
                                </div>
                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>

                <!-- Slider Navigation -->
                <div class="pm-testimonials-nav">
                    <button class="pm-slider-prev" type="button"
                        aria-label="<?php esc_attr_e('Previous', 'plantsmag'); ?>">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="2">
                            <polyline points="15 18 9 12 15 6" />
                        </svg>
                    </button>
                    <div class="pm-slider-dots"></div>
                    <button class="pm-slider-next" type="button"
                        aria-label="<?php esc_attr_e('Next', 'plantsmag'); ?>">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="2">
                            <polyline points="9 18 15 12 9 6" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    </div>
</section>