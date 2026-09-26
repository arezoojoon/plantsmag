<?php
/**
 * About Section Template Part
 *
 * @package PlantsMag
 */

$about_title = get_theme_mod('plantsmag_about_title', __('About PlantsMag', 'plantsmag'));
$about_description = get_theme_mod('plantsmag_about_description', __('At PlantsMag, we are committed to environmentally sustainable gardening practices that promote biodiversity, conserve resources, and minimize our environmental footprint. From water-wise irrigation systems to organic.', 'plantsmag'));
$years_experience = get_theme_mod('plantsmag_about_years', '25');
?>

<section id="about" class="pm-section pm-about">
    <div class="pm-container">
        <div class="pm-about-grid">
            <!-- Image Column -->
            <div class="pm-about-image-col">
                <div class="pm-about-image-wrapper">
                    <div class="pm-about-image-frame">
                        <img src="<?php echo esc_url(PLANTSMAG_URI . '/assets/images/about-image.jpg'); ?>"
                            alt="<?php esc_attr_e('About Us', 'plantsmag'); ?>" loading="lazy">
                    </div>
                    <div class="pm-about-badge">
                        <span class="pm-about-badge-number"><?php echo esc_html($years_experience); ?>+</span>
                        <span class="pm-about-badge-text"><?php esc_html_e('Year Experience', 'plantsmag'); ?></span>
                    </div>
                </div>
            </div>

            <!-- Content Column -->
            <div class="pm-about-content-col">
                <div class="pm-section-label">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z" />
                        <path d="M12 8c-2.5 2-4 5-4 8" />
                        <path d="M12 8c2.5 2 4 5 4 8" />
                        <path d="M12 2v6" />
                    </svg>
                    <span><?php esc_html_e('About Us', 'plantsmag'); ?></span>
                </div>

                <h2 class="pm-section-title"><?php echo esc_html($about_title); ?></h2>

                <p class="pm-about-text"><?php echo esc_html($about_description); ?></p>

                <!-- Features -->
                <div class="pm-about-features">
                    <div class="pm-about-feature">
                        <div class="pm-about-feature-icon">
                            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                stroke-width="1.5">
                                <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z" />
                                <path d="M9 12l2 2 4-4" />
                            </svg>
                        </div>
                        <div class="pm-about-feature-text">
                            <h4><?php esc_html_e('Customized Solutions', 'plantsmag'); ?></h4>
                        </div>
                    </div>
                    <div class="pm-about-feature">
                        <div class="pm-about-feature-icon">
                            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                stroke-width="1.5">
                                <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z" />
                                <path d="M9 12l2 2 4-4" />
                            </svg>
                        </div>
                        <div class="pm-about-feature-text">
                            <h4><?php esc_html_e('Expert Guidance', 'plantsmag'); ?></h4>
                        </div>
                    </div>
                </div>

                <!-- Progress Bars -->
                <div class="pm-about-progress-bars">
                    <div class="pm-progress-item">
                        <div class="pm-progress-header">
                            <span
                                class="pm-progress-label"><?php esc_html_e('Professional Expertise', 'plantsmag'); ?></span>
                            <span class="pm-progress-value">80%</span>
                        </div>
                        <div class="pm-progress-bar">
                            <div class="pm-progress-fill" data-progress="80"></div>
                        </div>
                    </div>
                    <div class="pm-progress-item">
                        <div class="pm-progress-header">
                            <span
                                class="pm-progress-label"><?php esc_html_e('Client Satisfaction', 'plantsmag'); ?></span>
                            <span class="pm-progress-value">90%</span>
                        </div>
                        <div class="pm-progress-bar">
                            <div class="pm-progress-fill" data-progress="90"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>