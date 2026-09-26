<?php
/**
 * Premium Front Page Template — PlantsMag v4.0
 * Full professional redesign: Hero, Tools, Stats, Blog, CTA
 *
 * @package PlantsMag_Premium
 */

get_header();
?>

<main id="primary" class="site-main">

    <!-- ═══════════════════════════════════════════════
         HERO SECTION — Split Layout with Parallax
    ═══════════════════════════════════════════════ -->
    <section class="hero-section" id="hero">
        <div class="hero-bg-orb hero-orb-1"></div>
        <div class="hero-bg-orb hero-orb-2"></div>
        <div class="container hero-inner">
            <div class="hero-content">
                <div class="hero-badge">
                    <span class="badge-dot"></span>
                    Free AI-Powered Plant Care Tools
                </div>
                <h1 class="hero-title">
                    Keep Every Plant
                    <span class="hero-title-gradient">Alive & Thriving.</span>
                </h1>
                <p class="hero-subtitle">
                    Stop the guesswork. Use our free AI tools to get exact watering schedules, instant disease diagnosis, and expert care guides — all in one place.
                </p>
                <div class="hero-actions">
                    <a href="<?php echo esc_url( home_url( '/watering-calculator' ) ); ?>" class="btn btn-primary btn-lg">
                        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
                        Watering Calculator
                    </a>
                    <a href="<?php echo esc_url( home_url( '/plant-disease-finder' ) ); ?>" class="btn btn-ghost btn-lg">
                        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
                        AI Disease Finder
                    </a>
                </div>
                <div class="hero-trust-row">
                    <div class="hero-trust-item">
                        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                        Free Forever
                    </div>
                    <div class="hero-trust-item">
                        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                        AI-Powered by Gemini
                    </div>
                    <div class="hero-trust-item">
                        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                        No Registration
                    </div>
                </div>
            </div>
            <div class="hero-visual">
                <div class="hero-img-frame">
                    <img
                        src="<?php echo esc_url( get_template_directory_uri() . '/assets/hero-plant.webp' ); ?>"
                        alt="Beautiful healthy monstera plant on a bright windowsill"
                        class="hero-plant-img"
                        loading="eager"
                    >
                    <!-- Floating Badge -->
                    <div class="hero-float-badge float-1">
                        <span class="float-icon">💧</span>
                        <div>
                            <strong>Water in 3 days</strong>
                            <small>Monstera Deliciosa</small>
                        </div>
                    </div>
                    <div class="hero-float-badge float-2">
                        <span class="float-icon">🌿</span>
                        <div>
                            <strong>Healthy Plant!</strong>
                            <small>AI Diagnosis</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>



    <!-- ═══════════════════════════════════════════════
         TOOLS SECTION — Premium Interactive Cards
    ═══════════════════════════════════════════════ -->
    <section class="tools-showcase-section" id="tools">
        <div class="container">
            <div class="section-header text-center">
                <span class="section-eyebrow">Free AI Tools</span>
                <h2 class="section-title">Smart Tools Built for Plant Parents</h2>
                <p class="section-subtitle">Professional-grade plant care tools, completely free. No app download needed.</p>
            </div>

            <div class="tools-grid">
                <!-- Tool 1: Watering Calculator -->
                <div class="tool-showcase-card tool-water">
                    <div class="tool-card-glow"></div>
                    <div class="tool-card-header">
                        <div class="tool-icon-wrap tool-icon-green">
                            <svg width="32" height="32" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
                        </div>
                        <div class="tool-badge">Free Tool</div>
                    </div>
                    <h3 class="tool-card-title">Smart Watering Calculator</h3>
                    <p class="tool-card-desc">Select your plant, pot type, and light conditions. Get a precise watering schedule tailored to your exact environment.</p>
                    <ul class="tool-feature-list">
                        <li><svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> 15+ Plant Species</li>
                        <li><svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Pot & Light Modifiers</li>
                        <li><svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Instant Schedule Output</li>
                    </ul>
                    <a href="<?php echo esc_url( home_url( '/watering-calculator' ) ); ?>" class="btn btn-primary tool-cta-btn">
                        Calculate My Schedule
                        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                    </a>
                </div>

                <!-- Tool 2: Disease Finder -->
                <div class="tool-showcase-card tool-ai">
                    <div class="tool-card-glow tool-glow-gold"></div>
                    <div class="tool-card-header">
                        <div class="tool-icon-wrap tool-icon-gold">
                            <svg width="32" height="32" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                        </div>
                        <div class="tool-badge tool-badge-ai">✨ AI Powered</div>
                    </div>
                    <h3 class="tool-card-title" style="color: var(--color-gold)">AI Plant Doctor</h3>
                    <p class="tool-card-desc">Upload a photo of your sick plant. Our Gemini AI analyzes the image, identifies diseases & pests, and recommends treatment in seconds.</p>
                    <ul class="tool-feature-list">
                        <li><svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Powered by Google Gemini AI</li>
                        <li><svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Instant Photo Analysis</li>
                        <li><svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Treatment Recommendations</li>
                    </ul>
                    <a href="<?php echo esc_url( home_url( '/plant-disease-finder' ) ); ?>" class="btn btn-gold tool-cta-btn">
                        Diagnose My Plant
                        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- ═══════════════════════════════════════════════
         LATEST GUIDES — Blog Grid
    ═══════════════════════════════════════════════ -->
    <section class="blog-preview-section" id="guides">
        <div class="container">
            <div class="section-header-flex">
                <div>
                    <span class="section-eyebrow">Expert Knowledge</span>
                    <h2 class="section-title">Latest Plant Care Guides</h2>
                </div>
                <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="btn btn-ghost-green view-all-btn">
                    View All Guides
                    <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </a>
            </div>

            <div class="blog-grid">
                <?php
                $query = new WP_Query( array(
                    'posts_per_page' => 6,
                    'post_status'    => 'publish',
                    'orderby'        => 'date',
                    'order'          => 'DESC',
                ) );

                if ( $query->have_posts() ) :
                    while ( $query->have_posts() ) : $query->the_post();
                        $categories = get_the_category();
                        $cat_name = ! empty( $categories ) ? esc_html( $categories[0]->name ) : 'Plant Care';
                        $word_count = str_word_count( strip_tags( get_the_content() ) );
                        $read_time = max( 1, round( $word_count / 200 ) );
                ?>
                <article class="blog-card">
                    <a href="<?php the_permalink(); ?>" class="blog-card-img-wrap">
                        <?php if ( has_post_thumbnail() ) : ?>
                            <?php the_post_thumbnail( 'medium_large', [ 'class' => 'blog-card-img', 'loading' => 'lazy' ] ); ?>
                        <?php else : ?>
                            <div class="blog-card-img blog-card-img-placeholder">
                                <svg width="48" height="48" fill="none" stroke="rgba(42,123,76,0.3)" stroke-width="1.5" viewBox="0 0 24 24"><path d="M12 22V12M12 12C12 12 9 9 6 9C3 9 2 12 2 12C2 12 2 18 6 20.5C8 21.7 10 22 12 22M12 12C12 12 15 9 18 9C21 9 22 12 22 12C22 12 22 18 18 20.5C16 21.7 14 22 12 22M12 12V2"/></svg>
                            </div>
                        <?php endif; ?>
                        <div class="blog-card-cat"><?php echo $cat_name; ?></div>
                    </a>
                    <div class="blog-card-body">
                        <div class="blog-card-meta">
                            <span><?php echo get_the_date( 'M j, Y' ); ?></span>
                            <span class="meta-dot">·</span>
                            <span><?php echo $read_time; ?> min read</span>
                        </div>
                        <h3 class="blog-card-title">
                            <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                        </h3>
                        <a href="<?php the_permalink(); ?>" class="blog-card-link">
                            Read Guide
                            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                        </a>
                    </div>
                </article>
                <?php
                    endwhile;
                    wp_reset_postdata();
                endif;
                ?>
            </div>
        </div>
    </section>

    <!-- ═══════════════════════════════════════════════
         HOW IT WORKS — 3 Steps
    ═══════════════════════════════════════════════ -->
    <section class="how-section">
        <div class="container">
            <div class="section-header text-center">
                <span class="section-eyebrow">Simple Process</span>
                <h2 class="section-title">Plant Care Made Effortless</h2>
            </div>
            <div class="steps-grid">
                <div class="step-card">
                    <div class="step-number">01</div>
                    <div class="step-icon">📸</div>
                    <h3>Upload or Select</h3>
                    <p>Take a photo of your plant or select your species — from tropicals and succulents to ferns and cacti.</p>
                </div>
                <div class="step-connector"></div>
                <div class="step-card">
                    <div class="step-number">02</div>
                    <div class="step-icon">🤖</div>
                    <h3>AI Analyzes</h3>
                    <p>Our Gemini AI instantly processes the data — identifying diseases, deficiencies, and optimal care routines.</p>
                </div>
                <div class="step-connector"></div>
                <div class="step-card">
                    <div class="step-number">03</div>
                    <div class="step-icon">🌱</div>
                    <h3>Your Plant Thrives</h3>
                    <p>Follow the personalized schedule and treatment plan. Watch your plants grow healthier every week.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- ═══════════════════════════════════════════════
         NEWSLETTER / LEAD CAPTURE
    ═══════════════════════════════════════════════ -->
    <section class="newsletter-section">
        <div class="container">
            <div class="newsletter-card">
                <div class="newsletter-bg-orb"></div>
                <div class="newsletter-content">
                    <div class="newsletter-badge">📗 Free eBook</div>
                    <h2>The Ultimate Houseplant Survival Guide</h2>
                    <p>Get our 30-page PDF covering light, water, and soil requirements for the 50 most popular indoor plants — absolutely free.</p>
                    <form class="newsletter-form" action="#" method="POST" id="pm-newsletter-form">
                        <div class="newsletter-input-wrap">
                            <svg class="newsletter-input-icon" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                            <input type="email" id="pm-email-input" placeholder="Enter your email address..." required>
                        </div>
                        <button type="submit" class="btn btn-gold btn-lg">Get Free PDF →</button>
                    </form>
                    <p class="newsletter-disclaimer">🔒 No spam. Unsubscribe anytime. We respect your privacy.</p>
                </div>
                <div class="newsletter-visual">
                    <div class="ebook-mockup">
                        <div class="ebook-cover">
                            <div class="ebook-icon">🌿</div>
                            <div class="ebook-title">Houseplant<br>Survival Guide</div>
                            <div class="ebook-sub">PlantsMag Edition</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

</main><!-- #main -->

<?php
get_footer();
?>
