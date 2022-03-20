import enum
import re
import string

import tensorflow_datasets as tfds
from nltk import sent_tokenize, word_tokenize
from nltk.lm.preprocessing import pad_sequence

from nltk_languagecode import get_nltk_tokenizer_language_code, is_nltk_tokenizer_supported_language
from japanese import JapaneseUtils

# TODO parse japanese and chinese sentence
REQUIRED_WORD_SEPARATION_LANGUAGES = [
    'ja', 'zh-cn', 'zh-tw', 'th', 
]

class DecodeWiki40b():

    def __init__(self, language_code, ngram_num, is_debug=True) -> None:
        self.language_code = language_code
        self.ngram_num = ngram_num
        self.is_debug = is_debug
        if language_code == 'ja':
            self.ja_text_separator = JapaneseUtils().split_to_sentences
            self.ja_sentence_sepatator = JapaneseUtils().separate_sentence
        self.is_nltk_tokenizer_supported_language = is_nltk_tokenizer_supported_language(self.language_code)
        if self.is_nltk_tokenizer_supported_language:
            self.nltk_languarge_code = get_nltk_tokenizer_language_code(self.language_code)
        # texts = self.decode_wiki40b()
        # sentences = [sentence for t in texts for sentence in self.split_to_sentences(t)]
        # sentences_tokenized = [self.split_to_words(s) for s in sentences]
        decoder = self.decode_wiki40b2()
        self.padded_sentences = []
        for d in decoder:
            self.padded_sentences += d
    
        # get sentence_indices by word
        self.sentences_indices_word_dict = self.get_dict(self.padded_sentences)
        # self.stopwords = self.get_stopwords(self.sentences_indices_word_dict)
    
    def decode_wiki40b(self, loading_paragraph_num = 5000000) -> list:
        # test : val : train = 5 : 5 : 90
        ds = tfds.load('wiki40b/' + self.language_code, split='test')
        start_paragraph = False
        paragraphs = []
        for wiki in ds.as_numpy_iterator():
            for text in wiki['text'].decode().split('\n'):
                if start_paragraph:
                    paragraph = text.replace('_NEWLINE_', ' ')
                    paragraph = paragraph.lower()
                    # paragraph = self.spacing_sp_chars(paragraph)
                    paragraph = self.replace_num(paragraph)
                    paragraphs.append(paragraph)
                    start_paragraph = False
                if text == '_START_PARAGRAPH_':
                    start_paragraph = True
                if len(paragraphs) > loading_paragraph_num:
                    return paragraphs
        return paragraphs
    
    def decode_wiki40b2(self):
        # test : val : train = 5 : 5 : 90
        if self.is_debug:
            ds = tfds.load('wiki40b/' + self.language_code, split='test')
        else:
            ds = tfds.load('wiki40b/' + self.language_code, split='train')
        start_paragraph = False
        
        for wiki in ds.as_numpy_iterator():
            for text in wiki['text'].decode().split('\n'):
                if start_paragraph:
                    text =  text.replace('_NEWLINE_', ' ')
                    text =  text.lower()
                    # text = self.spacing_sp_chars(text)
                    text = self.replace_num(text)
                    sentences = self.split_to_sentences(text)
                    sentences_tokenized = [self.split_to_words(s) for s in sentences]
                    sentences_padded = [self.padding_sentences(s) for s in sentences_tokenized]
                    yield sentences_padded
                    start_paragraph = False
                if text == '_START_PARAGRAPH_':
                    start_paragraph = True

    def padding_sentences(self, sentence_tokenized):
        sentence_padded = list(pad_sequence(sentence_tokenized ,pad_left=True, left_pad_symbol="<s>",pad_right=True, right_pad_symbol="</s>", n=self.ngram_num))
        return sentence_padded

    def get_stopwords(self, sentences_indices_word_dict, stopwords_num=100,):        
        stopwords = [k for k, v in sorted(sentences_indices_word_dict.items(), key=lambda item: len(item[1]), reverse=True)][:stopwords_num]
        return stopwords

    def split_to_sentences(self, text) -> list:
        if self.is_nltk_tokenizer_supported_language:
            return sent_tokenize(text, self.nltk_languarge_code)
        elif self.language_code == 'ja':
            return self.ja_text_separator(text)
        else:
            return text.split('.')
    
    def split_to_words(self, sentence):
        if self.is_nltk_tokenizer_supported_language:
            return word_tokenize(sentence, self.nltk_languarge_code)
        elif self.language_code == 'ja':
            # return [japanese_utils.separate_sentence(s) for s in sentences]
            return self.ja_sentence_sepatator(sentence)
        else:
            sentence = self.spacing_sp_chars(sentence)
            sentence_split = re.split('[ ]+', sentence)
            sentence_split = [w for w in sentence_split if w != '']
            return sentence_split
    
    def spacing_sp_chars(self, text):
        sp_chars = re.findall(r'[…?;:«»!,"()]', text)
        sp_chars = list(set(sp_chars))
        for char in sp_chars:
            text = re.sub(f'[{char}]', ' ' + char + ' ', text)
        return text

    # TODO clean    
    def replace_num(self, text, max_digits = 4,replace_chalacter = 'X'):
        for digit in range(1, max_digits + 1):
            replacement = replace_chalacter * digit
            text = re.sub('\d{%s}' % digit, replacement, text)
        return text

    def get_dict(self, sentences_tokenized):
        word_index_dict = {}
        for i, sent in enumerate(sentences_tokenized):
            for word in sent:
                if word not in word_index_dict:
                    word_index_dict[word] = [i]
                else:
                    word_index_dict[word].append(i)
        return word_index_dict

    def get_sentences_contain_word(self, word) -> list:
        try:
            indices = self.sentences_indices_word_dict[word]
            return [self.padded_sentences[i] for i in indices]
        # word does not exist in wiki40b
        except KeyError:
            return []
    
    def get_sentences_contain_words(self, words) -> list:
        # wordsの全ての単語を含む文章のインデックスを取得
        sentences_indieces_contain_words = {}
        for i, word in enumerate(words):
            if i == 0:
                try:
                    sentences_indieces_contain_words = set(self.sentences_indices_word_dict[word])
                except KeyError:
                    return []
            else:
                try:
                    indices = self.sentences_indices_word_dict[word]
                    sentences_indieces_contain_words = sentences_indieces_contain_words & set(indices )
                except KeyError:
                    return []
        # 得られたインデックスから文章を取得
        sentences_tokenized_contain_words = [self.padded_sentences[i] for i in sentences_indieces_contain_words]

        return sentences_tokenized_contain_words


    def get_word_num_in_sentences(self, word) -> int:
        try:
            indices = self.sentences_indices_word_dict[word]
            word_num = len(indices)
            return word_num
        except KeyError:
            return 0

        