<?php
/**
 * Template Name: Smart Tool Page
 *
 * A specialized template for displaying SaaS-like tools without distractions.
 *
 * @package PlantsMag_Premium
 */

get_header();
?>

<div class="tool-page-wrapper" style="background: linear-gradient(135deg, var(--color-bg-light) 0%, #ffffff 100%); min-height: calc(100vh - 80px); padding: 4rem 0;">
    <div class="container" style="max-width: 900px;">
        <?php
        while ( have_posts() ) :
            the_post();
            ?>
            <main id="primary" class="site-main">
                <article id="post-<?php the_ID(); ?>" <?php post_class('card premium-tool-card'); ?> style="padding: 1.5rem 1rem; box-shadow: 0 30px 60px rgba(0,0,0,0.08); border: 1px solid rgba(255,255,255,0.8); background: rgba(255,255,255,0.95); backdrop-filter: blur(20px);">


                    <div class="entry-content tool-content" style="font-size: 1.15rem; line-height: 1.8;">
                        <?php
                        the_content();
                        ?>
                    </div>
                </article>
            </main>
            <?php
        endwhile;
        ?>
    </div>
</div>

<?php
get_footer();
