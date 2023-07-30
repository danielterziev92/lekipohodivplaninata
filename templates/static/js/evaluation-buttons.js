const allLabelsForAssessment = document.querySelectorAll('#id_assessment label')

Array.from(allLabelsForAssessment).forEach((el) => {
    el.addEventListener('click', dispatcher)
});

function dispatcher(e) {
    if (e.currentTarget.classList.contains('selected')) {
        disableSelectedRadioElement(e.currentTarget);
    } else {
        enableSelectedRadioElement(e.currentTarget);
    }

    disableAllOtherLabels(allLabelsForAssessment, e.currentTarget);

    function disableAllOtherLabels(labels, currentElement) {
        Array.from(labels).forEach((el) => {
            if (el !== currentElement) {
                disableSelectedRadioElement(el);
            }
        })
    }

    function enableSelectedRadioElement(el) {
        el.style.backgroundColor = '#cf5533';
        el.style.color = '#ffffff';
    }

    function disableSelectedRadioElement(el) {
        el.style.backgroundColor = '#ffffff';
        el.style.color = '#1b1b1b';
    }


}
