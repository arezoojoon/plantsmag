<?php
/**
 * Single Post Template
 *
 * @package PlantsMag
 */

get_header();
?>

<main id="primary" class="site-main single-post">
    <div class="pm-container">
        <div class="pm-content-wrapper">
            <div class="pm-content">
                <?php plantsmag_breadcrumbs(); ?>

                <?php
                while (have_posts()):
                    the_post();
                    ?>

                    <article id="post-<?php the_ID(); ?>" <?php post_class('pm-article'); ?>>
                        <!-- Post Header -->
                        <header class="pm-article-header">
                            <?php
                            $categories = get_the_category();
                            if ($categories):
                                ?>
                                <div class="pm-article-cats">
                                    <?php foreach (array_slice($categories, 0, 2) as $cat): ?>
                                        <a href="<?php echo esc_url(get_category_link($cat->term_id)); ?>"
                                            class="pm-article-cat">
                                            <?php echo esc_html($cat->name); ?>
                                        </a>
                                    <?php endforeach; ?>
                                </div>
                            <?php endif; ?>

                            <h1 class="pm-article-title"><?php the_title(); ?></h1>

                            <div class="pm-article-meta">
                                <div class="pm-article-author">
                                    <?php echo get_avatar(get_the_author_meta('ID'), 40); ?>
                                    <span>
                                        <?php esc_html_e('By', 'plantsmag'); ?>
                                        <a
                                            href="<?php echo esc_url(get_author_posts_url(get_the_author_meta('ID'))); ?>">
                                            <?php the_author(); ?>
                                        </a>
                                    </span>
                                </div>
                                <span class="pm-article-date"><?php plantsmag_posted_on(); ?></span>
                                <span class="pm-article-reading-time"><?php plantsmag_reading_time(); ?></span>
                            </div>
                        </header>

                        <!-- Featured Image -->
                        <?php if (has_post_thumbnail()): ?>
                            <div class="pm-article-featured">
                                <?php the_post_thumbnail('plantsmag-featured'); ?>
                            </div>
                        <?php endif; ?>

                        <!-- Post Content -->
                        <div class="pm-article-content entry-content">
                            <?php
                            the_content();

                            wp_link_pages(
                                array(
                                    'before' => '<div class="page-links">' . esc_html__('Pages:', 'plantsmag'),
                                    'after' => '</div>',
                                )
                            );
                            ?>
                        </div>

                        <!-- Post Footer -->
                        <footer class="pm-article-footer">
                            <?php
                            $tags = get_the_tags();
                            if ($tags):
                                ?>
                                <div class="pm-article-tags">
                                    <span class="pm-article-tags-label"><?php esc_html_e('Tags:', 'plantsmag'); ?></span>
                                    <?php foreach ($tags as $tag): ?>
                                        <a href="<?php echo esc_url(get_tag_link($tag->term_id)); ?>" class="pm-tag">
                                            <?php echo esc_html($tag->name); ?>
                                        </a>
                                    <?php endforeach; ?>
                                </div>
                            <?php endif; ?>

                            <!-- Social Share -->
                            <div class="pm-article-share">
                                <span class="pm-article-share-label"><?php esc_html_e('Share:', 'plantsmag'); ?></span>
                                <div class="pm-share-buttons">
                                    <a href="https://www.facebook.com/sharer/sharer.php?u=<?php echo urlencode(get_permalink()); ?>"
                                        target="_blank" rel="noopener noreferrer" class="pm-share-btn pm-share-facebook"
                                        aria-label="Share on Facebook">
                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                                            <path
                                                d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
                                        </svg>
                                    </a>
                                    <a href="https://twitter.com/intent/tweet?url=<?php echo urlencode(get_permalink()); ?>&text=<?php echo urlencode(get_the_title()); ?>"
                                        target="_blank" rel="noopener noreferrer" class="pm-share-btn pm-share-twitter"
                                        aria-label="Share on Twitter">
                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                                            <path
                                                d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
                                        </svg>
                                    </a>
                                    <a href="https://www.linkedin.com/shareArticle?mini=true&url=<?php echo urlencode(get_permalink()); ?>&title=<?php echo urlencode(get_the_title()); ?>"
                                        target="_blank" rel="noopener noreferrer" class="pm-share-btn pm-share-linkedin"
                                        aria-label="Share on LinkedIn">
                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                                            <path
                                                d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
                                        </svg>
                                    </a>
                                </div>
                            </div>
                        </footer>

                        <!-- Author Box -->
                        <div class="pm-author-box">
                            <div class="pm-author-avatar">
                                <?php echo get_avatar(get_the_author_meta('ID'), 80); ?>
                            </div>
                            <div class="pm-author-info">
                                <h4 class="pm-author-name">
                                    <a href="<?php echo esc_url(get_author_posts_url(get_the_author_meta('ID'))); ?>">
                                        <?php the_author(); ?>
                                    </a>
                                </h4>
                                <p class="pm-author-bio"><?php echo esc_html(get_the_author_meta('description')); ?></p>
                            </div>
                        </div>

                        <!-- Post Navigation -->
                        <nav class="pm-post-navigation">
                            <?php
                            $prev_post = get_previous_post();
                            $next_post = get_next_post();
                            ?>
                            <?php if ($prev_post): ?>
                                <a href="<?php echo esc_url(get_permalink($prev_post)); ?>"
                                    class="pm-post-nav-link pm-post-nav-prev">
                                    <span class="pm-post-nav-label">
                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                            stroke-width="2">
                                            <path d="M19 12H5M12 19l-7-7 7-7" />
                                        </svg>
                                        <?php esc_html_e('Previous', 'plantsmag'); ?>
                                    </span>
                                    <span
                                        class="pm-post-nav-title"><?php echo esc_html(get_the_title($prev_post)); ?></span>
                                </a>
                            <?php endif; ?>
                            <?php if ($next_post): ?>
                                <a href="<?php echo esc_url(get_permalink($next_post)); ?>"
                                    class="pm-post-nav-link pm-post-nav-next">
                                    <span class="pm-post-nav-label">
                                        <?php esc_html_e('Next', 'plantsmag'); ?>
                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                            stroke-width="2">
                                            <path d="M5 12h14M12 5l7 7-7 7" />
                                        </svg>
                                    </span>
                                    <span
                                        class="pm-post-nav-title"><?php echo esc_html(get_the_title($next_post)); ?></span>
                                </a>
                            <?php endif; ?>
                        </nav>

                    </article>

                    <?php
                    // Comments
                    if (comments_open() || get_comments_number()):
                        comments_template();
                    endif;

                endwhile;
                ?>
            </div>

            <?php get_sidebar(); ?>
        </div>
    </div>
</main>

<?php
get_footer();
