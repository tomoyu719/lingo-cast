import pymorphy2
import nltk

# TODO implement other languages
class Pos():
    def __init__(self, language_code) -> None:
        self.language_code = language_code
        if self.language_code == 'uk':
            self.morph = pymorphy2.MorphAnalyzer(lang='uk')
        elif self.language_code == 'ru':
            self.morph = pymorphy2.MorphAnalyzer(lang='ru')
        # elif self.language_code == 'en':

        
    def get_word_pos(self, word) -> str:
        if self.language_code == 'uk':
            pos =  self.morph.parse(word)[0].tag.POS
        elif self.language_code == 'ru':
            pos =  self.morph.parse(word)[0].tag.POS
        elif self.language_code == 'en':
            pos = nltk.pos_tag([word])[0][1]
        else:
            pos = None
        return pos
