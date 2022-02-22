from google.cloud import texttospeech
from pydub import AudioSegment

class MakeAudio():

    def __init__(self, language, speaking_rate=1.0) -> None:
        self.language = language
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(language_code=language,ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
        self.audio_config = texttospeech.AudioConfig(
            sample_rate_hertz=16000,
            # audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            audio_encoding=texttospeech.AudioEncoding.MP3,
            # audio_encoding=texttospeech.AudioEncoding.AUDIO_ENCODING_UNSPECIFIED,
            speaking_rate=speaking_rate
        )

    def synthesize_text(self,text):

        input_text = texttospeech.SynthesisInput(text=text)

        response = self.client.synthesize_speech(
            request={"input": input_text, "voice": self.voice,
                    "audio_config": self.audio_config}
        )

        return AudioSegment(
            data=response.audio_content, sample_width=2, frame_rate=16000, channels=2)
