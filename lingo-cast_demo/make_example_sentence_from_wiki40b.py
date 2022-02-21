import re

import tensorflow_datasets as tfds
from utility.russian.russian_word_morph import RussianWordMorph


#  TODO 日本語、中国語などは文をparseする


class MakeExampleSentenceFromWiki40b():
    def __init__(self, wiki40b_language_code) -> None:
        self.sentences = self._decode_wiki40b(
            wiki40b_language_code)
        self.morph = RussianWordMorph()

    # TODO 前後の単語を取得するだけならdecodeしなくても良さそう
    def _decode_wiki40b(self, wiki40b_language_code) -> list:
        # test : val : train = 5 : 5 : 90
        ds = tfds.load('wiki40b/' + wiki40b_language_code, split='test')
        # ds = tfds.load('wiki40b/' + wiki40b_language_code, split='train')

        texts = []
        for wiki in ds.as_numpy_iterator():
            raw_text = wiki['text'].decode()
            text = self._remove_matetags(raw_text)
            texts.append(text)
        sentences = []
        for text in texts:
            sentences += re.split('[.\n]', text)
        # removing empty sentence
        sentences = list(filter(lambda x: x != '', sentences))
        return sentences

    def _remove_matetags(self, raw_text):
        SA = '_START_ARTICLE_'
        SS = '_START_SECTION_'
        SP = '_START_PARAGRAPH_'
        NL = '_NEWLINE_'
        META_TAGS = [SA, SS, SP, NL]
        for meta_tag in META_TAGS:
            raw_text = raw_text.replace(meta_tag, '')
        return raw_text

    #Wiki40bから、wordの前後の単語を含んだ文を返す
    def _get_around_words(self, word, exclude_pos_list) -> list:
        short_sentences = []
        for s in self.sentences:
            split = s.split()
            if word in split:
                index = split.index(word)
                try:
                    prev = split[index - 1]
                except IndexError:
                    prev = ''
                try:
                    next = split[index + 1]
                except IndexError:
                    next = ''
                prev_pos = self.morph.get_word_pos(prev)
                next_pos = self.morph.get_word_pos(next)

                if prev_pos not in exclude_pos_list and next_pos not in exclude_pos_list:
                    # TODO do lower case
                    s = prev + ' ' + word + ' ' + next
                    
                    short_sentences.append(s)

        return short_sentences


    def make_example_sentence(self, word, exclude_pos_list) -> str:
        all_word_forms = self.morph.get_inflected_forms(word)
        short_sentences_contain_word = []
        for word in all_word_forms:
            short_sentences_contain_word += self._get_around_words(word, exclude_pos_list)
            
        sentence_frequency_conter = {}
        for s in short_sentences_contain_word:
            if s not in sentence_frequency_conter:
                sentence_frequency_conter[s] = 1
            else:
                sentence_frequency_conter[s] += 1

        # descending order
        sentence_frequency_conter = sorted(sentence_frequency_conter.items(),
                         key=lambda x: x[1], reverse=True)

        # TODO error catch 
        most_frequent_sentence = sentence_frequency_conter[0][0]

        return most_frequent_sentence

