document.addEventListener('DOMContentLoaded', selectRadioButton);


function selectRadioButton() {
    const selectedEval = getUrlParams();

    if (selectedEval && !isNaN(selectedEval)) {
        const radioInputs = document.querySelectorAll('#id_assessment input[type=radio][name="assessment"]');

        for (const radio of radioInputs) {
            if (radio.value === selectedEval) {
                radio.click();
            }
        }
    }
}

function getUrlParams() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('selected_eval');
}