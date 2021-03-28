const spinner = document.querySelector('#spinner');
const animContainer = document.querySelector('#anim-container');

const title = document.querySelector('#title');
const creatorName = document.querySelector('#creator-name');
const watchButton = document.querySelector('#watch-btn');
const textContainer = document.querySelector('#text-container');

var isTesting = false;

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
    const url =  isTesting ? 'https://lecture-noted-backend.herokuapp.com/testing' : 'https://lecture-noted-backend.herokuapp.com/notes/' + videoId;
    const opts = {
        method: 'GET',
    }
    console.log('Getting notes for ' + videoId);
    fetch(url, opts).then(function(res) {
        return res.json();
    })
    .then(function(result) {
        console.log(result);
        title.innerHTML = result.metadata.title;
        creatorName.innerHTML = result.metadata.author;
        watchButton.href = 'https://youtube.com/watch?v=' + videoId;
        result.response.forEach((obj) => {
            if (obj.type === 'text') {
                const bullet = document.createElement('div');
                bullet.innerHTML = obj.data;
                bullet.classList.add('Notes-bullet');
                textContainer.appendChild(bullet);
            }
        });
        hideAnimation();
    })
    .catch(function(error) {
        // location.href = '/';
    });
}

getNotes();