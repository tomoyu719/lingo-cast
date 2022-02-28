from dataclasses import dataclass, field
import re
import MeCab
import ipadic

import tensorflow_datasets as tfds
from utility.russian.word_morph import WordMorph

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
        self._wiki40b_sentences, self._word_index_dict, self.word_counter = self._decode_wiki40b(
            language_code)
        tmp = [w[0] for w in self.word_counter]
        self.top100words = tmp[:100]

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

        start_paragraph = False
        sentences = []
        for wiki in ds.as_numpy_iterator():
            for text in wiki['text'].decode().split('\n'):
                if start_paragraph:
                    text = text.replace('_NEWLINE_', '').lower()
                    # num => X
                    text = re.sub('\d', 'X', text)
                    # TODO '.'で分割できない言語に対応
                    sentences += text.split('.')
                    start_paragraph = False
                if text == '_START_PARAGRAPH_':
                    start_paragraph = True
        
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


class CreateExampleSentence():

    def __init__(self, language_code, is_include_other_word_form=False) -> None:
        self.language_code = language_code
        self.decodeWiki40b = DecodeWiki40b(language_code)
        self.is_include_other_word_form = is_include_other_word_form
        self.morph = WordMorph(language_code)
        self.exclude_pos_list = self._get_exclude_pos_s()

    def _get_exclude_pos_s(self):
        if self.language_code == 'ru':
            # 'CONJ':接続詞(and, or等)、だいたいの単語に対して共起度が高いので、除外しないとだいたいの例文に接続詞が入り込んでしまう
            # TODO remove hard coding
            return ['CONJ']
        else:
            raise ValueError
    
    def _is_word_exclude_pos(self, word):
        pos = self.morph.get_word_pos(word)
        if pos in self.exclude_pos_list:
            return True
        return False

    def _is_idiom(self, word):
        s = re.split('[-_ ]', word)
        
        if len(s) > 1:
            return True
        return False     

    def _get_most_frequent_word_form_in_wiki40b(self, word):
        all_word_forms = self.morph.get_other_forms(word)
        frequent_count = -1
        most_frequent_word_form_in_wiki40b = ''
        for w in all_word_forms:
            sentences_contain_word = self.decodeWiki40b.get_sentences_contain_word(w)
            if len(sentences_contain_word) > frequent_count:
                frequent_count = len(sentences_contain_word)
                most_frequent_word_form_in_wiki40b = w
        return most_frequent_word_form_in_wiki40b

    # 1単語ずつ ずらしながらn文字分抜き出す
    def n_gram(self, words, n):
        return [ ' '.join(words[idx:idx + n]) for idx in range(len(words) - n + 1)]
    
    # TODO return class not (str, value) 
    def make_example_sentence(self, word) -> str:
        word = word.lower()

        # idiomならそのままで良し?
        if self._is_idiom(word):
            return word, 0

        # if self.is_include_other_word_form:
        
        sentences_contain_word = self.decodeWiki40b.get_sentences_contain_word(word)
        count_other_word = {}
        for sentence in sentences_contain_word:
            split = sentence.split()
            for w in split:
                if w == word:
                    continue
                if w not in count_other_word:
                    count_other_word[w] = 1
                else:
                    count_other_word[w] += 1
        count_other_word = dict(sorted(count_other_word.items(),key=lambda item: item[1], reverse=True))
        count_other_word = {k:v for k, v in count_other_word.items() if not self._is_word_exclude_pos(k)}

        n_grams = []
        for sentence in sentences_contain_word:
            split = sentence.split()
            for i in range(2, 6):
                n_grams += self.n_gram(split, i)
        
        # remove sentence not contain word 
        n_grams = [x for x in n_grams if word in x ]
        
        # scoring sentence
        sentences_with_score = []
        for sentence in n_grams:
            split = sentence.split()
            count = 0
            for word in split:
                if word in count_other_word.keys() and word not in self.decodeWiki40b.top100words:
                    count += count_other_word[word]
            sentences_with_score.append(SentenceScore(sentence, count))
        
        sentences_with_score.sort(reverse=True)
        
        if len(sentences_with_score) == 0:
            return word, 0
        
        return sentences_with_score[0].sentence, sentences_with_score[0].count


@dataclass(order=True)
class SentenceScore():
    sort_index: int = field(init=False)
    sentence: str
    count: int
    
    def __post_init__(self):
        self.sort_index = self.count
