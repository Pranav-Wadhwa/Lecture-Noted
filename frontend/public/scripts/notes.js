const spinner = document.querySelector('#spinner');
const animContainer = document.querySelector('#anim-container');

const title = document.querySelector('#title');
const creatorName = document.querySelector('#creator-name');
const watchButton = document.querySelector('#watch-btn');
const textContainer = document.querySelector('#text-container');
const exportButton = document.querySelector('#export-btn');

var isTesting = true;

function hideAnimation() {
    animContainer.style.transition = 'all 0.3s';
    animContainer.style.opacity = '0';
    setTimeout(() => {
        animContainer.style.display = 'none';
    }, 300);
}

function getParameterByName(name, url = window.location.href) {
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function getNotes() {
    const videoId = getParameterByName('vid');
    if (!(typeof videoId === 'string' && videoId.length > 0)) {
        location.href = '/';
        return;
    }
    // Post-hackathon note: isTesting must be set to true as the other endpoint is no longer active.
    const url =  isTesting ? 'https://lecture-noted-backend.herokuapp.com/testingv2' : 'https://lecture-noted-backend.herokuapp.com/notes/' + videoId;
    const opts = {
        method: 'GET',
    }
    fetch(url, opts).then(function(res) {
        return res.json();
    })
    .then(function(result) {
        title.innerHTML = result.metadata.title;
        creatorName.innerHTML = result.metadata.author;
        watchButton.href = 'https://youtube.com/watch?v=' + videoId;
        var addedImage = false;
        result.response.forEach((obj) => {
            if (obj.type === 'text') {
                const bullet = document.createElement('div');
                bullet.innerHTML = obj.data;
                bullet.classList.add('Notes-bullet');
                if ('time' in obj) {
                    const link = document.createElement('a');
                    const time = Math.round(obj.time);
                    var seconds = time % 60;
                    seconds = (seconds < 10) ? `0${seconds}` : `${seconds}`;
                    const minutes = Math.trunc(time / 60);
                    link.innerHTML = `[${minutes}:${seconds}]`;
                    link.href = `https://youtu.be/${videoId}?t=${time}`;
                    link.classList.add('Notes-intextLink');
                    bullet.insertBefore(link, bullet.firstChild);
                }
                textContainer.appendChild(bullet);
            } 
            else if (obj.type === 'image' && !addedImage) {
                const image = document.createElement('img');
                image.src = obj.data.image;
                image.classList.add('Notes-image');
                textContainer.insertBefore(image, textContainer.firstChild)
                addedImage = true;
            }
        });
        result.metadata.videoId = videoId;
        const origData = JSON.stringify(result);
        exportButton.href = `https://lecture-noted-backend.herokuapp.com/docx?data=${origData}`;
        hideAnimation();
    })
    .catch(function(error) {
        alert(error);
    });
}

getNotes();