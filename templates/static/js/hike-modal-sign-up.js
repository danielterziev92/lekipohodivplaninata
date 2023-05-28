document.querySelector('label[for=sing-me-up]').addEventListener('click', () => {
    if (userInfoElement.style.display === 'none' || !userInfoElement.style.display) {
        userInfoElement.querySelector('input[type=email]').required = true;
        userInfoElement.style.display = 'block';
    } else {
        userInfoElement.style.display = 'none';
        userInfoElement.querySelector('input[type=email]').required = false;
    }
})