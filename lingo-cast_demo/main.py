import os
import datetime
from get_audio_from_words import get_audio_from_words
from make_example_sentence_from_wiki40b import MakeExampleSentenceFromWiki40b
from text_to_speech import synthesize_text
from translate import translate
from utility.get_words import get_words
from utility.russian.word_morph import WordMorph
from pydub import AudioSegment


def main():
    file_dir = '/Users/kitanotoshiyuki/lingo-cast/words/russian/duolingo/no_duplicate_russian_words/'
    out_dir = '/Users/kitanotoshiyuki/lingo-cast/outputs/russian/duolingo/'

    file_names = os.listdir(file_dir)
    now_str = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    out_dir += now_str + '/'
    os.mkdir(out_dir)

    wiki40b_language_code = 'ru'
    m = MakeExampleSentenceFromWiki40b(wiki40b_language_code)
    exclude_pos_list = ['CONJ']

    morph = WordMorph()

    language_source = "ru-RU"
    language_target = "en-US"

    # TODO add interval ↓ doesnt work
    # interval = AudioSegment.silent(duration=3000, frame_rate=16000)
    for file_name in file_names:
        file_path = file_dir + file_name
        words = get_words(file_path)
        audios = []
        for word in words:
            word_audio = synthesize_text(word, language_source)
            word_inflected_forms = morph.get_inflected_forms(word)
            example_sentence = m.make_example_sentence(
                word_inflected_forms, exclude_pos_list)
            example_sentence_trans = translate(example_sentence,
                                               source_language='ru', target_language='en')
            example_sentence_trans_audio = synthesize_text(
                example_sentence_trans, language_target)

            example_sentence_audio = synthesize_text(
                example_sentence, language_source)
            audios += [word_audio, example_sentence_trans_audio,
                       example_sentence_audio, example_sentence_audio]

        audio = sum(audios)
        out_name = file_name.split('.')[0] + '.mp3'
        audio.export(out_dir + out_name, format="mp3")


if __name__ == '__main__':
    main()
