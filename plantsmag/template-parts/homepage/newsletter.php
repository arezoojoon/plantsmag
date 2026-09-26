<?php
/**
 * Newsletter Section Template Part
 *
 * @package PlantsMag
 */

?>

<section id="newsletter" class="pm-section pm-newsletter">
    <div class="pm-container">
        <div class="pm-newsletter-wrapper">
            <div class="pm-newsletter-content">
                <div class="pm-newsletter-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="1.5">
                        <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                        <polyline points="22,6 12,13 2,6" />
                    </svg>
                </div>
                <h2 class="pm-newsletter-title"><?php esc_html_e('Subscribe to Our Newsletter', 'plantsmag'); ?></h2>
                <p class="pm-newsletter-text">
                    <?php esc_html_e('Get the latest plant care tips, gardening guides, and exclusive offers delivered straight to your inbox.', 'plantsmag'); ?>
                </p>
            </div>

            <form class="pm-newsletter-form" action="#" method="post">
                <?php wp_nonce_field('plantsmag_newsletter', 'newsletter_nonce'); ?>
                <div class="pm-newsletter-input-group">
                    <input type="email" name="email" class="pm-newsletter-input"
                        placeholder="<?php esc_attr_e('Enter your email address', 'plantsmag'); ?>" required>
                    <button type="submit" class="pm-btn pm-btn-primary pm-newsletter-btn">
                        <?php esc_html_e('Subscribe', 'plantsmag'); ?>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="2">
                            <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
                        </svg>
                    </button>
                </div>
                <p class="pm-newsletter-privacy">
                    <?php esc_html_e('We respect your privacy. Unsubscribe at any time.', 'plantsmag'); ?>
                </p>
            </form>
        </div>
    </div>
</section>