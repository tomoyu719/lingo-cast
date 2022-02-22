from utility.russian.russian_word_morph import RussianWordMorph

morph = RussianWordMorph()
m = morph.get_word_pos

word = 'к'
print(word, m(word))
word = 'в'
print(word, m(word))
word = 'не'
print(word, m(word))
word = 'от'
print(word, m(word))
