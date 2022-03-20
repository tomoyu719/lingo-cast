'''
example textfile form 
words/ukrainian/duolingo_raw.txt
'''
import csv


source_file = '/Users/kitanotoshiyuki/lingo-cast/demo/words/japanese/duolingo_raw.txt'
out_dir = '/Users/kitanotoshiyuki/lingo-cast/demo/words/japanese/duolingo/'
initial_name = 'Hiragana 1 [test]'

with open(source_file) as f:
    s = f.read()
is_empty_line = False
is_after_words = False
name = initial_name
words_with_title = ''
for text in s.split('\n'):
    if text == '':
        is_after_words = False
        name = words_with_title.split(',')[-2].replace(' [test]', '').replace(' ', '').replace('.','').replace('-', '_')
        words = []
        print(words_with_title)
        print()
        raise ValueError
        words = words_with_title.split('\n')
        # with open(out_dir + name + '.csv', 'w') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(words)

    if 'Words:' in text:
        is_after_words = True
    elif is_after_words:
        words_with_title += text + ','
        
        # is_after_words = False