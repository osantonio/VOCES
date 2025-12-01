document.addEventListener('DOMContentLoaded', function () {
    var themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
    var themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
    var themeToggleBtn = document.getElementById('theme-toggle');

    if (!themeToggleDarkIcon || !themeToggleLightIcon || !themeToggleBtn) {
        console.error('Dark mode toggle elements not found');
        return;
    }

    // Function to update icon visibility
    function updateIcons(isDark) {
        if (isDark) {
            // Dark mode active -> show sun icon (to switch to light)
            themeToggleLightIcon.style.display = 'inline-block';
            themeToggleDarkIcon.style.display = 'none';
        } else {
            // Light mode active -> show moon icon (to switch to dark)
            themeToggleDarkIcon.style.display = 'inline-block';
            themeToggleLightIcon.style.display = 'none';
        }
    }

    // Initial icon state based on current theme
    var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    updateIcons(isDark);

    themeToggleBtn.addEventListener('click', function () {
        // Toggle theme
        if (localStorage.getItem('theme')) {
            if (localStorage.getItem('theme') === 'light') {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                updateIcons(true);
            } else {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                updateIcons(false);
            }
        } else {
            if (document.documentElement.getAttribute('data-theme') === 'dark') {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                updateIcons(false);
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                updateIcons(true);
            }
        }
    });
});
