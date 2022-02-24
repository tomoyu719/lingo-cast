import os
import re

import tensorflow_datasets as tfds
from utility.russian.russian_word_morph import RussianWordMorph


#  TODO 日本語、中国語などは文をparseする


class MakeExampleSentenceFromWiki40b():
    SA = '_START_ARTICLE_'
    SS = '_START_SECTION_'
    SP = '_START_PARAGRAPH_'
    NL = '_NEWLINE_'
    META_TAGS = [SA, SS, SP, NL]

    def __init__(self, wiki40b_language_code, exclude_pos_list=[], is_including_other_word_form=False) -> None:
        self.wiki40b_sentences, self.word_index_dict = self._decode_wiki40b(
            wiki40b_language_code)
        self.morph = RussianWordMorph()
        self.exclude_pos_list = exclude_pos_list
        self.is_including_other_word_form = is_including_other_word_form
        

    # TODO 数字等を置換する？　1994 -> XX    
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
                    sentences += text.split('.')
                    start_paragraph = False
                if text == '_START_PARAGRAPH_':
                    start_paragraph = True

        word_index_dict = {}
        for i, s in enumerate(sentences):
            for word in s.split():
                if word not in word_index_dict:
                    word_index_dict[word] = [i]
                else:
                    word_index_dict[word].append(i)
        return sentences, word_index_dict

    def _get_around_words2(self, word) -> list:
        try:
            indices = self.word_index_dict[word]
        # word doesnt exist in wiki40b
        except KeyError:
            return []
        short_sentences_contain_word = []
        sentences = [self.wiki40b_sentences[i] for i in indices]
        for s in sentences:
            split = s.split()
            index = split.index(word)
            
            short_sentence = word
            for i in range(index - 1, -1, -1):
                prev = split[i]
                pos = self.morph.get_word_pos(prev)
                if self.is_exclude_pos(pos):
                    break
                short_sentence = prev + ' ' + short_sentence
                if pos not in ['PRCL', 'PREP']:
                    break

            for i in range(index + 1, len(split)):
                next = split[i]
                pos = self.morph.get_word_pos(next)
                if self.is_exclude_pos(pos):
                    break
                short_sentence = short_sentence + ' ' + next
                if pos not in ['PRCL', 'PREP']:
                    break
            
            short_sentences_contain_word.append(short_sentence)
            
        return short_sentences_contain_word

    # TODO clean
    #Wiki40bから、 前+word,word+後, 前+word+後,を返す
    def _get_around_words(self, word) -> list:
        try:
            indices = self.word_index_dict[word]
        # word doesnt exist in wiki40b
        except KeyError:
            return []
        short_sentences_contain_word = []
        sentences = [self.wiki40b_sentences[i] for i in indices]
        for s in sentences:
            split = s.split()
            index = split.index(word)
            try:
                prev = split[index - 1]
                prev_pos = self.morph.get_word_pos(prev)
                if self.is_exclude_pos(prev_pos):
                    prev = None
                    continue
                s = prev + ' ' + word
                short_sentences_contain_word.append(s)
            except IndexError:
                prev = None
            try:
                next = split[index + 1]
                next_pos = self.morph.get_word_pos(next)
                if self.is_exclude_pos(next_pos):
                    next = None
                    continue
                # avoid end up with PREP(前置詞)
                if next_pos == 'PREP':
                    try:
                        next += ' ' + split[index + 2]
                    except IndexError:
                        next = next
                # avoid end up with PRCL(бы, же, лишь)
                if next_pos == 'PRCL':
                    try:
                        next += ' ' + split[index + 2]
                    except IndexError:
                        next = next
                s = word + ' ' + next
                short_sentences_contain_word.append(s)
            except IndexError:
                next = None
            if prev is not None and next is not None:
                s = prev + ' ' + word + ' ' + next
                short_sentences_contain_word.append(s)
        return short_sentences_contain_word
    
    def is_exclude_pos(self, pos):
        if pos in self.exclude_pos_list:
            return True
        return False

    def is_idiom(self, word):
        s = re.split('[-_ ]', word)
        
        if len(s) > 1:
            return True
        return False     

    def make_example_sentence(self, word) -> str:
        word = word.lower()

        # idiomならそのままで良し
        if self.is_idiom(word):
            return word

        example_sentences = []
        if self.is_including_other_word_form:
            all_word_forms = self.morph.get_inflected_forms(word)
            for word in all_word_forms:
                # example_sentences += self._get_around_words(word)
                example_sentences += self._get_around_words2(word)
        else:
            example_sentences = self._get_around_words2(word)
                
        # sentence not exist in wiki40b
        if len(example_sentences) == 0:
            return word        

        # count same sentence
        sentence_frequency_conter = {}
        for s in example_sentences:
            if s not in sentence_frequency_conter:
                sentence_frequency_conter[s] = 1
            else:
                sentence_frequency_conter[s] += 1

        s1 = sorted(sentence_frequency_conter.items(), key=lambda item: item[1], reverse=True)
        print(s1[:10])
        s = [s for s in s1 if len(s[0].split()) > 2]
        print(s[:10])
        
        most_frequent_sentence = max(sentence_frequency_conter, key=sentence_frequency_conter.get)
        count = sentence_frequency_conter[most_frequent_sentence]
        return most_frequent_sentence, count