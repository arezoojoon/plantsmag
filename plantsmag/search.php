<?php
/**
 * Search Results Template
 *
 * @package PlantsMag
 */

get_header();
?>

<main id="primary" class="site-main search-results">
    <!-- Search Header -->
    <div class="pm-archive-header pm-search-header">
        <div class="pm-container">
            <?php plantsmag_breadcrumbs(); ?>
            <h1 class="pm-archive-title">
                <?php
                printf(
                    /* translators: %s: search query */
                    esc_html__('Search Results for: %s', 'plantsmag'),
                    '<span>' . get_search_query() . '</span>'
                );
                ?>
            </h1>
            <p class="pm-search-count">
                <?php
                global $wp_query;
                printf(
                    /* translators: %d: number of results */
                    esc_html(_n('%d result found', '%d results found', $wp_query->found_posts, 'plantsmag')),
                    $wp_query->found_posts
                );
                ?>
            </p>
        </div>
    </div>

    <div class="pm-container">
        <div class="pm-content-wrapper">
            <div class="pm-content">
                <?php if (have_posts()): ?>

                    <div class="pm-posts-list">
                        <?php
                        while (have_posts()):
                            the_post();
                            get_template_part('template-parts/content/content', 'search');
                        endwhile;
                        ?>
                    </div>

                    <?php plantsmag_pagination(); ?>

                <?php else: ?>

                    <div class="pm-no-results">
                        <div class="pm-no-results-icon">
                            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                stroke-width="1.5">
                                <circle cx="11" cy="11" r="8" />
                                <path d="M21 21l-4.35-4.35" />
                            </svg>
                        </div>
                        <h2><?php esc_html_e('Nothing Found', 'plantsmag'); ?></h2>
                        <p><?php esc_html_e('Sorry, but nothing matched your search terms. Please try again with some different keywords.', 'plantsmag'); ?>
                        </p>
                        <div class="pm-no-results-search">
                            <?php get_search_form(); ?>
                        </div>
                    </div>

                <?php endif; ?>
            </div>

            <?php get_sidebar(); ?>
        </div>
    </div>
</main>

<?php
get_footer();
