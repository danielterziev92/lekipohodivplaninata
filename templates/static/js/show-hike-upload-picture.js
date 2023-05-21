const uploadFileElement = document.getElementById('id_new_main_picture');
const newImageContainer = document.querySelector('.new-image')
const newImgElement = document.getElementById('new-picture');

uploadFileElement.addEventListener('change', (e) => {
    newImgElement.src = URL.createObjectURL(e.currentTarget.files[0]);
    newImageContainer.style.display = 'flex';
});
