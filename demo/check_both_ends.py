import nltk

def check_both_ends(sentence):
    
    sentence = nltk.word_tokenize(sentence)
    if get_word_pos(sentence[0]) == 'CONJ':
        sentence = sentence[1:]
    if get_word_pos(sentence[-1]) == 'CONJ':
        sentence = sentence[:-1]
    return ' '.join(sentence)

def get_word_pos(word, language='rus'):
    token = [word]
    pos = nltk.tag.pos_tag(token, lang=language)
    return pos[0][1]
