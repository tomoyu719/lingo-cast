from mytranslater import MyTransrator
from utility.russian.russian_word_morph import RussianWordMorph


word = 'смог'
m = RussianWordMorph()
a = m.get_word_pos(word)
print(a)
word = 'вовремя'
a = m.get_word_pos(word)
print(a)

# m = MyTransrator('ru', 'en')
# dictionaries = [('смог вовремя', 6), ('раз вовремя', 4), ('успели вовремя', 3), ('его вовремя', 3), ('вовремя —', 3), ('вовремя эвакуироваться', 2), ('лишь вовремя', 2), ('вовремя подоспевшие', 2), ('лишь вовремя подоспевшие', 2), ('были вовремя', 2)]
# for d in dictionaries:
#     word = d[0]
#     print(word, m.translate(word), d[1])