from google.cloud import texttospeech
from pydub import AudioSegment

class TextToSpeech():

    def __init__(self, language, speaking_rate=1.0) -> None:
        self.language = language
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(language_code=language,ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
        self.audio_config = texttospeech.AudioConfig(
            sample_rate_hertz=48000,
            # audio_encoding=texttospeech.AudioEncoding.MP3,
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            speaking_rate=speaking_rate
        )

    def synthesize_text(self,text, spacing=False):
        # TODO jp, ch, kr
        if spacing:
            text = text.replace(' ', '. ')

        input_text = texttospeech.SynthesisInput(text=text)

        response = self.client.synthesize_speech(
            request={"input": input_text, "voice": self.voice,
                    "audio_config": self.audio_config}
        )

        return AudioSegment(
            data=response.audio_content)
