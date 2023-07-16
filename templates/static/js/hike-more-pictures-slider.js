new Swiper(".more-pictures", {
    rewind: true,
    slidesPerView: 3,
    autoplay: {
        delay: 5000,
        disableOnInteraction: false,
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
        dynamicBullets: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});


const morePictureContainers = document.querySelectorAll('#more-pictures');
window.addEventListener('resize', () => {
    changePositionOfMorePictureContainers(morePictureContainers);
});

function changePositionOfMorePictureContainers(containers) {
    for (let container of containers) {
        if (window.innerWidth > 1200 && container.previousElementSibling.className === 'hike-body') {
            container.previousElementSibling.appendChild(container)

        }

        if (window.innerWidth <= 1200 && container.parentElement.className === 'hike-body') {
            container.parentElement.after(container)
        }
    }
}

changePositionOfMorePictureContainers(morePictureContainers);