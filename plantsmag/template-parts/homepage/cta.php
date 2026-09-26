<?php
/**
 * CTA Section Template Part
 *
 * @package PlantsMag
 */

$cta_title = get_theme_mod('plantsmag_cta_title', __('Ready to Transform Your Space?', 'plantsmag'));
$cta_text = get_theme_mod('plantsmag_cta_text', __('Let us help you create the garden of your dreams. Contact us today for a free consultation.', 'plantsmag'));
$cta_btn_text = get_theme_mod('plantsmag_cta_btn_text', __('Get Started', 'plantsmag'));
$cta_btn_link = get_theme_mod('plantsmag_cta_btn_link', '/contact');
?>

<section id="cta" class="pm-section pm-cta">
    <div class="pm-cta-bg">
        <div class="pm-cta-shape pm-cta-shape-1"></div>
        <div class="pm-cta-shape pm-cta-shape-2"></div>
    </div>

    <div class="pm-container">
        <div class="pm-cta-wrapper">
            <div class="pm-cta-content">
                <h2 class="pm-cta-title"><?php echo esc_html($cta_title); ?></h2>
                <p class="pm-cta-text"><?php echo esc_html($cta_text); ?></p>
            </div>
            <div class="pm-cta-action">
                <a href="<?php echo esc_url($cta_btn_link); ?>" class="pm-btn pm-btn-white pm-btn-lg">
                    <?php echo esc_html($cta_btn_text); ?>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M5 12h14M12 5l7 7-7 7" />
                    </svg>
                </a>
            </div>
        </div>
    </div>
</section>