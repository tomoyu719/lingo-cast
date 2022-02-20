
def translate(text, source_language='en', target_language='ja'):
    from googletrans import Translator
    translator = Translator()
    message = translator.translate(
        text, src=source_language, dest=target_language)
    return message.text
