// Prevent default form submission behavior
document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = new FormData(this);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // Display message
            document.getElementById('result').innerHTML = '<div class="text-center mb-3">' + data.message + '</div>';
            
            // Create and populate textbox with extracted text
            createTextbox(data.text);

            // Play the MP3 using the media player
            var audioPlayer = document.getElementById('audio-player');
            var audioSource = document.getElementById('audio-source');
            audioSource.src = data.mp3_path;

            // Adjust the rate of speech
            var utterance = new SpeechSynthesisUtterance(data.text);
            utterance.rate = 1.0; // Adjust the rate as needed
            speechSynthesis.speak(utterance);

            // Update audio player source and play
            audioPlayer.load();
            audioPlayer.play();
        } else {
            // Display error message
            document.getElementById('result').innerText = data.error;
        }
    })
    .catch(error => console.error('Error:', error));
});
