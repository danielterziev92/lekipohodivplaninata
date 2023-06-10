Array.from(document.querySelectorAll('div.numbers input[type=number]')).map(el => participantsCounts(el));

function participantsCounts(el) {
    el.addEventListener('change', onlyNumberAllowed);
    el.previousElementSibling.addEventListener('click', increaseCountNumber);
    el.nextElementSibling.addEventListener('click', decreaseCountNumber);

    function onlyNumberAllowed(e) {
        if (!isNumeric(e.currentTarget.value) || Number(e.currentTarget.value) < 0) {
            e.currentTarget.value = 0;
        }
    }

    function isNumeric(value) {
        return /^-?\d+$/.test(value);
    }

    function increaseCountNumber() {
        el.value = Number(el.value) + 1;
    }

    function decreaseCountNumber() {
        el.value = Number(el.value) - 1;
    }
}


document.getElementById('option-1').addEventListener('click', (e) => {
    document.getElementById('organized-transport').checked = true;
});

document.querySelector('.option-2').addEventListener('click', () => {
    document.getElementById('personal-transport').checked = true;
});
