function solve() {
    document.getElementById('menu-btn-small').addEventListener('click', (e) => {
        e.preventDefault();

        const iElement = e.currentTarget.children[0]
        const sideMenuElement = document.getElementById('side-menu-mobile');
        const backgroundElement = document.getElementById('side-menu-mobile').querySelector('.background');

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

    const userCountElement = document.getElementById('users-count');
    userCountElement.addEventListener('change', (e) => {
        if (Number.isNaN(Number(e.currentTarget.value)) || Number(e.currentTarget.value) < 0) {
            e.currentTarget.value = 0;
        }
    });
    document.querySelector('.sign-up-for-hike .numeric .plus').addEventListener('click', (e) => {
        const currentValue = userCountElement.value;
        userCountElement.value = Number(currentValue) + 1;
    });
    document.querySelector('.sign-up-for-hike .numeric .minus').addEventListener('click', (e) => {
        const currentValue = userCountElement.value;
        if (currentValue > 0) {
            userCountElement.value = Number(currentValue) - 1;
        }
    });

    document.getElementById('option-1').addEventListener('click', (e) => {
        document.getElementById('organized-transport').checked = true;
    });

    document.querySelector('.option-2').addEventListener('click', () => {
        document.getElementById('personal-transport').checked = true;
    });
}

window.onload = solve()