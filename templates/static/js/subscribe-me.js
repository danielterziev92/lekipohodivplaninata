const subscribeMeButton = document.getElementById('subscribe-me');
subscribeMeButton.addEventListener('click', subscribeMe);

async function subscribeMe(e) {
    e.preventDefault();

    const emailInput = document.getElementById('subscribe-email');
    const successMessageBox = successMessageBoxElement('Вие се абонирахте успешно!');

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
    const url = `${window.location.origin}/api/subscribers/`;
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            'email': emailInput.value
        }),
    })

    if (response.status === 201) {
        const offset = 70;

        document.body.appendChild(successMessageBox);

        successMessageBox.style.top = `${window.scrollY + offset}px`;
        window.addEventListener('scroll', () => {
            successMessageBox.style.top = `${window.scrollY + offset}px`;
        });

        emailInput.value = '';

        setTimeout(() => {
            document.body.removeChild(successMessageBox);
        }, 5000);
    }
}

function successMessageBoxElement(text) {
    const element = document.createElement('div');
    element.textContent = text;
    element.classList.add('message-box');

    return element;
}