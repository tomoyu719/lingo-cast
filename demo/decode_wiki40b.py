from dataclasses import dataclass, field
import json
import random
import re
import string
import time

from nltk import sent_tokenize, word_tokenize, corpus, download
from nltk.lm        import Vocabulary
from nltk.lm.models import MLE
from nltk.util      import ngrams
from nltk.lm.preprocessing import pad_both_ends
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
        # self._is_required_word_separation = self._is_required_word_separation()
        # if self._is_required_word_separation:
        #     self.separator = self._separator()
        # self.wiki40b_sentences = self._decode_wiki40b(language_code)
        self._wiki40b_sentences = self._decode_wiki40b(language_code)
        self._word_index_dict = self._get_dict(self._wiki40b_sentences)
        
        
    # def _is_required_word_separation(self):
    #     if self.language_code in REQUIRED_WORD_SEPARATION_LANGUAGES:
    #         return True
    #     return False

    #TODO rename 
    #TODO Separator class?
    # def _separator(self):
    #     if self.language_code == 'ja':
    #         #MeCab.Tagger
    #         # return MeCab.Tagger("-Owakati")
    #         return MeCab.Tagger(f'-O wakati{ipadic.MECAB_ARGS}')
    #     else:
    #         raise ValueError
    
    # add spacing 
    # ex)今日はいい天気ですね　→ 今日 は いい 天気 です ね
    # def _spacing(self, sentence):
    #     if self.language_code == 'ja':
    #         spaced_sentence = self.separator.parse(sentence)
    #         return spaced_sentence
    #     # elif language_code == 'zh-cn':
    #     # elif language_code == 'zh-tw':
    #     # elif language_code == 'th':
    #     else:
    #         raise ValueError
    def _decode_wiki40b(self, wiki40b_language_code):
            
        # test : val : train = 5 : 5 : 90
        ds = tfds.load('wiki40b/' + wiki40b_language_code, split='test')
        start_paragraph = False
        sentences = []
        for wiki in ds.as_numpy_iterator():
            for text in wiki['text'].decode().split('\n'):
                if start_paragraph:
                    text = text.replace('_NEWLINE_', '')
                    # TODO! fix language hard coding
                    # TODO https://www.nltk.org/api/nltk.tokenize.html
                    sentences += sent_tokenize(text, language='russian')
                    start_paragraph = False
                if text == '_START_PARAGRAPH_':
                    start_paragraph = True
        sentences = [s.lower() for s in sentences]
        
        return sentences

    def _get_dict(self, sentences):
        word_index_dict = {}
        for i, s in enumerate(sentences):
            for word in word_tokenize(s):
                if word not in word_index_dict:
                    word_index_dict[word] = [i]
                else:
                    word_index_dict[word].append(i)
        return word_index_dict

    def get_sentences_contained_word(self, word):
        try:
            indices = self._word_index_dict[word]
            return  [self._wiki40b_sentences[i] for i in indices]
        # word does not exist in wiki40b
        except KeyError:
            return []

    def get_word_num_in_sentences(self, word):
        try:
            indices = self._word_index_dict[word]
            word_num = len(indices)
            return word_num
        # word does not exist in wiki40b
        except KeyError:
            return 0

        