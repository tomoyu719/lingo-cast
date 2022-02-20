from utility.get_words import get_words
from nltk.stem.snowball import RussianStemmer

file_path = 'fix_russian_words_duolingo_part5.txt'
words = get_words(file_path)

stemmer = RussianStemmer()
stemmed_words = {}
for word in words:
    stem = stemmer.stem(word)
    if stem not in stemmed_words:
        stemmed_words[stem] = word

# print(type(list(stemmed_words.values())))
# print(list(stemmed_words.values()))
# print(len(stemmed_words))

with open('stemmed_' + file_path, 'w') as f:
    f.write('\n'.join(list(stemmed_words.values())))
    
# print(set(stemmed_words))

# for s in set(stems):
#     print(s)