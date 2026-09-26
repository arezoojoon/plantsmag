<?php
/**
 * The premium landing page template
 *
 * @package PlantsMag_Premium
 */

get_header();
?>

<main id="primary" class="site-main">

    <!-- Premium Hero Section -->
    <section class="hero-section container">
        <div class="hero-content">
            <span class="hero-tagline">Trusted by 10,000+ Plant Parents</span>
            <h1>Keep Your Houseplants Thriving, 
                <br>
                <span style="background: linear-gradient(135deg, var(--color-primary-light) 0%, var(--color-accent) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Effortlessly.</span>
            </h1>
            <p style="font-size: 1.3rem; max-width: 600px; color: var(--color-text-muted); margin-bottom: 3rem;">
                Stop the guesswork. Use our Smart Watering Calculator and AI Plant Doctor to give your indoor jungle exactly what it needs.
            </p>
            <div style="display:flex; gap: 1.5rem; flex-wrap: wrap;">
                <a href="<?php echo esc_url( home_url( '/watering-calculator' ) ); ?>" class="btn btn-primary">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path></svg>
                    Watering Calculator
                </a>
                <a href="<?php echo esc_url( home_url( '/plant-disease-finder' ) ); ?>" class="btn btn-outline">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
                    AI Disease Scanner
                </a>
            </div>
        </div>
        <!-- Unsplash high quality plant image via URL -->
        <img src="https://images.unsplash.com/photo-1416879598555-220000000000?q=80&w=1200&auto=format&fit=crop" alt="Premium Monstera Plant" class="hero-img">
    </section>

    <!-- Glassmorphic Tools Section -->
    <section class="tools-section container">
        <div class="text-center" style="margin-bottom: 5rem;">
            <h2>Powerful Tools. <span style="color: var(--color-primary-light);">Zero Cost.</span></h2>
            <p style="max-width: 600px; margin: 0 auto; color: var(--color-text-muted);">We built the tools we wished we had. Instant access, directly from your browser.</p>
        </div>

        <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));">
            <!-- Tool 1 -->
            <a href="<?php echo esc_url( home_url( '/watering-calculator' ) ); ?>" class="pm-tool-card">
                <div class="tool-icon" style="color: var(--color-primary-light); background: rgba(42, 123, 76, 0.1);">
                    <svg width="32" height="32" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path></svg>
                </div>
                <h3>Smart Watering Calculator</h3>
                <p style="color: var(--color-text-muted);">Select your plant species, pot size, and lighting conditions. Get an exact watering schedule tailored to your environment.</p>
                <span style="color: var(--color-primary-light); font-weight: bold; margin-top: 1rem; display: inline-block;">Calculate Now &rarr;</span>
            </a>
            
            <!-- Tool 2 -->
            <a href="<?php echo esc_url( home_url( '/plant-disease-finder' ) ); ?>" class="pm-tool-card" style="border-color: rgba(212, 175, 55, 0.3);">
                <div class="tool-icon" style="color: var(--color-gold); background: rgba(212, 175, 55, 0.1);">
                    <svg width="32" height="32" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><path d="M3.27 6.96L12 12.01l8.73-5.05"></path><path d="M12 22.08V12"></path></svg>
                </div>
                <h3 style="color: var(--color-gold);">AI Plant Doctor</h3>
                <p style="color: var(--color-text-muted);">Snap a picture of yellowing leaves or weird spots. Our AI detects pests and fungal diseases in seconds, and tells you what to buy.</p>
                <span style="color: var(--color-gold); font-weight: bold; margin-top: 1rem; display: inline-block;">Scan Plant &rarr;</span>
            </a>
        </div>
    </section>

    <!-- Latest Guides Section (Blog) -->
    <section class="tools-section container mt-4">
        <h2 class="mb-4">Latest Plant Guides</h2>
        <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));">
            <?php
            $query = new WP_Query( array(
                'posts_per_page' => 3,
                'post_status'    => 'publish',
            ) );

            if ( $query->have_posts() ) :
                while ( $query->have_posts() ) : $query->the_post();
                    ?>
                    <article class="glass-panel" style="padding: 0; overflow: hidden; border: none; background: #fff;">
                        <?php if(has_post_thumbnail()): ?>
                            <a href="<?php the_permalink(); ?>">
                                <?php the_post_thumbnail('medium_large', ['style' => 'width:100%; height:200px; object-fit:cover; transition: transform 0.5s;']); ?>
                            </a>
                        <?php endif; ?>
                        <div style="padding: 2rem;">
                            <h3 style="font-size: 1.5rem; margin-bottom: 1rem;"><a href="<?php the_permalink(); ?>" style="color: var(--color-text-title);"><?php the_title(); ?></a></h3>
                            <a href="<?php the_permalink(); ?>" style="font-weight: 600; font-size: 0.9rem;">Read Complete Guide &rarr;</a>
                        </div>
                    </article>
                    <?php
                endwhile;
                wp_reset_postdata();
            endif;
            ?>
        </div>
    </section>

    <!-- Premium Lead Capture -->
    <section class="container">
        <div class="lead-capture-section">
            <div class="lead-content">
                <span class="hero-tagline" style="background: rgba(255,255,255,0.2); color: #fff;">Free eBook</span>
                <h2 style="font-size: 2.5rem; margin-bottom: 1rem;">The Ultimate Houseplant Survival Guide</h2>
                <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 0;">Get our 30-page PDF checklist covering light, water, and soil requirements for the 50 most popular indoor plants.</p>
            </div>
            <div style="width: 100%; max-width: 450px;">
                <form class="lead-form" action="#" method="POST">
                    <input type="email" placeholder="Enter your email address..." required>
                    <button type="submit" class="btn btn-gold">Send PDF</button>
                </form>
                <p style="font-size: 0.8rem; opacity: 0.6; text-align: center; margin-top: 1rem;">No spam. Unsubscribe anytime.</p>
            </div>
        </div>
    </section>

</main><!-- #main -->

<?php
get_footer();
