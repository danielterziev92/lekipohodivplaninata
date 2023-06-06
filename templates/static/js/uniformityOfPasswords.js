const buttonElement = document.querySelector('.fields-form button');
document.querySelector('label[for=password_1]').appendChild(createEyeIcon());
document.querySelector('label[for=password_2]').appendChild(createEyeIcon());
// secondPasswordLabel.appendChild(createShowHideIElement(true));
// let is_showed = false;

//TODO: Must Refactor This Functions

function createEyeIcon() {
    const element = document.createElement('i');
    element.classList.add('fa-solid', 'fa-eye');
    element.addEventListener('click', showOrHidePassword);
    return element;
}

function showOrHidePassword(e) {
    console.log(e.currentTarget);

    if (e.currentTarget.classList.contains('fa-eye-slash')) {
        console.log('here')
        e.currentTarget.classList.replace('fa-eye-slash', 'fa-eye');
        e.currentTarget.previousElementSibling.type = 'password';
    }

    if (e.currentTarget.classList.contains('fa-eye')) {
        e.currentTarget.className.replace('fa-eye', 'fa-eye-slash');
        e.currentTarget.previousElementSibling.type = 'text';
    }
}


// function createShowHideIElement(validate) {
//     buttonElement.disabled = true;
//
//
//     const element = document.createElement('i');
//     element.className = 'fa-solid fa-eye-slash';
//     element.addEventListener('click', toggleClassElement);
//     if (validate) {
//         document.getElementById('password_2').addEventListener('keyup', checkPasswords);
//         document.getElementById('password_2').addEventListener('touchstart', checkPasswords);
//     }
//
//     return element
//
//     function toggleClassElement(e) {
//         if (e.currentTarget.classList.contains('fa-eye-slash')) {
//             e.currentTarget.className = 'fa-solid fa-eye';
//             e.currentTarget.parentNode.querySelector('input[type=password]').type = 'text';
//         } else {
//             e.currentTarget.className = 'fa-solid fa-eye-slash';
//             e.currentTarget.parentNode.querySelector('input[type=text]').type = 'password';
//         }
//     }
//
//     function checkPasswords(e) {
//         const firstPassword = document.getElementById('password_1');
//         const secondPassword = e.currentTarget;
//         const errorElement = showErrorMessage();
//         if (firstPassword.value !== secondPassword.value && !is_showed) {
//             secondPasswordLabel.after(errorElement);
//             errorElement.classList.add('alert');
//             is_showed = true;
//             buttonElement.disabled = true;
//         }
//
//         if (firstPassword.value === secondPassword.value && is_showed) {
//             console.log(errorElement)
//             buttonElement.disabled = false;
//             // errorElement.style.backgroundColor = '#159357';
//             errorElement.style.backgroundColor = 'green';
//             // errorElement.textContent = 'Паролите съвпаднаха';
//             setTimeout(() => document.querySelector('small.alert').remove(), 1000);
//             errorElement.classList.remove('alert')
//             is_showed = false;
//         }
//     }
//
//     function showErrorMessage() {
//         const element = document.createElement('small');
//         element.textContent = 'Паролите не съвпадат.';
//         return element;
//     }
// }