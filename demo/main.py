import argparse
import json
import os
from decode_input_file import decode_input_file
from make_example_sentence import MakeExampleSentence



def main():
    parser = argparse.ArgumentParser()
    
    # TODO? guess soruce language from words file
    parser.add_argument("-l","--language_code", help="wiki40b language code: https://research.google/pubs/pub49029/?hl=ja")
    parser.add_argument("-d", "--words_files_dir")
    parser.add_argument("-o", "--output_files_dir")
    parser.add_argument("-min","--min_example_sentence_length", type=int, default=3)
    parser.add_argument("-max","--max_example_sentence_length", type=int, default=5)
    parser.add_argument("-n","--ngram_num", type=int, default=3)

    args = parser.parse_args()
    
    # TODO error check
    file_names = os.listdir(args.words_files_dir)
    make_example_sentence = MakeExampleSentence(args.language_code, args.max_example_sentence_length, args.min_example_sentence_length, args.ngram_num)

    try:
        os.makedirs(args.output_files_dir)
    except FileExistsError:
        pass

    for i, file_name in enumerate(file_names):
        print(i+1,'/',len(file_names))
        file_path = args.words_files_dir + file_name
    
        output_json_name = file_name.split('.')[0] + '.json'
        source_words = decode_input_file(file_path, args.language_code)
        words_with_example_sentences = []
        for source_word in source_words:
            word_with_example_sentence = {}
            word_with_example_sentence['word'] = source_word
            # example_sentence = make_example_sentence.make_example_sentence(source_word)
            # word_with_example_sentence['example'] = example_sentence
            # word_with_example_sentence['example_translation'] = translator.translate(example_sentence)
            # example_sentences, words_with_prob = make_example_sentence.make_example_sentence(source_word)
            # example_sentences = make_example_sentence.make_example_sentence(source_word)
            example_sentence = make_example_sentence.make_example_sentence(source_word)
            word_with_example_sentence['example'] = example_sentence
            # word_with_example_sentence['example_translation'] = [translator.translate(s) for s in example_sentences]
            word_with_example_sentence['word_contain_sentence_num'] = make_example_sentence.word_contain_num
            words_with_example_sentences.append(word_with_example_sentence)

        with open(args.output_files_dir + output_json_name, 'w',encoding='utf8') as f:
            json.dump(words_with_example_sentences, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()
              