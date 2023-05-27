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

    modalFormElement.action = `${pk}/${slug}`
    modalElement.style.top = `${window.scrollY.toFixed(0)}px`;
    modalFormElement.parentNode.style.display = 'flex';
}

function hideModal() {
    modalFormElement.parentNode.style.display = 'none';
}

