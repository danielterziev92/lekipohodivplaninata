const asideMenuStyle = document.querySelector('.side-menu-mobile');
const headerElement = document.getElementById('main-header');

window.addEventListener('scroll', () => {
    headerElement.classList.toggle('sticky', window.scrollY > 0);
});

document.getElementById('menu-btn-small').addEventListener('click', showHideAsideBarMenu)

function showHideAsideBarMenu(e) {
    e.preventDefault();

    const iElement = e.currentTarget.children[0];
    const sideMenuElement = document.getElementById('side-menu-mobile');
    const backgroundElement = sideMenuElement.querySelector('.background');

    if (sideMenuElement.classList.contains('collapse')) {
        showAsideBarMenu();
    } else {
        hideAsideBarMenu();
    }

    function showAsideBarMenu() {
        asideMenuStyle.style.top = `${window.scrollY.toFixed(0)}px`;
        sideMenuElement.classList.remove('collapse');
        backgroundElement.style.width = '100vw';
        backgroundElement.addEventListener('click', hideAsideBarMenu);
        iElement.classList.replace('fa-bars', 'fa-times');

        toggleBodyStyle()

        const allAElement = document.querySelectorAll('.side-menu-mobile > ul > li');
        checkElementForSubMenus(allAElement)

    }

    function hideAsideBarMenu() {
        sideMenuElement.classList.add('collapse');
        backgroundElement.style.width = '270px';
        backgroundElement.style.transition = 'ease-in-out 600ms';
        backgroundElement.removeEventListener('click', hideAsideBarMenu);
        iElement.classList.replace('fa-times', 'fa-bars');

        toggleBodyStyle()
    }

    function checkElementForSubMenus(elements) {
        Array.from(elements).map((el) => {
            if (el.children.length > 1) {
                if (!el.querySelector('span')) {
                    el.children[0].appendChild(createIcon());
                }
                el.children[0].addEventListener('click', showSubMenu);
            }
        });
    }

    function showSubMenu(e) {
        e.stopImmediatePropagation();

        if (!e.currentTarget.parentNode.classList.contains('active')) {
            activeSubMenu(e.currentTarget)
        } else {
            inactiveSubMenu(e.currentTarget)
        }

        inactiveAllOtherElement(e.currentTarget)

        function activeSubMenu(element) {
            element.parentNode.classList.toggle('active')

            const [aElement, subMenu] = Array.from(element.parentNode.children);

            aElement.children[0].children[0].classList.replace('fa-caret-down', 'fa-caret-up');

            if (subMenu.children.length > 1) {
                subMenu.classList.add('show')
                checkElementForSubMenus(subMenu.children)
            }
        }

        function inactiveSubMenu(element) {
            element.parentNode.classList.remove('active');

            const [aElement, subMenu] = Array.from(element.parentNode.children);

            aElement.children[0].children[0].classList.replace('fa-caret-up', 'fa-caret-down');
            subMenu.classList.remove('show');
        }

        function inactiveAllOtherElement(element) {
            const currentElement = element.parentNode
            const allElement = element.parentNode.parentNode.children;
            Array.from(allElement).map((el) => {
                if (el !== currentElement) {
                    el.classList.remove('active');
                    if (el.children.length > 1) {
                        let spanElement = el.children[0].children[0];
                        if (spanElement.children[0].classList.contains('fa-caret-up')) {
                            spanElement.children[0].classList.replace('fa-caret-up', 'fa-caret-down');
                        }
                        el.children[1].classList.remove('show');
                    }
                }
            });
        }
    }

    function toggleBodyStyle() {
        document.body.classList.toggle('body-freeze');
    }

    function createIcon() {
        const spanElement = document.createElement('span');
        const iElement = document.createElement('i');
        iElement.className = 'fas fa-caret-down';
        spanElement.appendChild(iElement);
        return spanElement
    }


}

