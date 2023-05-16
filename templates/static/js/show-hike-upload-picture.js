const uploadFileElement = document.querySelector('input[type=file]#id_main_picture');
const newImgElement = document.getElementById('new-picture');

uploadFileElement.addEventListener('change', (e) => {
    const pathName = URL.createObjectURL(e.currentTarget.files[0])
    console.log(pathName)
    newImgElement.src = pathName;
    newImgElement.style.display = 'block';
});
