const asideMenuStyle = document.querySelector('.side-menu-mobile');
const headerElement = document.getElementById('main-header');
const sideMenuElement = document.getElementById('side-menu-mobile');

document.querySelectorAll('.side-menu-mobile ul li').forEach((element) => {
    if (element.children.length > 1) {
        element.children[0].appendChild(createIcon());
    }

    function createIcon() {
        const spanElement = document.createElement('span');
        const iElement = document.createElement('i');
        iElement.className = 'fas fa-caret-down';
        spanElement.appendChild(iElement);
        return spanElement
    }
})


document.getElementById('menu-btn-small').addEventListener('click', (e) => {
    e.preventDefault();

    const iElement = e.currentTarget.children[0]
    const sideMenuElement = document.getElementById('side-menu-mobile');
    const backgroundElement = document.getElementById('side-menu-mobile').querySelector('.background');

    asideMenuStyle.style.top = `${window.scrollY.toFixed(0)}px`;

    document.body.style.overflow = 'hidden';
    document.body.style.height = '100%';

    if (sideMenuElement.classList.contains('collapse')) {
        sideMenuElement.classList.remove('collapse');
        backgroundElement.style.width = '100vw';
        iElement.className = ''
        iElement.classList.add('fas', 'fa-times');

        backgroundElement.addEventListener('click', () => {
            sideMenuElement.classList.add('collapse');
            backgroundElement.style.width = '270px';
            backgroundElement.style.transition = 'ease-in-out 600ms';
            iElement.className = ''
            iElement.classList.add('fa-solid', 'fa-bars');
            document.body.style.overflow = 'unset';
            document.body.style.height = 'auto';
        })
    }

    const sideMenuItems = document.getElementById('side-menu-mobile').querySelector('ul');
    Array.from(sideMenuItems.children).map((el) => {
        if (el.getAttribute('listener') !== 'true') {
            el.children[0].addEventListener('click', toggleActiveElement);
        }
    });

    function toggleActiveElement(e) {
        e.stopImmediatePropagation();

        if (e.currentTarget.parentNode.children.length > 1) {
            e.currentTarget.classList.toggle('rotate');
            e.currentTarget.nextElementSibling.classList.toggle('show');
        }

        e.currentTarget.parentNode.classList.add('active');

        Array.from(sideMenuItems.children).map((el) => {
            if (el !== e.currentTarget.parentNode) {
                el.classList.remove('active')
                if (el.children.length > 1 && el.children[1].classList.contains('show')) {
                    el.children[1].classList.remove('show')
                }
            }
        });
    }
});

if (window.scrollY > 0) {
    headerElement.classList.add('sticky');
}

window.addEventListener('scroll', () => {
    headerElement.classList.toggle('sticky', window.scrollY > 0);
});

window.onscroll = function () {
    asideMenuStyle.style.top = `${window.scrollY.toFixed(0)}px`;
    asideMenuStyle.style.transition = 'unset';
}
