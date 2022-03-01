import boto3
# NESTOR ROMERO - 301133331
# COMP264 MIDTERM
# Template service taken from class lab exercises

class TranslationService:
    def __init__(self):
        self.client = boto3.client('translate')

    def translate_text(self, text, source_language = 'auto', target_language = 'en'):
        response = self.client.translate_text(
            Text = text,
            SourceLanguageCode = source_language,
            TargetLanguageCode = target_language
        )

        translation = {
            'translatedText': response['TranslatedText'],
            'sourceLanguage': response['SourceLanguageCode'],
            'targetLanguage': response['TargetLanguageCode']
        }

        return translation
