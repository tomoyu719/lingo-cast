from dataclasses import dataclass, field
import json
import random
import re
import string

import nltk
import MeCab
import ipadic

import tensorflow_datasets as tfds


# TODO parse japanese and chinese sentence
REQUIRED_WORD_SEPARATION_LANGUAGES = [
    'ja', 'zh-cn', 'zh-tw', 'th', 
]

class DecodeWiki40b():

    def __init__(self, language_code) -> None:
        self.language_code = language_code
        self._is_required_word_separation = self._is_required_word_separation()
        if self._is_required_word_separation:
            self.separator = self._separator()
        self._wiki40b_sentences, self._word_index_dict, word_counter = self._decode_wiki40b(
            language_code)
        

    def _is_required_word_separation(self):
        if self.language_code in REQUIRED_WORD_SEPARATION_LANGUAGES:
            return True
        return False

    #TODO rename 
    #TODO Separator class?
    def _separator(self):
        if self.language_code == 'ja':
            #MeCab.Tagger
            # return MeCab.Tagger("-Owakati")
            return MeCab.Tagger(f'-O wakati{ipadic.MECAB_ARGS}')
        else:
            raise ValueError
    
    # add spacing 
    # ex)今日はいい天気ですね　→ 今日 は いい 天気 です ね
    def _spacing(self, sentence):
        if self.language_code == 'ja':
            spaced_sentence = self.separator.parse(sentence)
            return spaced_sentence
        # elif language_code == 'zh-cn':
        # elif language_code == 'zh-tw':
        # elif language_code == 'th':
        else:
            raise ValueError


    # TODO? テキストを分割せずに一つの巨大な文字列として扱う？
    def _decode_wiki40b(self, wiki40b_language_code):
            
        # test : val : train = 5 : 5 : 90
        # ds = tfds.load('wiki40b/' + wiki40b_language_code, split='train')
        ds = tfds.load('wiki40b/' + wiki40b_language_code, split='test')

        spacing_pattern = '«»'+ string.punctuation

        start_paragraph = False
        sentences = []
        for wiki in ds.as_numpy_iterator():
            for text in wiki['text'].decode().split('\n'):
                if start_paragraph:
                    text = text.replace('_NEWLINE_', '').lower()
                    # replace num to X
                    text = re.sub('\d', 'X', text)
                    
                    # replace special calactors to X
                    # text = re.sub('[{spacing_pattern}]', ' ', text)

                    # TODO '.'で分割できない言語に対応
                    texts = text.split('.')
                    texts = [' '.join(nltk.word_tokenize(s)) for s in texts]
                    # sentences += text.split('.')
                    sentences += texts
                    # sentences += re.split('[{string.punctuation}]', text)
                    start_paragraph = False
                if text == '_START_PARAGRAPH_':
                    start_paragraph = True
        
        # for s in random.sample(sentences, 200):
        #     print(s)

        # raise ValueError

        if self._is_required_word_separation:
            sentences = [self._spacing(s) for s in sentences]
            raise ValueError

        # for optimization, create word-sentence dict {word(str):indices(list)}
        word_index_dict = {}
        word_counter = {}
        for i, s in enumerate(sentences):
            for word in s.split():
                if word not in word_index_dict:
                    word_index_dict[word] = [i]
                    word_counter[word] = 1
                else:
                    word_index_dict[word].append(i)
                    word_counter[word] += 1
        word_counter = sorted(word_counter.items(), key=lambda x:x[1], reverse=True)
        return sentences, word_index_dict, word_counter
    
    
    def get_sentences_contain_word(self, word):
        try:
            indices = self._word_index_dict[word]
            return  [self._wiki40b_sentences[i] for i in indices]
        # word does not exist in wiki40b
        except KeyError:
            return []

    def is_nltk_stopwords_supported_languge(self):
        stopwords_language_code = self.get_nltk_stopwords_languge_code()
        stopwords = nltk.corpus.stopwords.words(stopwords_language_code)
        return stopwords



class CreateExampleSentence():

    def __init__(self, language_code, is_include_other_word_form=False) -> None:
        self.language_code = language_code
        self.decodeWiki40b = DecodeWiki40b(language_code)
        # self.is_include_other_word_form = is_include_other_word_form
        self.stopwords = self._get_stopwords()

    def _is_language_supported_nltk_stopwords(self):
        with open('nltk_stopwords_supported_language_code.json') as f:
            df = json.load(f)
            is_language_supported_nltk_stopwords = self.language_code in df.keys()
            return is_language_supported_nltk_stopwords
    
    def _get_nltk_stopwords_languge_code(self):
        with open('nltk_stopwords_supported_language_code.json') as f:
            df = json.load(f)
            return df[self.language_code]

    def _get_stopwords(self):
        if self._is_language_supported_nltk_stopwords():
            nltk.download('stopwords')
            nltk_stopwords_language_code = self._get_nltk_stopwords_languge_code()
            nltk_stopwords = nltk.corpus.stopwords.words(nltk_stopwords_language_code)
            return nltk_stopwords
        # TODO implemant for other language not supported by nltk
        else:
            raise ValueError()

    def _is_idiom(self, word):
        s = re.split('[-_ ]', word)        
        if len(s) > 1:
            return True
        return False     

    # 1単語ずつ ずらしながらn文字分抜き出す
    def n_gram(self, split_sentence, n):
        return [ ' '.join(split_sentence[idx:idx + n]) for idx in range(len(split_sentence) - n + 1)]

    def get_word_contained_n_grams(self, word, sentences, min_sentence_length, max_sentence_length):
        n_grams = []
        for sentence in sentences:
            split = sentence.split()
            for i in range(min_sentence_length, max_sentence_length + 1):
                n_grams += self.n_gram(split, i)
        # remove sentence not contained word 
        n_grams = [x for x in n_grams if word in x ]        
        return n_grams

    # for scoring example sentence, count other words from sentences contain source-word, except stopwords
    def count_other_words(self, word, sentences):
        word_counter = {}
        for sentence in sentences:
            split = sentence.split()
            for w in split:
                if w == word or w in self.stopwords or w in string.punctuation:
                    continue
                if w not in word_counter:
                    word_counter[w] = 1
                else:
                    word_counter[w] += 1
        return word_counter

    # scoring sentence with add other word count
    def scoring_sentence(self, sentences, word_counter):
        example_sentences = []
        for sentence in sentences:
            split = sentence.split()
            count = 0
            for word in split:
                if word in self.stopwords or word in string.punctuation:
                    continue
                if word in word_counter.keys():
                    count += word_counter[word]
            example_sentences.append(ExampleSentence(sentence, count))
        return example_sentences


    def make_example_sentence(self, source_word, min_sentence_length, max_sentence_length) -> str:
        source_word = source_word.lower()

        # idiomならそのままで良し?
        if self._is_idiom(source_word):
            return source_word, 0
        
        # for optimization
        sentences_contain_source_word = self.decodeWiki40b.get_sentences_contain_word(source_word)
        
        # source word doesnt exists in dataset
        if len(sentences_contain_source_word) == 0:
            return source_word

        word_counter = self.count_other_words(source_word, sentences_contain_source_word)
        
        word_contained_n_grams = self.get_word_contained_n_grams(source_word, sentences_contain_source_word, min_sentence_length, max_sentence_length)
        # scoring sentence
        example_sentences = self.scoring_sentence(word_contained_n_grams, word_counter)
        
        example_sentences.sort(reverse=True)
        highest_scored_example_sentence = example_sentences[0].sentence
        
        return highest_scored_example_sentence

@dataclass(order=True)
class ExampleSentence():
    sort_index: int = field(init=False)
    sentence: str
    count: int
    
    def __post_init__(self):
        # self.score = self.count / len(self.sentence.split())
        # self.sort_index = self.score
        self.sort_index = self.count
