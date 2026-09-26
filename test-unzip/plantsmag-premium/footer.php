<?php
/**
 * The premium footer for our theme
 *
 * @package PlantsMag_Premium
 */
?>

</div><!-- #page -->

<footer class="site-footer">
    <div class="container footer-grid">
        <div class="footer-brand">
            <div class="footer-logo">Plants<span class="text-accent">Mag</span></div>
            <p style="margin-top: 1.5rem; max-width: 300px; color: rgba(255,255,255,0.6); font-size: 1.05rem;">
                Your premium destination for expert houseplant care, smart watering tools, and AI plant health diagnosis.
            </p>
        </div>
        
        <div class="footer-links">
            <h3 class="footer-title">Smart Tools</h3>
            <ul>
                <li><a href="<?php echo esc_url(home_url('/watering-calculator')); ?>">Watering Calculator</a></li>
                <li><a href="<?php echo esc_url(home_url('/plant-disease-finder')); ?>">AI Disease Finder</a></li>
                <li><a href="<?php echo esc_url(home_url('/blog')); ?>">Plant Care Guides</a></li>
            </ul>
        </div>
        
        <div class="footer-links">
            <h3 class="footer-title">Legal</h3>
            <ul>
                <li><a href="<?php echo esc_url(home_url('/about-us')); ?>">About Us</a></li>
                <li><a href="<?php echo esc_url(home_url('/affiliate-disclosure')); ?>">Affiliate Disclosure</a></li>
                <li><a href="<?php echo esc_url(home_url('/privacy-policy')); ?>">Privacy Policy</a></li>
            </ul>
        </div>
    </div>
    
    <div class="container">
        <div class="footer-disclosure" style="text-align: center; margin-top: 2rem; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem;">
            <div class="engineered-wrapper">
                🚀 Engineered to Perfection by <a href="https://artinwebs.com/" target="_blank" class="artinwebs-box">ARTINWEBS</a>
            </div>
            <p style="margin-top: 1.5rem; color: rgba(255,255,255,0.4); font-size: 0.9rem;">
                &copy; <?php echo date('Y'); ?> <?php bloginfo('name'); ?>. Elevating Houseplant Care Globally.
            </p>
        </div>
    </div>
</footer>

<script>
// Smart Sticky Header & Reading Progress Logic
document.addEventListener('DOMContentLoaded', () => {
    let lastScrollY = window.scrollY;
    const header = document.querySelector('.site-header');
    const progressBar = document.getElementById('reading-progress');
    
    window.addEventListener('scroll', () => {
        // Sticky Header Logic
        if (window.scrollY > lastScrollY && window.scrollY > 100) {
            header.classList.add('scroll-down');
            header.classList.remove('scroll-up');
        } else {
            header.classList.add('scroll-up');
            header.classList.remove('scroll-down');
        }
        lastScrollY = window.scrollY;

        // Reading Progress Logic
        if(progressBar) {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            progressBar.style.width = scrolled + "%";
        }
    });

    // Simple reveal animation via Intersection Observer
    const observerItems = document.querySelectorAll('.pm-tool-card, .affiliate-box, .hero-content');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if(entry.isIntersecting) {
                entry.target.classList.add('animate-fade-up');
            }
        });
    });
    observerItems.forEach(item => {
        item.style.opacity = '0';
        observer.observe(item);
    });
});
</script>

<?php wp_footer(); ?>
</body>
</html>
