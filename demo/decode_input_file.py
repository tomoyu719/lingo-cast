import re

from japanese import JapaneseUtils

def decode_input_file(file_path, language_code) -> list:
    with open(file_path) as f:
        s = f.read()
        s = re.sub('\s','',s)
        words = s.split(',')        
        # remove empty
        words = [w for w in words if w != '']
        words = [w.lower() for w in words]

        if language_code == 'ja':
            ja_utils = JapaneseUtils()
            words = [ja_utils.spacing_sentence(w) for w in words]

        return words
