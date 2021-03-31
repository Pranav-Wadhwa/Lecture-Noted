const goButton = document.querySelector('#go-btn');
const demoButton = document.querySelector('#demo-btn');
const textField = document.querySelector('#text-field');

function getVideoId(url) {
    const parts = url.split('v=');
    if (parts.length < 2) {
        return '';
    }
    var videoId = parts[1];
    var ampersandPosition = videoId.indexOf('&');
    if (ampersandPosition != -1) {
        videoId = videoId.substring(0, ampersandPosition);
    }
    return videoId;
}

goButton.addEventListener('click', function (event) {
    const videoId = getVideoId(textField.value);
    location.href = '/notes?vid=' + videoId;
});

demoButton.addEventListener('click', function(event) {
    textField.value = 'https://www.youtube.com/watch?v=RqCqUEu9nY4';
    updateButton();
});

function updateButton() {
    const id = getVideoId(textField.value);
    goButton.disabled = id.length == 0;
}

textField.addEventListener('input', updateButton);
textField.addEventListener('propertychange', updateButton);

updateButton();