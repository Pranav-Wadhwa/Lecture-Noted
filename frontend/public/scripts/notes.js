const spinner = document.querySelector('#spinner');
const animContainer = document.querySelector('#anim-container');

function hideAnimation() {
    animContainer.style.transition = 'all 0.3s';
    animContainer.style.opacity = '0';
    setTimeout(() => {
        animContainer.style.display = 'none';
    }, 300);
}

setTimeout(() => {
    hideAnimation();
}, 2000);