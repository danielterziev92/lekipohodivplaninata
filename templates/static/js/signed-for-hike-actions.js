const allButtons = document.querySelectorAll('ul#signed-for-hike-actions');
Array.from(allButtons).map(el => {
    el.addEventListener('click', toggleClass);
});

function toggleClass(e) {
    const element = e.currentTarget;
    if (e.currentTarget.classList.contains('show')) {
        e.currentTarget.classList.remove('show');
    } else {
        e.currentTarget.classList.add('show');
        document.addEventListener('click', clickOutsideBox);
    }

    function clickOutsideBox(event) {
        if (!element.contains(event.target)) {
            element.classList.remove('show');
            document.removeEventListener('click', clickOutsideBox);
        }
    }
}
