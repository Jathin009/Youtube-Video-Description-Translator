from flask import Flask, render_template, request, jsonify
from youtube import fetch_youtube_video_details
from google.cloud import translate_v2 as translate
import os

app = Flask(__name__)

# Configure Google Cloud Translation API credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/Student/Documents/IWC/cloud-muthineni-jathin/Final2/cloud-muthineni-jathin-725aeb7eac88.json'  # Replace with the path to your credentials.json file

# Initialize Google Cloud Translation API client
translate_client = translate.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')

    if not query:
        return 'No search query provided'

    # Fetch YouTube video details using youtube.py module
    video_details_list = fetch_youtube_video_details(query, max_results=5   )

    if not video_details_list:
        return 'No videos found'

    # Translate video descriptions to English by default
    for video in video_details_list:
        translations = translate_client.translate(video['description'], target_language='en')
        video['translated_description'] = translations['translatedText']

    return render_template('results.html', video_details_list=video_details_list)

@app.route('/translate', methods=['POST'])
def translate_descriptions():
    data = request.get_json()
    descriptions = data.get('descriptions', [])
    target_language = data.get('target_language', 'en')

    translated_descriptions = []
    for description in descriptions:
        translation = translate_client.translate(description, target_language=target_language)
        translated_descriptions.append(translation['translatedText'])

    return jsonify({'translated_descriptions': translated_descriptions})

if __name__ == '__main__':
    app.run(debug=True)
