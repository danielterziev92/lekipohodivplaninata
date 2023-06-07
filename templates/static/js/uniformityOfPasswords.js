const buttonElement = document.querySelector('.fields-form button');
const secondPasswordLabelElement = document.querySelector('label[for=password_2]');
const errorElement = showErrorMessageBox();

document.querySelector('label[for=password_1]').appendChild(createEyeIcon());
document.getElementById('password_2').addEventListener('keyup', checkSamenessOfPasswords);
document.getElementById('password_2').addEventListener('change', checkSamenessOfPasswords);
secondPasswordLabelElement.appendChild(createEyeIcon());


function createEyeIcon() {
    const element = document.createElement('i');
    element.classList.add('fa-solid', 'fa-eye-slash');
    element.addEventListener('click', showOrHidePassword);
    return element;

    function showOrHidePassword(e) {
        if (e.currentTarget.classList.contains('fa-eye-slash')) {
            e.currentTarget.classList.replace('fa-eye-slash', 'fa-eye');
            e.currentTarget.previousElementSibling.type = 'text';
        } else if (e.currentTarget.classList.contains('fa-eye')) {
            e.currentTarget.classList.replace('fa-eye', 'fa-eye-slash');
            e.currentTarget.previousElementSibling.type = 'password';
        }
    }
}

function checkSamenessOfPasswords(e) {
    const first_password = document.getElementById('password_1').value;
    const second_password = e.currentTarget.value;

    if (first_password !== second_password) {
        secondPasswordLabelElement.after(errorElement);
        if (errorElement.classList.contains('success')) {
            errorElement.classList.remove('success');
        }
        errorElement.classList.add('alert');
        errorElement.textContent = 'Паролите не съвпадат';
        buttonElement.disabled = true;
    }

    if (first_password === second_password) {
        errorElement.classList.replace('alert', 'success');
        errorElement.textContent = 'Паролите съвпадат';
        buttonElement.disabled = false;
        setTimeout(() => errorElement.remove(), 1000);
    }
}


function showErrorMessageBox() {
    return document.createElement('small');
}
