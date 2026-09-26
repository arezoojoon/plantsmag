<?php
/**
 * Premium Footer Template — PlantsMag v4.0
 *
 * @package PlantsMag_Premium
 */
?>

</div><!-- #page -->

<footer class="site-footer">
    <div class="container footer-grid">
        <div class="footer-brand">
            <div class="footer-logo">Plants<span class="text-accent">Mag</span></div>
            <p style="margin-top: 1.5rem; max-width: 300px; color: rgba(255,255,255,0.7); font-size: 1.05rem; line-height: 1.6;">
                Your premium destination for expert houseplant care, smart watering tools, and AI plant health diagnosis.
            </p>
        </div>
        
        <div class="footer-links">
            <h3 class="footer-title">Smart Tools</h3>
            <ul>
                <li><a href="<?php echo esc_url(home_url('/watering-calculator')); ?>">Watering Calculator</a></li>
                <li><a href="<?php echo esc_url(home_url('/plant-disease-finder')); ?>">AI Disease Finder</a></li>
                <li><a href="<?php echo esc_url(home_url('/plant-guides')); ?>">Plant Care Guides</a></li>
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
        <div class="footer-disclosure">
            <div class="engineered-wrapper">
                🚀 Engineered to Perfection by <a href="https://artinwebs.com/" target="_blank" class="artinwebs-box">ARTINWEBS</a>
            </div>
            <p style="margin-top: 1.5rem; color: rgba(255,255,255,0.4); font-size: 0.9rem;">
                &copy; <?php echo date('Y'); ?> PlantsMag. Elevating Houseplant Care Globally.
            </p>
        </div>
    </div>
</footer>

<script>
document.addEventListener('DOMContentLoaded', () => {
    // 1. Smart Sticky Header & Reading Progress
    let lastScrollY = window.scrollY;
    const header = document.querySelector('.site-header');
    const progressBar = document.getElementById('reading-progress');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > lastScrollY && window.scrollY > 100) {
            header.classList.add('scroll-down');
            header.classList.remove('scroll-up');
        } else {
            header.classList.add('scroll-up');
            header.classList.remove('scroll-down');
        }
        lastScrollY = window.scrollY;

        if (progressBar) {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            progressBar.style.width = scrolled + "%";
        }
    }, { passive: true });

    // 2. Mobile Navigation Toggle
    const hamburger = document.getElementById('nav-hamburger');
    const drawer = document.getElementById('mobile-nav-drawer');
    const overlay = document.getElementById('mobile-nav-overlay');

    if (hamburger && drawer && overlay) {
        const toggleMenu = () => {
            const isActive = drawer.classList.contains('active');
            hamburger.setAttribute('aria-expanded', !isActive);
            drawer.classList.toggle('active');
            overlay.classList.toggle('active');
            document.body.style.overflow = isActive ? '' : 'hidden'; // Prevent background scrolling
        };

        hamburger.addEventListener('click', toggleMenu);
        overlay.addEventListener('click', toggleMenu);
    }

    // 3. Number Counter Animation for Stats
    const statsSection = document.querySelector('.stats-section');
    if (statsSection) {
        const counters = document.querySelectorAll('.stat-number');
        let animated = false;

        const animateCounters = () => {
            counters.forEach(counter => {
                const target = +counter.getAttribute('data-target');
                const duration = 2000; // 2 seconds
                const increment = target / (duration / 16); // 60fps

                const updateCount = () => {
                    const current = +counter.innerText.replace(/,/g, '');
                    if (current < target) {
                        counter.innerText = Math.ceil(current + increment).toLocaleString();
                        requestAnimationFrame(updateCount);
                    } else {
                        counter.innerText = target.toLocaleString();
                    }
                };
                updateCount();
            });
            animated = true;
        };

        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting && !animated) {
                animateCounters();
            }
        });
        observer.observe(statsSection);
    }
});
</script>

<?php wp_footer(); ?>
<!-- App Bottom Navigation (Mobile Only) -->
<nav class="pm-bottom-nav">
    <a href="/" class="pm-nav-item <?php echo is_front_page() ? 'active' : ''; ?>">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
        <span>Home</span>
    </a>
    <a href="/watering-calculator/" class="pm-nav-item <?php echo (is_page('watering-calculator')) ? 'active' : ''; ?>">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>
        </svg>
        <span>Watering</span>
    </a>
    <a href="/plant-disease-finder/" class="pm-nav-item <?php echo (is_page('plant-disease-finder')) ? 'active' : ''; ?>">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
        </svg>
        <span>AI Doctor</span>
    </a>
    <a href="/plant-guides/" class="pm-nav-item <?php echo (is_category() || is_single() || is_page('plant-guides')) ? 'active' : ''; ?>">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
            <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
            <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
        </svg>
        <span>Guides</span>
    </a>
</nav>
</body>
</html>
