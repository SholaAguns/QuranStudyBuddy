
let currentVerseIndex = 0;
let verses = document.querySelectorAll('.card');
let audioElements = document.querySelectorAll('.verse-audio');
let playButton = document.getElementById('play-button');
let pauseButton = document.getElementById('pause-button');
let resetButton = document.getElementById('reset-button');
let isPlaying = false;
let currentAudio = null;

// Play the audio and scroll to the verse
function playNextVerse() {
    if (currentVerseIndex < verses.length) {
        let currentVerse = verses[currentVerseIndex];
        let currentAudioElement = audioElements[currentVerseIndex];

        // Scroll to the verse
        currentVerse.scrollIntoView({behavior: 'smooth', block: 'center'});

        // Play the audio
        currentAudioElement.play();

        // Update button states
        currentAudio = currentAudioElement;
        isPlaying = true;
        playButton.style.display = 'none';
        pauseButton.style.display = 'inline-block';
        resetButton.style.display = 'inline-block';

        // Listen for when the audio ends
        currentAudioElement.onended = function() {
            currentVerseIndex++;
            if (currentVerseIndex < verses.length) {
                playNextVerse(); // Move to next verse
            } else {
                isPlaying = false;
                playButton.style.display = 'inline-block';
                pauseButton.style.display = 'none';
                resetButton.style.display = 'none';
            }
        };
    }
}

// Pause the current audio
function pauseAudio() {
    if (currentAudio) {
        currentAudio.pause();
        isPlaying = false;
        playButton.style.display = 'inline-block';
        pauseButton.style.display = 'none';
    }
}

// Stop and reset the audio
function resetAudio() {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
        isPlaying = false;
        playButton.style.display = 'inline-block';
        pauseButton.style.display = 'none';
        resetButton.style.display = 'none';
    }
    currentVerseIndex = 0;
}

// Event listeners for buttons
playButton.addEventListener('click', function() {
    if (!isPlaying) {
        playNextVerse();
    }
});

pauseButton.addEventListener('click', pauseAudio);
resetButton.addEventListener('click', resetAudio);
