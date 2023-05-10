const buttonElement = document.querySelector('.fields-form button');
document.querySelector('label[for=password_1]').appendChild(createShowHideIElement(false));
const secondPasswordLabel = document.querySelector('label[for=password_2]');
secondPasswordLabel.appendChild(createShowHideIElement(true));
let is_showed = false;


function createShowHideIElement(validate) {
    buttonElement.disabled = true;


    const element = document.createElement('i');
    element.className = 'fa-solid fa-eye-slash';
    element.addEventListener('click', toggleClassElement);
    if (validate) {
        document.getElementById('password_2').addEventListener('change', checkPasswords);
    }

    return element

    function toggleClassElement(e) {
        if (e.currentTarget.classList.contains('fa-eye-slash')) {
            e.currentTarget.className = 'fa-solid fa-eye';
            e.currentTarget.parentNode.querySelector('input[type=password]').type = 'text';
        } else {
            e.currentTarget.className = 'fa-solid fa-eye-slash';
            e.currentTarget.parentNode.querySelector('input[type=text]').type = 'password';
        }
    }

    function checkPasswords(e) {
        const firstPassword = document.getElementById('password_1');
        const secondPassword = e.currentTarget;
        const errorElement = showErrorMessage();
        if (firstPassword.value !== secondPassword.value && !is_showed) {
            secondPasswordLabel.after(errorElement);
            errorElement.classList.add('alert');
            is_showed = true;
        }

        if (firstPassword.value === secondPassword.value && is_showed) {
            errorElement.classList.remove('alert')
            setTimeout(() => document.querySelector('small.alert').remove(), 1000);
            is_showed = false;
            buttonElement.disabled = false;
        }
    }

    function showErrorMessage() {
        const element = document.createElement('small');
        element.textContent = 'Паролите не съвпадат.';
        return element;
    }
}