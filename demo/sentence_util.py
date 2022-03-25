import json
import re

from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.lm.preprocessing import pad_sequence

class SentenceUtil():
    def __init__(self, language_code) -> None:
        self.language_code = language_code
        self.is_nltk_tokenizer_supported_language = self.is_nltk_tokenizer_supported_language(language_code)
        if self.is_nltk_tokenizer_supported_language:
            self.nltk_languarge_code = self.get_nltk_tokenizer_language_code(language_code)
        # self.nltk_languarge_code = self.get_nltk_tokenizer_language_code(language_code)

    def split_to_sentences(self, text) -> list:
        if self.is_nltk_tokenizer_supported_language:
            return sent_tokenize(text, self.nltk_languarge_code)
        elif self.language_code == 'ja':
            return self.ja_text_separator(text)
        else:
            return text.split('.')

    def tokenize_sentence(self, sentence):
        sentence = self.spacing_spchars(sentence)
        if self.is_nltk_tokenizer_supported_language:
            nltk_languarge_code = self.get_nltk_tokenizer_language_code(self.language_code)
            return word_tokenize(sentence, nltk_languarge_code)
        elif self.language_code == 'ja':
            return self.ja_sentence_sepatator(sentence)
        else:
            return sentence.split()
        
    def padding_sentence(self, sentence_tokenized, ngram_num):
        sentence_padded = list(pad_sequence(sentence_tokenized ,pad_left=True, left_pad_symbol="<s>",pad_right=True, right_pad_symbol="</s>", n=ngram_num))
        return sentence_padded

    def is_nltk_tokenizer_supported_language(self, language_code) -> bool:
        with open('wiki40b_code_to_nltk_tokenizer_code.json') as f:
            d = json.load(f)
        return language_code in d

    def get_nltk_tokenizer_language_code(self, language_code) -> str:
        with open('wiki40b_code_to_nltk_tokenizer_code.json') as f:
            d = json.load(f)
        return d[language_code]    
    
    def spacing_spchars(self, text):
        spchars = re.findall('\W', text)
        spchars = set(spchars)
        spchars.discard(' ')
        spchars.discard('.')
        spchars.discard('-')
        spchars.discard('\'')
        for c in spchars:
            text = text.replace(c, ' ' + c + ' ')
        text = re.sub('[ ]+', ' ', text)
        return text
    
    def replace_num(self, text, max_digits = 4,replace_chalacter = 'X'):
        for digit in range(1, max_digits + 1):
            replacement = replace_chalacter * digit
            text = re.sub('\d{%s}' % digit, replacement, text)
        return text

    #TODO 
    def is_idiom(self, word):
        return len(word.split()) > 1