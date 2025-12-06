document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();

    // Mobile Menu Toggle
    const mobileMenuButton = document.getElementById('mobileMenuButton');
    const mobileMenu = document.getElementById('mobile-menu');

    function toggleMobileMenu() {
        if (mobileMenu && mobileMenuButton) {
            mobileMenu.classList.toggle('hidden');
            mobileMenu.classList.toggle('block');
            const icons = mobileMenuButton.querySelectorAll('.current-icon');
            icons.forEach(icon => icon.classList.toggle('hidden'));
        }
    }
    
    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', toggleMobileMenu);
    }

    // User Profile Dropdown Toggle
    const userMenuButton = document.getElementById('user-menu-button');
    const userProfileDropdown = document.getElementById('userProfileDropdown');

    if (userMenuButton && userProfileDropdown) {
        userMenuButton.addEventListener('click', () => {
            const isExpanded = userMenuButton.getAttribute('aria-expanded') === 'true' || false;
            userMenuButton.setAttribute('aria-expanded', String(!isExpanded));
            userProfileDropdown.classList.toggle('hidden');
        });
        
        document.addEventListener('click', (event) => {
            if (userProfileDropdown && !userProfileDropdown.classList.contains('hidden') && 
                userMenuButton && !userMenuButton.contains(event.target) && 
                !userProfileDropdown.contains(event.target)) {
                userProfileDropdown.classList.add('hidden');
                userMenuButton.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // Set current year in footer
    const currentYearEl = document.getElementById('currentYear');
    if (currentYearEl) {
        currentYearEl.textContent = new Date().getFullYear();
    }
});