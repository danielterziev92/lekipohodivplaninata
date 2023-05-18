const showButtonElement = document.getElementById('show-sign-hike-form');
const hideButtonElement = document.getElementById('hide-sign-hike-form');
const signHikeFormElement = document.getElementById('sign-hike-form');

showButtonElement.addEventListener('click', showForm);
hideButtonElement.addEventListener('click', hideForm)


function showForm(e) {
    showButtonElement.style.display = 'none';
    signHikeFormElement.style.display = 'block';
    signHikeFormElement.style.height = '100%';
}

function hideForm() {
    signHikeFormElement.style.display = 'none';
    signHikeFormElement.style.height = '0%';
    showButtonElement.style.display = 'block';
}