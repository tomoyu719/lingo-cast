from utility.get_words import get_words
from nltk.stem.snowball import SnowballStemmer


stemmer = SnowballStemmer("russian")


def stemming_word(word):
    return stemmer.stem(word)
