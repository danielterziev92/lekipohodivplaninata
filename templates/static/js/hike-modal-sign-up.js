const userInfoElement = document.getElementById('user-info');

document.querySelector('.registration label[for=sing-me-up]').addEventListener('click', () => {
    userInfoElement.toggleAttribute('id');
})