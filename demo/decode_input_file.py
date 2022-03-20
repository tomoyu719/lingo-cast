import os
import re

from japanese import JapaneseUtils

def decode_input_file(file_path, language_code) -> list:
    with open(file_path) as f:
        s = f.read()
        # s = re.sub('\s','',s)
        words = s.split(',')
        
        #remove around space
        words = [' '.join(w.split()) for w in words]

        # remove empty
        words = [w for w in words if w != '']
        words = [w.lower() for w in words]

        if language_code == 'ja':
            ja_utils = JapaneseUtils()
            words = [ja_utils.spacing_sentence(w) for w in words]

        return words


# p = '/Users/kitanotoshiyuki/lingo-cast/demo/words/ukrainian/duolingo/12_Food_2_-_Food_2._Accusative_Case.csv'
# x = decode_input_file(p, 'uk')
# print(x)

# p = '/Users/kitanotoshiyuki/lingo-cast/demo/words/ukrainian/duolingo/'
# ns = os.listdir(p)
# ns.sort()
# for n in ns:
#     print(n)
#     x = decode_input_file(p+n,'uk')
#     print(x)
#     print('='*10)
