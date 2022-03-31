'''
example textfile form 
words/ukrainian/duolingo_raw.txt
'''
import csv

source_file = '/Users/kitanotoshiyuki/lingo-cast/demo/words/pl/pl_duolingo_raw.txt'
out_dir = '/Users/kitanotoshiyuki/lingo-cast/demo/words/pl/duolingo/'
initial_name = 'Basics 1 [test]'

with open(source_file) as f:
    s = f.read()
is_after_Words = False
name = initial_name.replace(' [test]','').replace(' ', '_')
count = 1
for text in s.split('\n'):
    if 'Words: ' in text:
        is_after_Words = True
        words = text.replace('Words: ', '')
    elif is_after_Words:
        is_after_Words = False
        name = str(count) + '_' + name
        count += 1 
        with open(out_dir + name + '.csv', 'w') as f:
            f.write(words)
        name = text.replace(' [test]','').replace(' ', '_')
        