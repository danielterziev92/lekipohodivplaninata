const userInfoElement = document.getElementById('user-info');

document.querySelector('.registration label[for=sing-me-up]').addEventListener('click', () => {
    userInfoElement.getAttribute('id') === 'user-info'
        ? userInfoElement.removeAttribute('id')
        : userInfoElement.setAttribute('id', 'user-info')
})