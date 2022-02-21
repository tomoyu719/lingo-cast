import time
from make_example_sentence_from_wiki40b import MakeExampleSentenceFromWiki40b
from text_to_speech import MakeAudio
from mytranslater import MyTransrator
from utility.get_words import get_source_words


def main():
    # TODO 翻訳と音声の言語設定をまとめる
    # source_language = 'ru'
    # target_language = 'en'
    # TODO commnd line から設定できるようにする

    wiki40b_language_code = 'ru'

    # 発音
    audio_language_source = "ru-RU"
    audio_language_target = "en-US"

    # 翻訳
    trans_language_source = 'ru'
    trans_language_target = 'en'

    file_name = 'part2.txt'
    file_dir = '/Users/kitanotoshiyuki/lingo-cast/lingo-cast_demo/words/russian/duolingo/no_duplicate_russian_words/'
    output_file_dir = '/Users/kitanotoshiyuki/lingo-cast/lingo-cast_demo/outputs/russian/duolingo/'

    file_path = file_dir + file_name
    output_file_name = file_name.split('.')[0] + '.mp3'
    output_file_path = output_file_dir + output_file_name

    make_example_sentence = MakeExampleSentenceFromWiki40b(wiki40b_language_code)

    # 'CONJ':接続詞(and, or等)、だいたいの単語に対して共起度が高いので、除外しないとだいたいの例文に接続詞が入り込んでしまう
    exclude_pos_list = ['CONJ']

    translator = MyTransrator(source_language=trans_language_source, target_language=trans_language_target)
    text_to_speech_source = MakeAudio(audio_language_source)
    text_to_speech_target = MakeAudio(audio_language_target)

    # TODO add interval under sentence doesnt work
    # interval = AudioSegment.silent(duration=3000, frame_rate=16000)
    
    # 例文音声作成用の単語リストを読み込む
    words = get_source_words(file_path)
    audios = []

    # TODO functionalize
    # for word in words[:2]:
    words_length = len(words)
    for i, word in enumerate(words):
        print(i+1, '/', words_length)
        example_sentence = make_example_sentence.make_example_sentence(
            word, exclude_pos_list)

        example_sentence_trans = translator.translate(example_sentence)

        word_audio = text_to_speech_source.synthesize_text(word)
        example_sentence_trans_audio = text_to_speech_target.synthesize_text(
            example_sentence_trans)
        example_sentence_audio = text_to_speech_source.synthesize_text(
            example_sentence)
        track = word_audio + example_sentence_trans_audio + example_sentence_audio + example_sentence_audio
        # track = word_audio + example_sentence_trans_audio + example_sentence_audio + example_sentence_audio + interval
        audios += [track]
    
    audio = sum(audios)
    audio.export(output_file_path, format="mp3")


if __name__ == '__main__':
    main()
