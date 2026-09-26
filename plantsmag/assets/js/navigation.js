/**
 * PlantsMag - Navigation JavaScript
 *
 * @package PlantsMag
 */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
        const mobileMenu = document.getElementById('mobile-menu');
        const mobileMenuClose = document.querySelector('.mobile-menu-close');
        const mobileMenuLinks = document.querySelectorAll('.mobile-menu-list a');

        if (!mobileMenuToggle || !mobileMenu) return;

        // Toggle mobile menu
        const toggleMenu = (open) => {
            if (open) {
                mobileMenu.classList.add('is-open');
                mobileMenu.setAttribute('aria-hidden', 'false');
                mobileMenuToggle.setAttribute('aria-expanded', 'true');
                document.body.style.overflow = 'hidden';

                // Focus trap
                mobileMenuClose?.focus();
            } else {
                mobileMenu.classList.remove('is-open');
                mobileMenu.setAttribute('aria-hidden', 'true');
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }
        };

        // Event listeners
        mobileMenuToggle.addEventListener('click', function () {
            const isOpen = mobileMenu.classList.contains('is-open');
            toggleMenu(!isOpen);
        });

        mobileMenuClose?.addEventListener('click', function () {
            toggleMenu(false);
        });

        // Close menu when clicking a link
        mobileMenuLinks.forEach(link => {
            link.addEventListener('click', function () {
                toggleMenu(false);
            });
        });

        // Close on escape key
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && mobileMenu.classList.contains('is-open')) {
                toggleMenu(false);
            }
        });

        // Close on click outside
        document.addEventListener('click', function (e) {
            if (mobileMenu.classList.contains('is-open')) {
                if (!mobileMenu.contains(e.target) && !mobileMenuToggle.contains(e.target)) {
                    toggleMenu(false);
                }
            }
        });

        // Desktop dropdown accessibility
        const menuItemsWithChildren = document.querySelectorAll('.menu-item-has-children');

        menuItemsWithChildren.forEach(item => {
            const link = item.querySelector('a');
            const submenu = item.querySelector('.sub-menu');

            if (!link || !submenu) return;

            // Add dropdown indicator
            const indicator = document.createElement('span');
            indicator.className = 'dropdown-indicator';
            indicator.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>';
            link.appendChild(indicator);

            // Keyboard navigation
            link.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    const isExpanded = item.classList.contains('is-expanded');
                    item.classList.toggle('is-expanded');
                    link.setAttribute('aria-expanded', !isExpanded);
                }
            });

            // Mouse events
            item.addEventListener('mouseenter', function () {
                this.classList.add('is-expanded');
                link.setAttribute('aria-expanded', 'true');
            });

            item.addEventListener('mouseleave', function () {
                this.classList.remove('is-expanded');
                link.setAttribute('aria-expanded', 'false');
            });
        });
    });

})();
