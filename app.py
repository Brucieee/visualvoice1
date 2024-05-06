from flask import Flask, render_template, request, jsonify
from flask_uploads import UploadSet, IMAGES, configure_uploads
import pytesseract
from PIL import Image
import os
import pyttsx3
import subprocess

app = Flask(__name__)

# Configure file upload
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
configure_uploads(app, photos)

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Upload image and convert text to speech
@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        image_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)

        # Extract text from image
        text = extract_text(image_path)

        # Convert text to speech and save as MP3
        mp3_path = convert_to_speech(text, filename)

        if mp3_path:
            return jsonify({'message': 'Text converted to speech and saved as MP3', 'mp3_path': mp3_path})
        else:
            return jsonify({'error': 'Error converting text to speech'})
    else:
        return jsonify({'error': 'No file uploaded'})

# Extract text from image
def extract_text(image_path):
    try:
        # Specify language (replace 'eng' with the appropriate language code if needed)
        text = pytesseract.image_to_string(Image.open(image_path), lang='eng')
        return text.strip()  # Strip whitespace from the extracted text
    except Exception as e:
        print("Error during text extraction:", e)
        return None

# Convert text to speech using eSpeak and save as MP3
def convert_to_speech(text, filename):
    try:
        # Initialize the eSpeak engine
        engine = pyttsx3.init()

        # Set properties (optional)
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.9) # Volume (0.0 to 1.0)

        # Convert text to speech
        engine.say(text)

        # Save speech to a file as MP3
        mp3_output_folder = 'mp3_outputs'
        os.makedirs(mp3_output_folder, exist_ok=True)

        mp3_output_path = os.path.join(mp3_output_folder, os.path.splitext(filename)[0] + '.mp3')
        engine.save_to_file(text, mp3_output_path)

        # Run the eSpeak engine
        engine.runAndWait()

        return mp3_output_path  # Return the path to the saved MP3 file
    except Exception as e:
        print("Error during text-to-speech conversion:", e)
        return None

if __name__ == '__main__':
    app.run(debug=True)
