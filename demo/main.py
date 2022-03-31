import argparse
import json
import os
from decode_input_file import decode_input_file
from make_example_sentence import MakeExampleSentence


def main():
    parser = argparse.ArgumentParser()
    
    # TODO? guess soruce language from words file
    parser.add_argument("-l","--language_code", help="wiki40b language code: https://research.google/pubs/pub49029/?hl=ja")
    parser.add_argument("-w", "--words_file_path")
    parser.add_argument("-o", "--output_file_dir", default='output')
    parser.add_argument("-min","--min_example_sentence_length", type=int, default=2)
    parser.add_argument("-max","--max_example_sentence_length", type=int, default=3)
    parser.add_argument("-n","--ngram_num", type=int, default=3)
    args = parser.parse_args()
    
    # TODO error check
    if os.path.isfile(args.words_file_path):
        file_dir = os.path.split(args.words_file_path)[0]
        file_names = [os.path.basename(args.words_file_path)]
    elif os.path.isdir(args.words_file_path):
        file_dir = args.words_file_path
        file_names = os.listdir(args.words_file_path)
    else:
        raise ValueError

    output_dir = os.path.join(args.output_file_dir, args.language_code)
    os.makedirs(output_dir, exist_ok=True)
    
    make_example_sentence = MakeExampleSentence(args.language_code, args.max_example_sentence_length, args.min_example_sentence_length, args.ngram_num)
    
    for n in file_names:
        file_path = os.path.join(file_dir, n)
        source_words = decode_input_file(file_path, args.language_code)
        words_with_example_sentences = []
        for source_word in source_words:
            example_sentence, probs = make_example_sentence.make_example_sentence(source_word)
            word_contain_sentence_num = make_example_sentence.count_word_contain_sentence_num(source_word)
            data = {}
            data['word'] = source_word
            data['example'] = example_sentence
            data['probs'] = ', '.join(probs)
            data['word_contain_sentence_num'] = word_contain_sentence_num
            words_with_example_sentences.append(data)
        
        output_name = os.path.basename(file_path).split('.')[0] + '.json'
        output_json_path = os.path.join(output_dir , output_name)
        
        with open(output_json_path, 'w', encoding='utf8') as f:
            json.dump(words_with_example_sentences, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
