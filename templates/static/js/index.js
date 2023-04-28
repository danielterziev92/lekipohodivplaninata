const asideMenuStyle = document.querySelector('.side-menu-mobile');
const headerElement = document.getElementById('main-header');
const sideMenuElement = document.getElementById('side-menu-mobile');


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


// left: 37, up: 38, right: 39, down: 40,
// spacebar: 32, pageup: 33, pagedown: 34, end: 35, home: 36
// var keys = {37: 1, 38: 1, 39: 1, 40: 1};
//
// function preventDefault(e) {
//   e.preventDefault();
// }
//
// function preventDefaultForScrollKeys(e) {
//   if (keys[e.keyCode]) {
//     preventDefault(e);
//     return false;
//   }
// }
//
// // modern Chrome requires { passive: false } when adding event
// var supportsPassive = false;
// try {
//   window.addEventListener("test", null, Object.defineProperty({}, 'passive', {
//     get: function () { supportsPassive = true; }
//   }));
// } catch(e) {}
//
// var wheelOpt = supportsPassive ? { passive: false } : false;
// var wheelEvent = 'onwheel' in document.createElement('div') ? 'wheel' : 'mousewheel';
//
// // call this to Disable
// function disableScroll() {
//   window.addEventListener('DOMMouseScroll', preventDefault, false); // older FF
//   window.addEventListener(wheelEvent, preventDefault, wheelOpt); // modern desktop
//   window.addEventListener('touchmove', preventDefault, wheelOpt); // mobile
//   window.addEventListener('keydown', preventDefaultForScrollKeys, false);
// }
//
// // call this to Enable
// function enableScroll() {
//   window.removeEventListener('DOMMouseScroll', preventDefault, false);
//   window.removeEventListener(wheelEvent, preventDefault, wheelOpt);
//   window.removeEventListener('touchmove', preventDefault, wheelOpt);
//   window.removeEventListener('keydown', preventDefaultForScrollKeys, false);
// }