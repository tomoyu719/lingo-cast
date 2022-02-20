# from utility.get_words import get_words

import pymorphy2


class WordMorph():
    morph = pymorphy2.MorphAnalyzer()

    # get part-of-speech
    def get_word_pos(self, word):
        pos = self.morph.parse(word)[0].tag.POS
        return pos

    # get standard form
    def get_normalized_word(self, word):
        norm = self.morph.parse(word)[0].normal_form
        return

    # get all forms
    def get_inflected_forms(self, word):
        lexemes = self._get_same_pos_lexemes(word)
        words = []
        for lexeme in lexemes:
            words.append(lexeme.word)
        return words

    def _get_same_pos_lexemes(self, word):
        pos = self.get_word_pos(word)
        lexemes = self.morph.parse(word)[0].lexeme
        lexemes = [l for l in lexemes if l.tag.POS == pos]
        return lexemes
