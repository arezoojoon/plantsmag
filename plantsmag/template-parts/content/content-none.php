<?php
/**
 * Content None Template Part
 *
 * @package PlantsMag
 */

?>

<section class="pm-no-results">
    <div class="pm-no-results-icon">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z" />
            <path d="M12 8c-2.5 2-4 5-4 8" />
            <path d="M12 8c2.5 2 4 5 4 8" />
            <path d="M12 2v6" />
        </svg>
    </div>

    <?php if (is_home() && current_user_can('publish_posts')): ?>

        <h2 class="pm-no-results-title"><?php esc_html_e('Ready to publish your first post?', 'plantsmag'); ?></h2>
        <p><?php esc_html_e('Your garden is waiting for content. Start by adding your first plant guide or article.', 'plantsmag'); ?>
        </p>
        <a href="<?php echo esc_url(admin_url('post-new.php')); ?>" class="pm-btn pm-btn-primary">
            <?php esc_html_e('Create Your First Post', 'plantsmag'); ?>
        </a>

    <?php elseif (is_search()): ?>

        <h2 class="pm-no-results-title"><?php esc_html_e('Nothing Found', 'plantsmag'); ?></h2>
        <p><?php esc_html_e('Sorry, but nothing matched your search terms. Please try again with some different keywords.', 'plantsmag'); ?>
        </p>
        <?php get_search_form(); ?>

    <?php else: ?>

        <h2 class="pm-no-results-title"><?php esc_html_e('Nothing Found', 'plantsmag'); ?></h2>
        <p><?php esc_html_e('It seems we can\'t find what you\'re looking for. Perhaps searching can help.', 'plantsmag'); ?>
        </p>
        <?php get_search_form(); ?>

    <?php endif; ?>
</section>