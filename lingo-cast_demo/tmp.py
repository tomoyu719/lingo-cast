from pydub import AudioSegment
from translate import translate
from text_to_speech import synthesize_text


out_path = '/Users/kitanotoshiyuki/lingo-cast/outputs/tmp/'

language_source = "ru-RU"
language_target = "en-US"

word = 'его'
e_s = 'это его яблоко'
e_s_trans = translate(e_s, source_language='ru', target_language='en')

word_audio = synthesize_text(word, language_source)
e_s_audio = synthesize_text(e_s, language_source)
e_s_trans_audio = synthesize_text(e_s_trans, language_target)

interval = AudioSegment.silent(duration=50000, frame_rate=16000)
# interval = AudioSegment.silent(duration=50000)
print(interval)
audios = []
for i in range(2):
    audios += [word_audio,  e_s_trans_audio, e_s_audio, e_s_audio, interval]
audio = sum(audios)
audio.export(out_path + 'tmp.mp3', format="mp3")
