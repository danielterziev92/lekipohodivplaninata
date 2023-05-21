document.getElementById('add-new-row').addEventListener('click', addNewRowImage);
const imageElement = document.getElementById('image');
imageElement.addEventListener('change', showPicture)
const moreImagesFormElement = document.getElementById('more-images')
const buttonsElement = document.querySelector('.buttons')


function addNewRowImage(e) {
    const element = imageElement.cloneNode(true);
    clearNode(element)
    element.addEventListener('change', showPicture)
    moreImagesFormElement.insertBefore(element, buttonsElement)
}

function showPicture(e) {
    const inputElement = e.currentTarget.querySelector('input[type=file]')
    const newImgElement = e.currentTarget.querySelector('#new-picture');
    newImgElement.src = URL.createObjectURL(inputElement.files[0]);
    newImgElement.parentNode.style.display = 'flex';
}

function clearNode(element) {
    element.querySelector('input[type=file]').value = ''
    element.querySelector('#new-picture').src = ''
}