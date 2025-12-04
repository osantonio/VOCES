document.addEventListener('DOMContentLoaded', function () {
    var sidebar = document.getElementById('app-sidebar');
    var overlay = document.getElementById('sidebar-overlay');
    var toggleBtn = document.getElementById('sidebar-toggle');
    var content = document.getElementById('content-wrapper');

    if (!sidebar || !toggleBtn || !content) {
        console.error('Sidebar elements not found');
        return;
    }

    function isDesktop() {
        return window.matchMedia('(min-width: 768px)').matches;
    }

    function persist(state) {
        try {
            localStorage.setItem('sidebar-open', state ? 'true' : 'false');
        } catch (e) {}
    }

    function showOverlay(show) {
        if (!overlay) return;
        if (show) {
            overlay.classList.remove('hidden');
        } else {
            overlay.classList.add('hidden');
        }
    }

    function openSidebar() {
        sidebar.classList.remove('-translate-x-full');
        sidebar.classList.add('translate-x-0');
        content.classList.add('md:ml-64');
        showOverlay(!isDesktop());
        persist(true);
    }

    function closeSidebar() {
        sidebar.classList.add('-translate-x-full');
        sidebar.classList.remove('translate-x-0');
        content.classList.remove('md:ml-64');
        showOverlay(false);
        persist(false);
    }

    var stored = null;
    try {
        stored = localStorage.getItem('sidebar-open');
    } catch (e) {}
    if (stored === 'true') {
        openSidebar();
    } else {
        closeSidebar();
    }

    toggleBtn.addEventListener('click', function () {
        if (sidebar.classList.contains('translate-x-0')) {
            closeSidebar();
        } else {
            openSidebar();
        }
    });

    if (overlay) {
        overlay.addEventListener('click', function () {
            closeSidebar();
        });
    }

    window.addEventListener('resize', function () {
        if (sidebar.classList.contains('translate-x-0')) {
            showOverlay(!isDesktop());
        }
    });
});
