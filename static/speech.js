window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();
recognition.interimResults = true;
recognition.lang = 'en-US';

recognition.addEventListener('result', e => {
    const transcript = Array.from(e.results)
        .map(result => result[0])
        .map(result => result.transcript)
        .join('')
        .toLowerCase();

    if (e.results[0].isFinal) {
        if (transcript.includes('zoom in')) {
            map.zoomIn();
        } else if (transcript.includes('zoom out')) {
            map.zoomOut();
        } else if (transcript.includes('search for')) {
            const city = transcript.split('search for')[1].trim();
            document.getElementById('searchBar').value = city;
            searchCity();
        }
    }
});

recognition.addEventListener('end', recognition.start);
recognition.start();
