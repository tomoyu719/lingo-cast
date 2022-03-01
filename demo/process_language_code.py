import json


class LanguageCode():

    def __init__(self, source_language_code, target_language_code) -> None:
        self.wiki40b_code = source_language_code
        # TODO error handling
        with open('wiki40b_language_codes.txt') as f:
            wiki40b_language_codes = [s.strip() for s in f.readlines()]
            if source_language_code not in wiki40b_language_codes and target_language_code not in wiki40b_language_codes:
                raise ValueError()
        
        # TODO error handling
        with open('language_code.json') as f:
            df = json.load(f)
            self.source_audio_code = df[source_language_code]["audio_code"]
            self.source_translation_code = df[source_language_code]["translation_code"]
            self.target_audio_code = df[target_language_code]["audio_code"]
            self.target_translation_code = df[target_language_code]["translation_code"]
