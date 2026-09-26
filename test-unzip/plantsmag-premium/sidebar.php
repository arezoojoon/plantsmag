<?php
/**
 * The sidebar containing the main widget area.
 *
 * @package PlantsMag_Premium
 */

if ( ! is_active_sidebar( 'sidebar-1' ) ) {
	// If no widgets are active, let's output a beautiful custom AI box and recent posts
	?>
    <aside id="secondary" class="widget-area premium-sidebar">
        <!-- CTA Widget -->
        <div class="sidebar-widget ai-cta-widget">
            <div class="ai-cta-content">
                <span class="ai-badge">Featured Tool ⚡️</span>
                <h3>Sick Plant?</h3>
                <p>Upload a photo and let our AI Doctor instantly diagnose the disease and prescribe a cure.</p>
                <a href="<?php echo esc_url(home_url('/plant-disease-finder')); ?>" class="btn btn-primary" style="width:100%; text-align:center;">Launch AI Doctor</a>
            </div>
        </div>

        <!-- Recent Posts Widget -->
        <div class="sidebar-widget recent-posts-widget">
            <h2 class="widget-title">Trending Guides</h2>
            <ul class="premium-recent-posts">
                <?php
                $recent_posts = wp_get_recent_posts(array(
                    'numberposts' => 4,
                    'post_status' => 'publish'
                ));
                foreach( $recent_posts as $post_item ) : ?>
                    <li>
                        <a href="<?php echo get_permalink($post_item['ID']); ?>">
                            <?php if(has_post_thumbnail($post_item['ID'])): ?>
                                <div class="recent-post-thumb" style="background-image: url('<?php echo get_the_post_thumbnail_url($post_item['ID'], 'thumbnail'); ?>');"></div>
                            <?php else: ?>
                                <div class="recent-post-thumb default-thumb">🌿</div>
                            <?php endif; ?>
                            <div class="recent-post-info">
                                <h4><?php echo esc_html($post_item['post_title']); ?></h4>
                                <span class="recent-post-date"><?php echo get_the_date('', $post_item['ID']); ?></span>
                            </div>
                        </a>
                    </li>
                <?php endforeach; wp_reset_query(); ?>
            </ul>
        </div>
    </aside>
    <?php
	return;
}
?>

<aside id="secondary" class="widget-area premium-sidebar">
	<?php dynamic_sidebar( 'sidebar-1' ); ?>
</aside><!-- #secondary -->
