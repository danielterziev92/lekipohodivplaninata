const emailListContainer = document.getElementById('email-list');

async function fetchEmails() {
    try {
        const url = `${window.location.origin}/api/mailbox/`;
        const response = await fetch(url);

        if (!response.ok) {
            const result = await response.json();
            throw new Error(result.message);
        }

        const data = await response.json();
        displayEmails(data);

    } catch (error) {
        console.error('An error occurred:', error);
    }
}

function displayEmails(emails) {
    emailListContainer.innerHTML = '';

    for (const email of emails) {
        const emailDiv = document.createElement('div');
        emailDiv.classList.add('email');

        const subjectElem = document.createElement('h2');
        subjectElem.textContent = email.subject;

        const senderElem = document.createElement('p');
        senderElem.textContent = `From: ${email.sender}`;

        const bodyElem = document.createElement('p');
        bodyElem.textContent = email.body;

        emailDiv.appendChild(subjectElem);
        emailDiv.appendChild(senderElem);
        emailDiv.appendChild(bodyElem);

        emailListContainer.appendChild(emailDiv);
    }
}

fetchEmails();
