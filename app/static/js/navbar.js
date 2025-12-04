document.addEventListener('DOMContentLoaded', function () {
    var btn = document.getElementById('user-menu-button');
    var menu = document.getElementById('user-dropdown');

    if (!btn || !menu) {
        console.error('Navbar menu elements not found');
        return;
    }

    function openMenu() {
        menu.classList.remove('hidden');
        btn.setAttribute('aria-expanded', 'true');
        menu.style.opacity = '1';
        menu.style.transform = 'scale(1)';
    }

    function closeMenu() {
        menu.classList.add('hidden');
        btn.setAttribute('aria-expanded', 'false');
        menu.style.opacity = '0';
        menu.style.transform = 'scale(0.98)';
    }

    btn.addEventListener('click', function (e) {
        e.stopPropagation();
        if (menu.classList.contains('hidden')) {
            openMenu();
        } else {
            closeMenu();
        }
    });

    btn.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            openMenu();
            var firstItem = menu.querySelector('[role="menuitem"]');
            if (firstItem) firstItem.focus();
        } else if (e.key === 'Escape') {
            closeMenu();
        }
    });

    document.addEventListener('click', function (e) {
        if (!menu.contains(e.target) && e.target !== btn) {
            closeMenu();
        }
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            closeMenu();
        }
    });
});
