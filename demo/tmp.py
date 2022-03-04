import nltk

def get_word_pos(word):
    token = [word]
    pos = nltk.tag.pos_tag(token, lang='rus')
    return pos[0][1]

word = 'и'
pos = get_word_pos(word)
print(pos)
