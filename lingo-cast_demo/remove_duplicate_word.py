from utility.russian.word_morph import WordMorph

# 正規化した単語が重複すれば、取り除く
def remove_duplicate_word(words):
    morph = WordMorph()

    norm_words = []
    no_duplicate_word = []

    for w in words:
        norm = morph.get_normalized_word(w)
        if norm not in norm_words:
            norm_words.append(norm)
            no_duplicate_word.append(w)
    
    return no_duplicate_word

