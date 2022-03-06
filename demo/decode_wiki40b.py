import re

import tensorflow_datasets as tfds
from nltk import sent_tokenize, word_tokenize

from japanese import Japanese


# TODO parse japanese and chinese sentence
REQUIRED_WORD_SEPARATION_LANGUAGES = [
    'ja', 'zh-cn', 'zh-tw', 'th', 
]

class DecodeWiki40b():

    def __init__(self, language_code) -> None:
        self.language_code = language_code
        
        # TODO correspond to chinese, korean...
        if language_code == 'ja':
            self.jp_utils = Japanese()
            self._wiki40b_sentences = self._decode_wiki40b_japanese()
        else:
            self._wiki40b_sentences = self._decode_wiki40b(language_code)
        self._word_index_dict = self._get_dict(self._wiki40b_sentences)
        
    def _is_required_word_separation(self):
        return self.language_code in REQUIRED_WORD_SEPARATION_LANGUAGES
    
    def _decode_wiki40b(self, wiki40b_language_code):
            
        # test : val : train = 5 : 5 : 90
        ds = tfds.load('wiki40b/' + wiki40b_language_code, split='test')
        start_paragraph = False
        sentences = []
        for wiki in ds.as_numpy_iterator():
            for text in wiki['text'].decode().split('\n'):
                if start_paragraph:
                    text = text.replace('_NEWLINE_', '')
                    text = self.replace_num(text)
                    # TODO! fix language hard coding
                    # TODO https://www.nltk.org/api/nltk.tokenize.html
                    sentences += sent_tokenize(text, language='russian')
                    start_paragraph = False
                if text == '_START_PARAGRAPH_':
                    start_paragraph = True
        sentences = [s.lower() for s in sentences]
        
        return sentences
    
    def _decode_wiki40b_japanese(self):
        ds = tfds.load('wiki40b/' + 'ja', split='test')
        start_paragraph = False
        sentences = []
        for wiki in ds.as_numpy_iterator():
            for text in wiki['text'].decode().split('\n'):
                if start_paragraph:
                    text = text.replace('_NEWLINE_', '')
                    sentences += text.split('。')
                    start_paragraph = False
                if text == '_START_PARAGRAPH_':
                    start_paragraph = True
        sentences = [self.spacing_jp_sentence(s) for s in sentences]
        return sentences

    def spacing_jp_sentence(self, sentence):
        return self.jp_utils.spacing_sentence(sentence)

    # TODO clean    
    def replace_num(self, text, replace_chalacter = 'X'):
        
        one_replace_chalacter = ' ' + replace_chalacter * 1 + ' '
        text = re.sub(' \d{1} ', one_replace_chalacter, text)
        two_replace_chalacter = ' ' + replace_chalacter * 2 + ' '
        text = re.sub(' \d{2} ', two_replace_chalacter, text)
        three_replace_chalacter = ' ' + replace_chalacter * 3 + ' '
        text = re.sub(' \d{3} ', three_replace_chalacter, text)
        four_replace_chalacter = ' ' + replace_chalacter * 4 + ' '
        text = re.sub(' \d{4} ', four_replace_chalacter, text)
        return text

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

        