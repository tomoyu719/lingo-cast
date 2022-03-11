import json

from japanese import JapaneseUtils 
file_path = 'outputs/japanese/duolingo/Ability.json'
with open(file_path) as f:
    df = json.load(f)

jp_utils = JapaneseUtils()

for d in df:
    word = d['word']
    example_sentence = d['example']
    example_sentence = example_sentence.replace(' ', '') + '.'
    print(example_sentence)
    # pos = jp_utils.get_pos_tmp(example_sentence)
    
    # print(example_sentence, word)
    # print(pos)
    

