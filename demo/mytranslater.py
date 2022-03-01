from googletrans import Translator


class MyTransrator():

    def __init__(self, source_language, target_language) -> None:
        self.translator = Translator()
        self.source_language = source_language
        self.target_language = target_language

    def translate(self, text):
        message = self.translator.translate(
            text, src=self.source_language, dest=self.target_language)
        return message.text
