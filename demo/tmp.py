import json

p = '/Users/kitanotoshiyuki/lingo-cast/demo/outputs/ukrainian/12_Food_2_-_Food_2.json'
with open(p) as f:
    df = json.load(f)

for d in df:
    wn = d['word_contain_sentence_num']
    w = d['word']
    print(w)
    print(wn)
    s = d['example']
    print(s, '.')
    for w in s.split():
        print(w,end='. ')
    print()
    print()

