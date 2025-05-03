document.getElementById('click-btn').addEventListener('click', () => {
    fetch('/click', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            document.getElementById('score-display').innerText = data.score;
            new Audio('/static/click_sound.wav').play();
        });
});

document.getElementById('click-boost').addEventListener('click', () => {
    fetch('/boost', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            document.getElementById('score-display').innerText = data.score;
            document.getElementById('multiplier-display').innerText = 'x' + data.multiplier;
            document.getElementById('boost-cost').innerText = data.cost;
            new Audio('/static/click_boost.wav').play();
        })
});