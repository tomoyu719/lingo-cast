from google.cloud import texttospeech
from pydub import AudioSegment


def synthesize_text(text, language):
    """Synthesizes speech from the input string of text."""

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        # language_code="en-US",
        # language_code="ja-JP",
        language_code=language,
        # name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        sample_rate_hertz=16000,
        # audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        audio_encoding=texttospeech.AudioEncoding.MP3,
        # audio_encoding=texttospeech.AudioEncoding.AUDIO_ENCODING_UNSPECIFIED,
        # speaking_rate=0.5

    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice,
                 "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    # with open('outputs/' + output_name + ".mp3", "wb") as out:
    #     out.write(response.audio_content)
    # print('Audio content written to file "output.mp3"')
    return AudioSegment(
        data=response.audio_content, sample_width=2, frame_rate=16000, channels=2)
    # return response.audio_content
