from pydub import AudioSegment
from text_to_speech import synthesize_text
from translate import translate


def get_audio_from_words(word, language):
    audio = AudioSegment.empty()
    # interval = AudioSegment.silent(duration=3000, frame_rate=16000)

    origin_audio = synthesize_text(word, language=language)
    # origin_audiosegment = AudioSegment(data=origin_audio,sample_width=2,frame_rate=44100,channels=2)
    origin_audiosegment = AudioSegment(
        data=origin_audio, sample_width=2, frame_rate=16000, channels=2)

    trans = translate(word, source_language='ru', target_language='en')
    trans_audio = synthesize_text(trans, language="en-US")
    trans_audiosegment = AudioSegment(
        data=trans_audio, sample_width=2, frame_rate=16000, channels=2)

    audio += origin_audiosegment + trans_audiosegment + origin_audiosegment
    # TODO add interval
    # audio += interval
    return audio
