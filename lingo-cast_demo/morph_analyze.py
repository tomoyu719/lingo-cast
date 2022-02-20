# from utility.get_words import get_words

# import pymorphy2
# morph = pymorphy2.MorphAnalyzer()

# def get_part_of_speech(word):
#     return morph.parse(word)[0].tag.POS

# file_dir = '/Users/kitanotoshiyuki/lingo-cast/words/russian/duolingo/no_duplicate_russian_words_duolingo/'
# import os
# file_names = os.listdir(file_dir)
# file_names.sort()
# count_pos = {}
# for file_name in file_names:
#     file_path = file_dir + file_name
#     words = get_words(file_path)
#     for word in words:
#         pos = get_part_of_speech(word)
#         if pos not in count_pos:
#             count_pos[pos] = 1
#         else:
#             count_pos[pos] += 1

# print(count_pos)
