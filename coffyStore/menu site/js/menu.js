// Tab switching functionality
function openMenu(menuName) {
    // Hide all menu sections
    var sections = document.getElementsByClassName('menu-section');
    for (var i = 0; i < sections.length; i++) {
        sections[i].classList.remove('active');
    }
    
    // Remove active class from all tabs
    var tabs = document.getElementsByClassName('tab-btn');
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove('active');
    }
    
    // Show selected section and activate tab
    document.getElementById(menuName).classList.add('active');
    event.currentTarget.classList.add('active');
}

// Mobile menu functionality
document.addEventListener('DOMContentLoaded', function() {
    const menuOpen = document.getElementById('menu-open');
    const menuClose = document.getElementById('menu-close');
    const navbar = document.querySelector('.navbar');
    
    // Toggle mobile menu
    if (menuOpen && menuClose && navbar) {
        menuOpen.addEventListener('click', () => {
            navbar.style.display = 'flex';
            navbar.style.right = '0';
        });
        
        menuClose.addEventListener('click', () => {
            navbar.style.right = '-100%';
        });
        
        // Close menu when clicking on a link (optional)
        const navLinks = navbar.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navbar.style.right = '-100%';
            });
        });
    }
    
    // Add smooth scroll effect for better UX (optional)
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.style.cursor = 'pointer';
        item.addEventListener('click', function() {
            // Add visual feedback when item is clicked
            this.style.backgroundColor = '#f9f5f0';
            setTimeout(() => {
                this.style.backgroundColor = '';
            }, 300);
        });
    });
    
    // Set default active tab if none is active
    const activeTabs = document.querySelectorAll('.tab-btn.active');
    if (activeTabs.length === 0) {
        const defaultTab = document.querySelector('.tab-btn');
        if (defaultTab) {
            defaultTab.classList.add('active');
        }
    }
});