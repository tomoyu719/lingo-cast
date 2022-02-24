import json
from make_example_sentence_from_wiki40b import MakeExampleSentenceFromWiki40b
from process_language_code import LanguageCode
from remove_duplicate_word import remove_duplicate_word
from text_to_speech import MakeAudio
from mytranslater import MyTransrator
from utility.get_words import get_source_words
from utility.russian.word_morph import WordMorph


def main():
    # TODO 翻訳と音声の言語設定をまとめる
    source_language = 'ru'
    target_language = 'en'

    language_codes = LanguageCode(source_language, target_language)    

    # TODO commnd line から設定できるようにする
    
    # remove same normalized word from source file
    # is_remove_duplicate_word = True
    is_remove_duplicate_word = False
    # get sentence not only original form but also other forms 
    # is_including_other_word_form = True
    # is_including_other_word_form = False

    # wiki40b_language_code = 'ru'
    # wiki40b_language_code = 'ja'


    audio_language_source_speaking_rate = 0.8
    # 発音
    # audio_language_source = "ru-RU"
    # audio_language_target = "en-US"
    # audio_language_target = "ja-JP"

    # 翻訳
    # trans_language_source = 'ru'
    # trans_language_target = 'en'
    # trans_language_target = 'ja'

    file_name = 'PrefixVerb.txt'
    file_dir = '/Users/kitanotoshiyuki/lingo-cast/lingo-cast_demo/words/russian/duolingo/Section3/'
    file_path = file_dir + file_name
    # file_path = '/Users/kitanotoshiyuki/lingo-cast/lingo-cast_demo/words/russian/duolingo/Section3/Speak2.txt'
    output_file_dir = '/Users/kitanotoshiyuki/lingo-cast/lingo-cast_demo/outputs/russian/duolingo/Section3/'
    # output_file_dir = '/Users/kitanotoshiyuki/lingo-cast/lingo-cast_demo/outputs/russian/duolingo/japanese/Section3/'
    
    output_file_name = file_name.split('.')[0] + '.mp3'
    output_json_name = file_name.split('.')[0] + '.json'
    output_file_path = output_file_dir + output_file_name

    # 'CONJ':接続詞(and, or等)、だいたいの単語に対して共起度が高いので、除外しないとだいたいの例文に接続詞が入り込んでしまう
    exclude_pos_list = ['CONJ']

    make_example_sentence = MakeExampleSentenceFromWiki40b(language_codes.wiki40b_code, exclude_pos_list)

    translator = MyTransrator(language_codes.source_translation_code, language_codes.target_translation_code)
    
    text_to_speech_source = MakeAudio(language_codes.source_audio_code, speaking_rate=audio_language_source_speaking_rate)
    text_to_speech_target = MakeAudio(language_codes.target_audio_code)

    # TODO add interval under sentence doesnt work
    # interval = AudioSegment.silent(duration=3000, frame_rate=16000)
    
    # 例文音声作成用の単語リストを読み込む
    words = get_source_words(file_path)
    if is_remove_duplicate_word:
        words = remove_duplicate_word(words)
    
    morph = WordMorph()

    audios = []
    word_with_example_sentences = []
    # TODO functionalize
    for i, word in enumerate(words):
        print(i+1, '/', len(words))
        word_with_example_sentence = {}
        # word = morph.get_normalized_word(word)
        # word_with_example_sentence['word'] = word
        example_sentence, count = make_example_sentence.make_example_sentence(word)
        word_with_example_sentence['example'] = example_sentence
        word_with_example_sentence['count_in_dataset'] = count
        example_sentence_trans = translator.translate(example_sentence)
        word_with_example_sentence['translation'] = example_sentence_trans
        word_with_example_sentences.append(word_with_example_sentence)

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

    with open(output_file_dir + output_json_name, 'w',encoding='utf8') as f:
        json.dump(word_with_example_sentences, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
