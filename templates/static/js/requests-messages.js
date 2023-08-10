window.addEventListener('DOMContentLoaded', (event) => {

    const messageElements = document.querySelectorAll('.messages li');

    messageElements.forEach((message) => {
        message.classList.add('show-message')
        message.classList.add('show-message');
        setTimeout(() => {
            message.parentElement.remove();
        }, 5000);
    });

});