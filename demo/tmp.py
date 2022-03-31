import json

p = '/Users/kitanotoshiyuki/lingo-cast/demo/outputs/ukrainian/9_Hobby.json'
with open(p) as f:
    df = json.load(f)

for d in df:
    
    s = d['example']
    w = d['word']
    print(w,'.')
    print(s, '.')
