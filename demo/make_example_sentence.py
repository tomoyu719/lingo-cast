import random

from ngram_language_model import NgramLanguageModel
from pos import Pos
from sentence_db import SentenceDb
from sentence_util import SentenceUtil

# MAX_PROCESS_SENTENCE_NUM = 200
MAX_PROCESS_SENTENCE_NUM = 500

class MakeExampleSentence():
    def __init__(self, language_code, max_sentence_length, min_sentence_length, ngram_num) -> None:
        self.language_code = language_code
        self.ngram_num = ngram_num
        self.max_sentence_length = max_sentence_length 
        self.min_sentence_length = min_sentence_length
        self.sentence_db = SentenceDb(language_code)
        self.pos = Pos(language_code)
        self.sentence_util = SentenceUtil(language_code)
    
    def make_example_sentence(self, source_word):

        if self.sentence_util.is_idiom(source_word):
            sentences_contain_word = self.sentence_db.fetch_sentences_contain_many_words(source_word.split())
        else:
            sentences_contain_word = self.sentence_db.fetch_sentences_contain_word(source_word)
        sentences_contain_word = [s.lower() for s in sentences_contain_word]
        sentences_contain_word = [self.sentence_util.replace_num(s) for s in sentences_contain_word]
        # sentences_contain_word = sentences_contain_word[:MAX_PROCESS_SENTENCE_NUM]
        sentences_contain_word = random.sample(sentences_contain_word, min(len(sentences_contain_word), MAX_PROCESS_SENTENCE_NUM))
        sentences_tokenized = [self.sentence_util.tokenize_sentence(s) for s in sentences_contain_word]
        sentences_padded = [self.sentence_util.padding_sentence(s, self.ngram_num) for s in sentences_tokenized]
        
        model = NgramLanguageModel(sentences_padded, self.ngram_num, self.language_code)
        example_sentence, probs = model.create_example_sentence(source_word, self.max_sentence_length, self.min_sentence_length)
        example_sentence = self.remove_paddings(example_sentence)
        example_sentence = self.check_sentence_both_sides(example_sentence, source_word)
        return example_sentence, probs
    
    def count_word_contain_sentence_num(self, source_word):
        if self.sentence_util.is_idiom(source_word):
            #TODO fix split
            return self.sentence_db.fetch_sentence_num_contain_many_words(source_word.split())
        else:
            return self.sentence_db.fetch_sentence_num_contain_word(source_word)

    def remove_paddings(self, sentence):
        return sentence.replace('<s> ','').replace('</s>','').replace('.END','')

    def check_sentence_both_sides(self, sentence, source_word):
        split_sentence = sentence.split()
        words = split_sentence
        
        is_word_idiom = self.sentence_util.is_idiom(source_word)

        for w in split_sentence:
            if w == source_word:
                break
            if is_word_idiom and w == source_word.split()[0]:
                break
            p = self.pos.get_word_pos(w)
            if p in ['CONJ']:
                words.remove(w)
            else:
                break
        for w in split_sentence[::-1]:
            if w == source_word:
                break
            if is_word_idiom and w == source_word.split()[-1]:
                break
            p = self.pos.get_word_pos(w)
            if p in ['CONJ', 'PREP']:
                words.remove(w)
            else:
                break
        return ' '.join(words)