import argparse
import json
import os
from make_example_sentence_from_wiki40b import MakeExampleSentence
from process_language_code import LanguageCode
from text_to_speech import MakeAudio
from mytranslater import MyTransrator
from utility.get_words import get_source_words
from utility.russian.word_morph import WordMorph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--source_language_code")
    parser.add_argument("-t","--target_language_code", default='en')
    
    # TODO considar input file
    parser.add_argument("-d", "--words_files_dir")
    parser.add_argument("-r","--remove_duplicate", help="Remove duplicate normalized word in one file", default=True)
    parser.add_argument("-i","--include_other_form", help="Create example sentence using not only origin word form, but also other word forms", default=True)

    args = parser.parse_args()

    # file_dir = '/Users/kitanotoshiyuki/lingo-cast/lingo-cast_demo/words/russian/duolingo/Section3/'
    output_file_dir = '/Users/kitanotoshiyuki/lingo-cast/demo/outputs/russian/duolingo/Section3/'

    language_codes = LanguageCode(args.source_language_code, args.target_language_code)    

    audio_language_source_speaking_rate = 0.8

    make_example_sentence = MakeExampleSentence(language_codes.wiki40b_code, args.include_other_form)

    translator = MyTransrator(language_codes.source_translation_code, language_codes.target_translation_code)
    
    text_to_speech_source = MakeAudio(language_codes.source_audio_code, speaking_rate=audio_language_source_speaking_rate)
    text_to_speech_target = MakeAudio(language_codes.target_audio_code)
    morph = WordMorph(args.source_language_code)

    # TODO add interval under sentence doesnt work
    # interval = AudioSegment.silent(duration=3000, frame_rate=16000)
        
    file_names = os.listdir(args.words_files_dir)
    for i, file_name in enumerate(file_names):
        print(i+1,'/',len(file_names))
        file_path = args.words_files_dir + file_name
        output_file_name = file_name.split('.')[0] + '.mp3'
        output_json_name = file_name.split('.')[0] + '.json'
        
        words = get_source_words(file_path)
        if args.remove_duplicate:
            words = morph.remove_duplicate_word(words)

        audios = []
        word_with_example_sentences = []
        # TODO functionalize
        for word in words:
            
            word_with_example_sentence = {}
            word = morph.get_normalized_word(word)
            word_with_example_sentence['word'] = word
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
        audio.export(output_file_dir + output_file_name, format="mp3")

        with open(output_file_dir + output_json_name, 'w',encoding='utf8') as f:
            json.dump(word_with_example_sentences, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
