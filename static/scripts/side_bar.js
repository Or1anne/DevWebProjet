function toggleBurgerMenu() {
    const menu = document.getElementById('mobileMenu');
    const burger = document.getElementById('burgerBtn');

    menu.classList.toggle('open');

    if (menu.classList.contains('open')) {
        burger.style.display = 'none';
    } else {
        burger.style.display = 'block';
    }
}