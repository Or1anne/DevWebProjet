(function () {
    const savedTheme = localStorage.getItem('theme');
    const isDark = savedTheme === 'dark';

    if (isDark) {
        document.documentElement.classList.add('dark-mode');
    }

    // Met à jour le texte du bouton selon le thème enregistré
    document.addEventListener('DOMContentLoaded', () => {
        const toggleButton = document.querySelector('.themeToggle');
        if (toggleButton) {
            toggleButton.textContent = isDark ? 'Mode Clair' : 'Mode Sombre';
        }
    });
})();

document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.querySelector('.themeToggle');

    if (toggleButton) {
        toggleButton.addEventListener('click', () => {
            document.documentElement.classList.toggle('dark-mode');
            const isDarkMode = document.documentElement.classList.contains('dark-mode');

            // Met à jour le texte du bouton
            toggleButton.textContent = isDarkMode ? 'Mode Clair' : 'Mode Sombre';

            // Sauvegarde dans le localStorage
            localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
        });
    }
});
