// Function to create and append the download button
function createDownloadButton() {
    var downloadBtn = document.createElement('a');
    downloadBtn.setAttribute('id', 'download-btn');
    downloadBtn.setAttribute('class', 'btn btn-success');
    downloadBtn.innerText = 'Download MP3';

    // Download button click event
    downloadBtn.addEventListener('click', function(event) {
        // Simulate click event to trigger download
        var link = document.createElement('a');
        link.setAttribute('href', '/uploads/output.mp3'); // Correct path to the MP3 file
        link.setAttribute('download', 'output.mp3');
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

    // Append download button to download-section
    document.getElementById('download-section').appendChild(downloadBtn);
}

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
            
            // Create and append the download button
            createDownloadButton();
        } else {
            // Display error message
            document.getElementById('result').innerText = data.error;
        }
    })
    .catch(error => console.error('Error:', error));
});
    
document.addEventListener('DOMContentLoaded', function() {
    var dropArea = document.getElementById('drag-drop-area');

    dropArea.addEventListener('dragover', function(event) {
        event.preventDefault();
        dropArea.classList.add('dragover');
    });

    dropArea.addEventListener('dragleave', function(event) {
        event.preventDefault();
        dropArea.classList.remove('dragover');
    });

    dropArea.addEventListener('drop', function(event) {
        event.preventDefault();
        dropArea.classList.remove('dragover');

        var files = event.dataTransfer.files;
        document.getElementById('photo').files = files;
    });
});
