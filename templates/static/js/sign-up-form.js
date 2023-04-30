const userCountElement = document.getElementById('users-count');
userCountElement.addEventListener('change', (e) => {
    if (Number.isNaN(Number(e.currentTarget.value)) || Number(e.currentTarget.value) < 0) {
        e.currentTarget.value = 0;
    }
});
document.querySelector('.sign-up-for-hike .numeric .plus').addEventListener('click', (e) => {
    const currentValue = userCountElement.value;
    userCountElement.value = Number(currentValue) + 1;
});
document.querySelector('.sign-up-for-hike .numeric .minus').addEventListener('click', (e) => {
    const currentValue = userCountElement.value;
    if (currentValue > 0) {
        userCountElement.value = Number(currentValue) - 1;
    }
});

document.getElementById('option-1').addEventListener('click', (e) => {
    document.getElementById('organized-transport').checked = true;
});

document.querySelector('.option-2').addEventListener('click', () => {
    document.getElementById('personal-transport').checked = true;
});
