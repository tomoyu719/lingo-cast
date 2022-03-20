from decode_wiki40b import DecodeWiki40b
from is_idiom import is_idiom
from ngram_language_model import NgramLanguageModel
from pos import Pos


class MakeExampleSentence():
    def __init__(self, wiki40b_language_code, max_sentence_length, min_sentence_length, ngram_num) -> None:
        self.ngram_num = ngram_num
        self.max_sentence_length = max_sentence_length 
        self.min_sentence_length = min_sentence_length
        self.wiki40b = DecodeWiki40b(wiki40b_language_code, ngram_num)
        self.pos = Pos(wiki40b_language_code)
    
    def make_example_sentence(self, source_word):
        if is_idiom(source_word):
            # tokenized_sentences = self.wiki40b.get_tokenized_sentences_contain_idiom(source_word)
            padded_sentences = self.wiki40b.get_sentences_contain_words(source_word.split())
        else:
            # tokenized_sentences = self.wiki40b.get_tokenized_sentences_contain_word(source_word)
            padded_sentences = self.wiki40b.get_sentences_contain_word(source_word)
        # something like confidence
        self.word_contain_num = len(padded_sentences)
        model = NgramLanguageModel(padded_sentences, self.ngram_num)
        # example_sentence = model.create_example_sentence(source_word, self.max_sentence_length, self.min_sentence_length)
        # example_sentence = self.check_sentence_both_sides(example_sentence, source_word)
        # return example_sentence
        # example_sentences, words_with_prob = model.create_example_sentence2(source_word, self.max_sentence_length, self.min_sentence_length)
        # return example_sentences, words_with_prob
        # example_sentences = model.create_example_sentence(source_word, self.max_sentence_length, self.min_sentence_length)
        # return example_sentences
        example_sentences = model.create_example_sentence(source_word, self.max_sentence_length, self.min_sentence_length)
        # example_sentences = [self.remove_sp_chars(s) for s in example_sentences]
        # example_sentences = [self.check_sentence_both_sides(s) for s in example_sentences]
        # poses = [self.pos.get_word_pos(w) for w in example_sentence.split()] 
        example_sentence = self.remove_sp_chars(example_sentences[-1])
        example_sentence = self.check_sentence_both_sides(example_sentence, source_word)
        
        return example_sentence
    
    def remove_sp_chars(self, sentence):
        return sentence.replace('<s> ','').replace('</s>','').replace('.END','')

    def check_sentence_both_sides(self, sentence, source_word):
        split_sentence = sentence.split()
        words = split_sentence
        is_word_idiom = is_idiom(source_word)

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