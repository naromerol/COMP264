from chalice import Chalice
from chalicelib import storage_service
from chalicelib import recognition_service
from chalicelib import translation_service
from chalicelib import speech_service

import base64
import json

#####
# chalice app configuration
#####
app = Chalice(app_name='Capabilities')
app.debug = True

#####
# services initialization
#####
storage_location = 'content301133331'
storage_service = storage_service.StorageService(storage_location)
recognition_service = recognition_service.RecognitionService(storage_service)
translation_service = translation_service.TranslationService()
# Initialize speech service
speech_service = speech_service.SpeechService()


#####
# RESTful endpoints
#####
@app.route('/images', methods = ['POST'], cors = True)
def upload_image():
    """processes file upload and saves file to storage service"""
    request_data = json.loads(app.current_request.raw_body)
    file_name = request_data['filename']
    file_bytes = base64.b64decode(request_data['filebytes'])

    image_info = storage_service.upload_file(file_bytes, file_name)

    return image_info


@app.route('/images/{image_id}/translate-text', methods = ['POST'], cors = True)
def translate_image_text(image_id):
    """detects then translates text in the specified image"""
    request_data = json.loads(app.current_request.raw_body)
    from_lang = request_data['fromLang']
    to_lang = request_data['toLang']

    MIN_CONFIDENCE = 70.0

    text_lines = recognition_service.detect_text(image_id)

    translated_lines = []
    
    #create text to transform to speech
    # speech_input = ''

    for line in text_lines:
        # check confidence
        if float(line['confidence']) >= MIN_CONFIDENCE:
            translated_line = translation_service.translate_text(line['text'], from_lang, to_lang)
            translated_lines.append({
                'text': line['text'],
                'translation': translated_line,
                'boundingBox': line['boundingBox']
            })

            # # extract only required text for speech synthesis
            # speech_input += ' ' + translated_line["translatedText"]

    return translated_lines

@app.route('/create-audio', methods = ['POST'], cors = True)
def create_text_audio():

    request_data = json.loads(app.current_request.raw_body)
    translation_lines = request_data['translation_lines']
    
    ### Call speech synthesis service
    speech_service.create_speech_from_text(' '.join(translation_lines), 'audio_result')