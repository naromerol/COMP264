# NESTOR ROMERO - 301133331
# COMP264 MIDTERM

from chalice import Chalice
from services.translation_service import TranslationService

app = Chalice(app_name='Capabilities')

translation_service = TranslationService()

@app.route('/reviews', methods = ['GET'], cors = True)
def index():

    # variables definition
    review_count = 0
    reviews = []

    review_file = open('reviews_nestor.txt', 'r')
    # read lines from file
    for line in review_file:
        # keeps count of reviews
        review_count += 1
        
        # print(line)
        ts_result = translation_service.translate_text(line)
        reviews.append({
            "line" : line,
            "translation" : ts_result['translatedText'],
            "lang" : ts_result['sourceLanguage']
            })
        
    result = {
        "review_count" : review_count,
        "reviews" : reviews
    }

    return result