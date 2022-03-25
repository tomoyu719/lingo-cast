import random
import string
import json


from nltk.lm        import Vocabulary
from nltk.lm.models import MLE
from nltk.util      import ngrams
from nltk.lm.preprocessing import pad_sequence
import nltk
from sentence_util import SentenceUtil

class NgramLanguageModel():
    
    def __init__(self, padded_sentences, ngram_num, language_code) -> None:        
        self.ngram_num = ngram_num
        self.padded_sentences = padded_sentences
        self.vocabulary = self.get_vocab(padded_sentences)
        self.forward_models = [self.create_language_model(n) for n in range(2, ngram_num + 1)]
        self.backward_models = [self.create_language_model(n, backward=True) for n in range(2, ngram_num + 1)]
        self.sentence_util = SentenceUtil(language_code)
    
    def select_model(self, seed_words):
        words_num = len(seed_words)
        models_num = len(self.backward_models)
        if words_num <= models_num:
            prev_model = self.backward_models[words_num - 1]
            next_model = self.forward_models[words_num - 1]
        else:
            prev_model = self.backward_models[-1]
            next_model = self.forward_models[-1]
        return prev_model, next_model
    
    def create_language_model(self, N, backward=False):
        ngrams = self.get_ngram(N, self.padded_sentences, backward)
        ngram_language_model = MLE(order=N, vocabulary=self.vocabulary)
        ngram_language_model.fit(ngrams, self.vocabulary)
        return ngram_language_model

    def get_vocab(self, sentences_padded):
        vocab = Vocabulary([word for sent in sentences_padded for word in sent])
        return vocab
        
    def get_ngram(self, N, sentences_padded, backward=False):
        if backward:
            word_ngrams = [ngrams(sent[::-1], N) for sent in sentences_padded]
        else:
            word_ngrams = [ngrams(sent, N) for sent in sentences_padded]
        return word_ngrams
    
    # Maximum Likelihood Estimator
    # P(new_word|context)
    def get_mle_word(self, model, context, exclude_stopwords=False):
        ngram_words = model.context_counts(model.vocab.lookup(context))
        # model doesnt have context
        if len(ngram_words) == 0:
            return '', 0
        word_prob_list = []
        for word in ngram_words:
            word_prob_list.append((word, model.score(word, context)))
        word_prob_list.sort(key=lambda x: x[1], reverse=True) # 出現確率順

        for word, prob in word_prob_list:
            if word not in ',.\'\'«»()!':
                return word, prob
            # if word not in  ',.and\'\'':
            # if exclude_stopwords:
            # else:
            #     return word, prob
        return '', 0
    
    def get_context(self, words):
        # if ngram_num == 3
        # He eats the apple => (the, eats, he)
        prev_context = tuple(words[:self.ngram_num - 1][::-1])
        # He eats the apple => (eats, the, apple)
        next_context = tuple(words[-self.ngram_num + 1:])
        return prev_context, next_context
    
    def create_example_sentence(self, word, max_sentence_length, min_sentence_length):
        if self.sentence_util.is_idiom(word):
            words = word.split()
        else:
            words = [word]
        
        example_sentences = []

        while(len(words)) < max_sentence_length:
            prev_model, next_model = self.select_model(words)
            prev_context, next_context = self.get_context(words)

            prev_word, prev_word_prob = self.get_mle_word(prev_model, prev_context)
            next_word, next_word_prob = self.get_mle_word(next_model, next_context)
            
            if prev_word_prob == 0 and next_word_prob == 0: 
                words = words + ['.END']
                example_sentences.append(' '.join(words))  
                return example_sentences
            if prev_word_prob > next_word_prob:
                if prev_word == '<s>':
                    max_sentence_length += 1
                    min_sentence_length += 1
                words = [prev_word] + words
            else:
                if next_word == '</s>':
                    max_sentence_length += 1
                    min_sentence_length += 1
                words = words + [next_word]    
            if len(words) >= min_sentence_length:
                example_sentences.append(' '.join(words))  

        return example_sentences
