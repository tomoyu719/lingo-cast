class SettingLanguage():
    def __init__(self, source_language, target_language='en') -> None:
        # TODO check existance language code in list file
        self.source_languge_audio = self._audio_language(source_language)
        self.target_languge_audio = self._audio_language(target_language)
        self.source_languge_translation = self._translation_language(source_language)
        self.target_languge_translation = self._translation_language(target_language)
    

    # TODO rename
    def _audio_language(self, language_code):
        return ''
    
    # TODO rename
    def _translation_language(self, language_code):
        return ''

    
