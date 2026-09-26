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
                <article id="post-<?php the_ID(); ?>" <?php post_class('card premium-tool-card'); ?> style="padding: 4rem; box-shadow: 0 30px 60px rgba(0,0,0,0.08); border: 1px solid rgba(255,255,255,0.8); background: rgba(255,255,255,0.95); backdrop-filter: blur(20px);">
                    
                    <header class="tool-header" style="text-align: center; margin-bottom: 3rem;">
                        <?php the_title( '<h1 class="entry-title" style="font-size: 3rem; background: linear-gradient(135deg, var(--color-primary), var(--color-accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">', '</h1>' ); ?>
                        <div class="tool-badge" style="display:inline-block; margin-top: 1rem; padding: 0.4rem 1.2rem; background: var(--color-gold); color: #fff; font-weight: bold; border-radius: 50px; font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase; box-shadow: 0 4px 15px rgba(212,175,55,0.3);">Premium Feature</div>
                    </header>

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
