# import os

# from utility.get_words import get_words
# from utility.russian.word_morph import normalize_word


# file_dir = '/Users/kitanotoshiyuki/lingo-cast/words/russian/duolingo/raw_russian_words/'
# file_names = os.listdir(file_dir)
# file_names.sort()

# out_dir = '/Users/kitanotoshiyuki/lingo-cast/words/russian/duolingo/no_duplicate_russian_words/'

# processed_words = []
# for file_name in file_names:
#     file_path = file_dir + file_name
#     no_dup_words = []
#     words = get_words(file_path)

#     for word in words:
#         word_normalize = normalize_word(word)
#         if word_normalize not in processed_words:
#             processed_words.append(word_normalize)
#             no_dup_words.append(word_normalize)

#     out_path = out_dir + file_name

#     with open(out_path, 'w') as f:
#         f.write('\n'.join(no_dup_words))
