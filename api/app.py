from flask import Flask, render_template, request, jsonify, send_file
from flask_uploads import UploadSet, IMAGES, configure_uploads
import pytesseract
from PIL import Image
import os
from gtts import gTTS
import os

app = Flask(__name__)

# Configure file upload
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
configure_uploads(app, photos)

# Homepage
@app.route('/')
def index():
    return render_template('upload.html')

# Upload image and convert text to speech
@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        image_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)

        # Extract text from image
        text = extract_text(image_path)

        # Convert text to speech and get the path to the generated MP3 file
        mp3_path = convert_to_speech(text, filename)

        if mp3_path:
            return jsonify({'message': 'Text extracted successfully', 'text': text, 'mp3_path': mp3_path})
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

# Convert text to speech
def convert_to_speech(text, filename):
    try:
        # Generate speech using gTTS
        tts = gTTS(text=text, lang='en')
        
        # Define the directory to save the MP3 file
        save_dir = 'static/audio'
        
        # Create the directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Define the path to save the MP3 file
        mp3_path = os.path.join(save_dir, f'{filename}.mp3')
        
        # Save the speech as an MP3 file
        tts.save(mp3_path)
        
        return mp3_path
    except Exception as e:
        print("Error during text-to-speech conversion:", e)
        return None

