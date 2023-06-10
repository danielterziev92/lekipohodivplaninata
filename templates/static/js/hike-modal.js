const modalFormElement = document.getElementById('sign-for-hike-form');
const modalElement = document.getElementById('hike-modal');

document.getElementById('hide-sign-hike-form').addEventListener('click', hideModal);

document.querySelectorAll('#sign-for-hike').forEach(item => {
    item.addEventListener('click', showModal)
})


function get_pk_and_slug(e) {
    return e.currentTarget.getAttribute('datatype').split('/');
}

function showModal(e) {
    const [pk, slug] = get_pk_and_slug(e)
    const chooses = modalFormElement.querySelector('#choose-hike');
    Array.from(chooses.children).forEach((choose) => {
        if (choose.value === pk) {
            choose.selected = true;
        }
    });

    modalFormElement.action = `${pk}/${slug}/sign-up/`
    modalElement.style.top = `${window.scrollY.toFixed(0)}px`;
    document.body.classList.add('body-freeze')
    modalFormElement.parentNode.classList.add('active');
}

function hideModal() {
    modalFormElement.parentNode.classList.remove('active')
    document.body.classList.remove('body-freeze')
}

