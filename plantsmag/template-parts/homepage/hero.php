<?php
/**
 * Hero Section Template Part
 *
 * @package PlantsMag
 */

$hero_title = get_theme_mod('plantsmag_hero_title', __('Your Garden Your Passion', 'plantsmag'));
$hero_subtitle = get_theme_mod('plantsmag_hero_subtitle', __('Whether you\'re dreaming of a lush, verdant paradise or a sleek, modern outdoor retreat, we\'ll work closely with you to bring your vision to life.', 'plantsmag'));
$hero_bg = get_theme_mod('plantsmag_hero_bg', '');
$cta_text = get_theme_mod('plantsmag_hero_cta_text', __('Read More', 'plantsmag'));
$cta_link = get_theme_mod('plantsmag_hero_cta_link', '#about');
?>

<section id="hero" class="pm-hero">
    <?php if ($hero_bg): ?>
        <div class="pm-hero-bg">
            <img src="<?php echo esc_url($hero_bg); ?>" alt="" loading="eager">
        </div>
    <?php endif; ?>

    <div class="pm-hero-overlay"></div>

    <div class="pm-container">
        <div class="pm-hero-content">
            <div class="pm-hero-text">
                <?php if ($hero_title): ?>
                    <h1 class="pm-hero-title">
                        <span class="pm-hero-title-line"><?php echo esc_html($hero_title); ?></span>
                    </h1>
                <?php endif; ?>

                <?php if ($hero_subtitle): ?>
                    <p class="pm-hero-subtitle"><?php echo esc_html($hero_subtitle); ?></p>
                <?php endif; ?>

                <?php if ($cta_text): ?>
                    <div class="pm-hero-cta">
                        <a href="<?php echo esc_url($cta_link); ?>" class="pm-btn pm-btn-white">
                            <?php echo esc_html($cta_text); ?>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                stroke-width="2">
                                <path d="M7 17L17 7M17 7H7M17 7V17" />
                            </svg>
                        </a>
                    </div>
                <?php endif; ?>
            </div>

            <div class="pm-hero-visual">
                <div class="pm-hero-image-wrapper">
                    <img src="<?php echo esc_url(PLANTSMAG_URI . '/assets/images/hero-plant.png'); ?>"
                        alt="<?php esc_attr_e('Plants', 'plantsmag'); ?>" class="pm-hero-image" loading="eager">
                </div>

                <div class="pm-hero-badge">
                    <div class="pm-hero-badge-inner">
                        <span
                            class="pm-hero-badge-text"><?php esc_html_e('Your Garden, Grow Your Dreams', 'plantsmag'); ?></span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Social Links -->
    <div class="pm-hero-social">
        <?php plantsmag_social_links(); ?>
    </div>

    <!-- Scroll Indicator -->
    <div class="pm-hero-scroll">
        <a href="#about" class="pm-scroll-down" aria-label="<?php esc_attr_e('Scroll down', 'plantsmag'); ?>">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14M5 12l7 7 7-7" />
            </svg>
        </a>
    </div>
</section>