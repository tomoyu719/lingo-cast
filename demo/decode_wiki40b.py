import itertools
from re import S
import tensorflow_datasets as tfds
from nltk import sent_tokenize, word_tokenize

from nltk_languagecode import get_nltk_tokenizer_language_code, is_nltk_tokenizer_supported_language
from japanese import JapaneseUtils


# TODO parse japanese and chinese sentence
REQUIRED_WORD_SEPARATION_LANGUAGES = [
    'ja', 'zh-cn', 'zh-tw', 'th', 
]

class DecodeWiki40b():

    def __init__(self, language_code) -> None:
        self.language_code = language_code
        if language_code == 'ja':
            self.ja_text_separator = JapaneseUtils().split_to_sentences
            self.ja_sentence_sepatator = JapaneseUtils().separate_sentence
        self.is_nltk_tokenizer_supported_language = is_nltk_tokenizer_supported_language(self.language_code)
        if self.is_nltk_tokenizer_supported_language:
            self.nltk_languarge_code = get_nltk_tokenizer_language_code(self.language_code)
        texts = self.decode_wiki40b()
        texts = [t.lower() for t in texts]
        sentences = [sentence for t in texts for sentence in self.split_to_sentences(t)]
        self.sentences_tokenized = [self.split_to_words(s) for s in sentences]
        # get sentences_indices by word
        self.sentences_indices_dict = self.get_dict(self.sentences_tokenized)
    
    def decode_wiki40b(self) -> list:
        # test : val : train = 5 : 5 : 90
        # dss = [tfds.load('wiki40b/' + self.language_code, split='test'), tfds.load('wiki40b/' + self.language_code, split='validation')]
        ds = tfds.load('wiki40b/' + self.language_code, split='test')
        # ds = tfds.load('wiki40b/' + self.language_code, split='validation')
        start_paragraph = False
        texts = []
        for wiki in ds.as_numpy_iterator():
            for text in wiki['text'].decode().split('\n'):
                if start_paragraph:
                    text = text.replace('_NEWLINE_', ' ')
                    texts.append(text)
                    start_paragraph = False
                if text == '_START_PARAGRAPH_':
                    start_paragraph = True
        
        return texts


    def split_to_sentences(self, text) -> list:
        if self.is_nltk_tokenizer_supported_language:
            return sent_tokenize(text, self.nltk_languarge_code)
        elif self.language_code == 'ja':
            return self.ja_text_separator(text)
        else:
            raise ValueError('not supported language-code: {language_code}')
    
    # def split_to_words(self, sentences):
    def split_to_words(self, sentence):
        if self.is_nltk_tokenizer_supported_language:
            # return [word_tokenize(s, self.nltk_languarge_code) for s in sentences]
            return word_tokenize(sentence, self.nltk_languarge_code)
        elif self.language_code == 'ja':
            # return [japanese_utils.separate_sentence(s) for s in sentences]
            return self.ja_sentence_sepatator(sentence)
        else:
            raise ValueError('not supported language-code: {language_code}')
    
    # TODO clean    
    # def replace_num(self, text, replace_chalacter = 'X'):
        
    #     one_replace_chalacter = ' ' + replace_chalacter * 1 + ' '
    #     text = re.sub(' \d{1} ', one_replace_chalacter, text)
    #     two_replace_chalacter = ' ' + replace_chalacter * 2 + ' '
    #     text = re.sub(' \d{2} ', two_replace_chalacter, text)
    #     three_replace_chalacter = ' ' + replace_chalacter * 3 + ' '
    #     text = re.sub(' \d{3} ', three_replace_chalacter, text)
    #     four_replace_chalacter = ' ' + replace_chalacter * 4 + ' '
    #     text = re.sub(' \d{4} ', four_replace_chalacter, text)
    #     return text

    def get_dict(self, sentences_tokenized):
        word_index_dict = {}
        for i, sent in enumerate(sentences_tokenized):
            for word in sent:
                if word not in word_index_dict:
                    word_index_dict[word] = [i]
                else:
                    word_index_dict[word].append(i)
        return word_index_dict

    def get_tokenized_sentences_contain_word(self, word) -> list:
        try:
            indices = self.sentences_indices_dict[word]
            return [self.sentences_tokenized[i] for i in indices]
        # word does not exist in wiki40b
        except KeyError:
            return []
    
    def get_tokenized_sentences_contain_words(self, words) -> list:
        # wordsの全ての単語を含む文章のインデックスを取得
        sentences_indieces_contain_words = {}
        for i, word in enumerate(words):
            if i == 0:
                try:
                    sentences_indieces_contain_words = set(self.sentences_indices_dict[word])
                except KeyError:
                    return []
            else:
                try:
                    indices = self.sentences_indices_dict[word]
                    sentences_indieces_contain_words = sentences_indieces_contain_words & set(indices )
                except KeyError:
                    return []
        # 得られたインデックスから文章を取得
        sentences_tokenized_contain_words = [self.sentences_tokenized[i] for i in sentences_indieces_contain_words]

        return sentences_tokenized_contain_words

    # TODO? 文中に単語が重複した場合、sentence.index(word)は最初の単語のインデックスを返すので、文中にイディオムが存在する場合でも、存在しない判定をされる可能性がある
    def get_tokenized_sentences_contain_idiom(self, idiom) -> list:
        words_of_idiom = idiom.split()
        sentences_tokenized_contain_words = self.get_tokenized_sentences_contain_words(words_of_idiom)
        
        # idiom中の全ての単語を含む文章から、idiomが正しい語順のものを取得
        sentences_tokenized_contain_idiom = []
        for sentence in sentences_tokenized_contain_words:
            for i, word in enumerate(words_of_idiom):
                word_position = sentence.index(word)
                if i == 0:                    
                    initial_word_position = word_position
                elif i == len(words_of_idiom) - 1 and initial_word_position + i == word_position:
                    sentences_tokenized_contain_idiom.append(sentence)
                if initial_word_position + i != word_position:
                    break
        return sentences_tokenized_contain_idiom


    def get_word_num_in_sentences(self, word) -> int:
        try:
            indices = self.sentences_indices_dict[word]
            word_num = len(indices)
            return word_num
        except KeyError:
            return 0

        