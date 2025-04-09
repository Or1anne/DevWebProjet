
(function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark-mode');
    }
})();

document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementsByClassName('themeToggle');

    if (toggleButton[0]) {
        toggleButton[0].addEventListener('click', () => {
            document.documentElement.classList.toggle('dark-mode');
            // Sauvegarde le thème dans le localStorage
            const isDarkMode = document.documentElement.classList.contains('dark-mode');
            localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
        });
    }
    });
