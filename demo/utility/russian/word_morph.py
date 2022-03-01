# # import pymorphy2
# import json
# import nltk

# class WordMorph():

#     def __init__(self, language_code) -> None:
#         self.language_code = language_code
#         if self.is_supported_language(language_code):
#             self.morph
#         else:
#             raise Exception
#         self.stopwords 

#     # TODO error handling
#     def is_supported_language(self):
#         with open('wiki40b_language_codes.txt') as f:
#             wiki40b_language_codes = [s.strip() for s in f.readlines()]
    
#     # TODO error handling
#     def get_nltk_stopwords_languge_code(self):
#         with open('nltk_stopwords_supported_language_code.json') as f:
#             df = json.load(f)
#             return df[self.language_code]

#     def is_nltk_stopwords_supported_languge(self):
#         stopwords_language_code = self.get_nltk_stopwords_languge_code()
#         stopwords = nltk.corpus.stopwords.words(stopwords_language_code)
#         return stopwords

#     # part-of-speech：品詞
#     def get_word_pos(self, word):
#         # TODO 'ru'
#         if self.language_code == 'ru':
#             pos = self.russian_morph.parse(word)[0].tag.POS
#             return pos
#         else: 
#             raise ValueError

#     # get standard form. had -> have
#     def get_normalized_word(self, word):
#         if self.language_code == 'ru':
#             norm = self.russian_morph.parse(word)[0].normal_form
#             return norm
#         else: 
#             raise ValueError

#     # get all word forms. have -> [have,has,had,having,,,]
#     def get_other_word_forms(self, word):
#         lexemes = self.russian_morph.parse(word)[0].lexeme
#         return [l.word for l in lexemes]
#         # pos_origin = self.get_word_pos(word)
#         # words = []
#         # for l in lexemes:
#         #     word = l.word
#         #     if pos_origin == self.get_word_pos(word):
#         #         words.append(word)

#         # return words
    
#     # words内の単語のうち、正規化した形が重複すれば、取り除く
#     def remove_duplicate_word(self, words):
        
#         norm_words = []
#         no_duplicate_word = []
#         for w in words:
#             norm = self.get_normalized_word(w)
#             if norm not in norm_words:
#                 norm_words.append(norm)
#                 no_duplicate_word.append(w)
        
#         return no_duplicate_word

