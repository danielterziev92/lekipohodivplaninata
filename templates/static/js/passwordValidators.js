document.getElementById('password_1').addEventListener('keyup', passwordValidations);
document.getElementById('password_1').addEventListener('touchstart', passwordValidations);

const passwordTooShortLiElement = document.getElementById('too-short');
const uppercaseLetterLiElement = document.getElementById('uppercase-letter');
const lowercaseLetterLiElement = document.getElementById('lowercase-letter');
const numberLiElement = document.getElementById('number');


function passwordValidations(e) {
    class ChangeHelpingTextFields {
        constructor(element, successfulClassName, unsuccessfulClassName) {
            this.element = element;
            this.successfulClassName = successfulClassName;
            this.unsuccessfulClassName = unsuccessfulClassName;
            this.successfulIconColor = '#159357';
            this.unsuccessfulIconColor = '#c41e3d';
        }

        passwordIsInvalid() {
            this.changeColor(this.unsuccessfulIconColor);
            this.changeIcon(this.successfulClassName, this.unsuccessfulClassName);
            buttonElement.disabled = true;
        }

        passwordIsValid() {
            this.changeColor(this.successfulIconColor);
            this.changeIcon(this.unsuccessfulClassName, this.successfulClassName);
            buttonElement.disabled = false;
        }

        changeColor(color) {
            this.element.style.color = color
        }

        changeIcon(oldClassName, newClassName) {
            const icon = this.element.children[0];
            icon.classList.remove(oldClassName);
            icon.classList.add(newClassName)
        }

    }


    const validators = [
        passwordTooShor,
        passwordContainUppercaseLetter,
        passwordContainLowercaseLetter,
        passwordContainNumber
    ]

    const checkedClassName = 'fa-check';
    const crossClassName = 'fa-xmark';

    checkAllValidations(e.currentTarget.value);

    function checkAllValidations(value) {
        for (const validator of validators) {
            validator(value);
        }
    }

    function passwordTooShor(value) {
        const validator = new ChangeHelpingTextFields(passwordTooShortLiElement, checkedClassName, crossClassName)
        if (value.length < 8) {
            return validator.passwordIsInvalid();
        }

        return validator.passwordIsValid();

    }

    function checkRegEx(value, pattern, validator) {
        if (!value.match(pattern)) {
            return validator.passwordIsInvalid();
        }

        return validator.passwordIsValid();
    }

    function passwordContainUppercaseLetter(value) {
        const pattern = /[A-Z]|[А-Я]/g;
        const validator = new ChangeHelpingTextFields(uppercaseLetterLiElement, checkedClassName, crossClassName);
        checkRegEx(value, pattern, validator);
    }

    function passwordContainLowercaseLetter(value) {
        const pattern = /[a-z]|[а-я]/g;
        const validator = new ChangeHelpingTextFields(lowercaseLetterLiElement, checkedClassName, crossClassName);
        checkRegEx(value, pattern, validator);
    }

    function passwordContainNumber(value) {
        const pattern = /[0-9]/g;
        const validator = new ChangeHelpingTextFields(numberLiElement, checkedClassName, crossClassName);
        checkRegEx(value, pattern, validator);
    }

}

