const subscribeMeButton = document.getElementById('subscribe-me');
subscribeMeButton.addEventListener('click', subscribeMe);

async function subscribeMe(e) {
    e.preventDefault();

    const emailInput = document.getElementById('subscribe-email');
    const offset = 70;

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
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
    });

    if (response.status === 201) {
        showMessageBox('Вие се абонирахте успешно!', ['message-box', 'success']);

        emailInput.value = '';
    }

    if (response.status === 409) {
        const responseData = await response.text();
        const data = JSON.parse(responseData)

        showMessageBox(data.message, ['message-box', 'error']);
    }

    function showMessageBox(message, classes) {
        const boxWithMessage = messageBoxElement(message, classes);

        document.body.appendChild(boxWithMessage);

        boxWithMessage.style.top = `${window.scrollY + offset}px`;
        window.addEventListener('scroll', () => {
            boxWithMessage.style.top = `${window.scrollY + offset}px`;
        });

        setTimeout(() => {
            document.body.removeChild(boxWithMessage);
        }, 5000);
    }
}

function messageBoxElement(text, classes) {
    const element = document.createElement('div');
    element.textContent = text;
    element.classList.add(...classes);

    return element;
}

