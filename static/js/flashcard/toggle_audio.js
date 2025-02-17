function toggleAudio(id) {
    var audio = document.getElementById('audio-' + id);

    if (audio.paused) {
        audio.play();
    } else {
        audio.pause();
        audio.currentTime = 0;  // Reset to start when paused
    }
}
