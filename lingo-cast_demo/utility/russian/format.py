import os



file_dir = '/Users/kitanotoshiyuki/lingo-cast/words/russian/duolingo/raw_russian_words/'
file_names = os.listdir(file_dir)
file_names.sort()

out_dir = '/Users/kitanotoshiyuki/lingo-cast/words/russian/duolingo/raw_russian_words/'

for file_name in file_names:
    file_path = file_dir + file_name
    
    with open(file_path) as f:
        txt = f.read()
        txt = txt.replace(',', ' ')
    
    words = txt.split()

    out_name = file_name.split('_')[-1]
    with open(out_dir + out_name, 'w') as f:
        f.write('\n'.join(words))
    