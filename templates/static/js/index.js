function solve() {
    document.getElementById('menu-btn-small').addEventListener('click', toggleNavigationMenu);
    const navigationMenuAsideElement = document.getElementById('side-menu-mobile');

    function toggleNavigationMenu(e) {
        e.preventDefault()

        if (Array.from(navigationMenuAsideElement.classList).includes('collapse')) {
            navigationMenuAsideElement.classList.remove('collapse');
        } else {
            addHiddenClassToNavMenuAsideElement();
        }
    }

    function addHiddenClassToNavMenuAsideElement() {
        navigationMenuAsideElement.classList.add('collapse');
    }

}

window.onload = solve()