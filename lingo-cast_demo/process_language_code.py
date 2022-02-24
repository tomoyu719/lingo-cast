import json

from mytranslater import MyTransrator


class LanguageCode():
    def __init__(self, source_language_code, target_language_code) -> None:
        with open('language_code.json') as f:
            df = json.load(f)
            self.wiki40b_code = source_language_code
            self.source_audio_code = df[source_language_code]["audio_code"]
            self.source_translation_code = df[source_language_code]["translation_code"]
            self.target_audio_code = df[target_language_code]["audio_code"]
            self.target_translation_code = df[target_language_code]["translation_code"]
