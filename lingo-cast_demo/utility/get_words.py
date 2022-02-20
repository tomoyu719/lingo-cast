# TODO rename
def get_words(file_path):
    with open(file_path) as f:
        words = [s.strip() for s in f.readlines()]
        
    return words
    