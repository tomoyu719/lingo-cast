from google.cloud import translate_v2 as translate

class MyTransrator():

    def __init__(self, target_language) -> None:
        self.translate_client = translate.Client()
        self.target_language = target_language

    def translate(self, text):
        result = self.translate_client.translate(text, target_language=self.target_language)
        return result["translatedText"]
        # return u"Translation: {}".format(result["translatedText"])
