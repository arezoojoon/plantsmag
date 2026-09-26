/**
 * PlantsMag - Main JavaScript
 *
 * @package PlantsMag
 */

(function() {
    'use strict';

    // DOM Ready
    document.addEventListener('DOMContentLoaded', function() {
        PlantsMag.init();
    });

    // PlantsMag Namespace
    const PlantsMag = {
        init: function() {
            this.stickyHeader();
            this.backToTop();
            this.scrollAnimations();
            this.progressBars();
            this.portfolioFilters();
            this.smoothScroll();
            this.searchModal();
        },

        // Sticky Header
        stickyHeader: function() {
            const header = document.querySelector('.site-header');
            if (!header) return;

            const scrollThreshold = 50;

            const handleScroll = () => {
                if (window.scrollY > scrollThreshold) {
                    header.classList.add('is-scrolled');
                } else {
                    header.classList.remove('is-scrolled');
                }
            };

            window.addEventListener('scroll', handleScroll, { passive: true });
            handleScroll(); // Initial check
        },

        // Back to Top Button
        backToTop: function() {
            const button = document.getElementById('back-to-top');
            if (!button) return;

            const showThreshold = 300;

            const handleScroll = () => {
                if (window.scrollY > showThreshold) {
                    button.classList.add('is-visible');
                } else {
                    button.classList.remove('is-visible');
                }
            };

            button.addEventListener('click', function(e) {
                e.preventDefault();
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });

            window.addEventListener('scroll', handleScroll, { passive: true });
        },

        // Scroll Animations (Intersection Observer)
        scrollAnimations: function() {
            const animatedElements = document.querySelectorAll('[data-animate]');
            if (!animatedElements.length) return;

            const observerOptions = {
                root: null,
                rootMargin: '0px 0px -50px 0px',
                threshold: 0.1
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);

            animatedElements.forEach(el => observer.observe(el));
        },

        // Animated Progress Bars
        progressBars: function() {
            const progressBars = document.querySelectorAll('.pm-progress-fill');
            if (!progressBars.length) return;

            const observerOptions = {
                root: null,
                threshold: 0.5
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const progress = entry.target.dataset.progress;
                        entry.target.style.width = progress + '%';
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);

            progressBars.forEach(bar => observer.observe(bar));
        },

        // Portfolio Filters
        portfolioFilters: function() {
            const filterBtns = document.querySelectorAll('.pm-filter-btn');
            const portfolioItems = document.querySelectorAll('.pm-portfolio-item');

            if (!filterBtns.length || !portfolioItems.length) return;

            filterBtns.forEach(btn => {
                btn.addEventListener('click', function() {
                    const filter = this.dataset.filter;

                    // Update active button
                    filterBtns.forEach(b => b.classList.remove('active'));
                    this.classList.add('active');

                    // Filter items
                    portfolioItems.forEach(item => {
                        const categories = item.dataset.category || '';
                        
                        if (filter === '*' || categories.includes(filter)) {
                            item.style.display = 'block';
                            setTimeout(() => {
                                item.style.opacity = '1';
                                item.style.transform = 'scale(1)';
                            }, 10);
                        } else {
                            item.style.opacity = '0';
                            item.style.transform = 'scale(0.8)';
                            setTimeout(() => {
                                item.style.display = 'none';
                            }, 300);
                        }
                    });
                });
            });
        },

        // Smooth Scroll for Anchor Links
        smoothScroll: function() {
            const anchorLinks = document.querySelectorAll('a[href^="#"]:not([href="#"])');

            anchorLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    const targetId = this.getAttribute('href');
                    const targetElement = document.querySelector(targetId);

                    if (targetElement) {
                        e.preventDefault();
                        const headerHeight = document.querySelector('.site-header')?.offsetHeight || 0;
                        const targetPosition = targetElement.getBoundingClientRect().top + window.scrollY - headerHeight;

                        window.scrollTo({
                            top: targetPosition,
                            behavior: 'smooth'
                        });
                    }
                });
            });
        },

        // Search Modal
        searchModal: function() {
            const searchToggle = document.querySelector('[data-toggle="search-modal"]');
            const searchModal = document.getElementById('search-modal');
            const searchClose = searchModal?.querySelector('.search-modal-close');
            const searchOverlay = searchModal?.querySelector('.search-modal-overlay');
            const searchField = searchModal?.querySelector('.search-field');

            if (!searchToggle || !searchModal) return;

            const openModal = () => {
                searchModal.classList.add('is-open');
                searchModal.setAttribute('aria-hidden', 'false');
                document.body.style.overflow = 'hidden';
                setTimeout(() => {
                    searchField?.focus();
                }, 100);
            };

            const closeModal = () => {
                searchModal.classList.remove('is-open');
                searchModal.setAttribute('aria-hidden', 'true');
                document.body.style.overflow = '';
            };

            searchToggle.addEventListener('click', openModal);
            searchClose?.addEventListener('click', closeModal);
            searchOverlay?.addEventListener('click', closeModal);

            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && searchModal.classList.contains('is-open')) {
                    closeModal();
                }
            });
        }
    };

    // Expose to global scope
    window.PlantsMag = PlantsMag;

})();
