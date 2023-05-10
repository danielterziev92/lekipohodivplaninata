document.getElementById('id_new_password1').addEventListener('change', passwordValidations);
const passwordTooShortLiElement = document.getElementById('password_too_short');
const passwordNumericLiElement = document.getElementById('password_too_short');
const passwordSimilarLiElement = document.getElementById('password_too_short');


function passwordValidations(e) {
    class Alabala {
        constructor(element, successfulClassName, unsuccessfulClassName) {
        }
    }

    checkAllValidations(e.currentTarget.value);

    function checkAllValidations(value) {
        const validators = [
            passwordTooShor,

        ]
        for (let validator of validators) {
            validator(value);
        }
    }

    function passwordTooShor(value) {
        if (value.length < 8) {
            return
        }

        changeIcon(passwordTooShortLiElement, 'fa-xmark', 'fa-check');
        changeColor(passwordTooShortLiElement);
    }

    function passwordIsValid(element) {
        // console.log(element.children);
    }

    function changeIcon(element, oldClassName, newClassName) {
        const icon = findElementByClass(element.children, oldClassName).shift();
        Array.from(icon.classList).map((className) => {
            if (className === oldClassName) {
                icon.classList.remove(className)
                icon.classList.add(newClassName)
            }
        });
    }

    function changeColor(element) {
        element.style.color = '#159357'
    }

    function findElementByClass(elements, className) {
        return Array.from(elements).map((el) => {
            if (el.classList.contains(className)) {
                return el;
            }
        })
    }
}

