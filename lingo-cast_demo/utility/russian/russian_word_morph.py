# from utility.get_words import get_words

import pymorphy2


class RussianWordMorph():
    morph = pymorphy2.MorphAnalyzer()

    # part-of-speech：品詞
    def get_word_pos(self, word):
        pos = self.morph.parse(word)[0].tag.POS
        return pos

    # get standard form. had -> have
    def get_normalized_word(self, word):
        norm = self.morph.parse(word)[0].normal_form
        return norm

    # get all word forms. have -> [have,has,had,having,,,]
    def get_inflected_forms(self, word):
        lexemes = self.morph.parse(word)[0].lexeme
        words = [l.word for l in lexemes]
        return words
