import string
import nltk
from nltk.lm        import Vocabulary
from nltk.lm.models import MLE
from nltk.util      import ngrams
from nltk.lm.preprocessing import pad_both_ends

EXCLUDE_STR = string.punctuation + '<s></s>«»、「」（）『』・'

# TODO consider the appropriate number
MAX_PROCESS_SENTENCE_NUM = 1000

class NgramLanguageModel():
    def __init__(self, sentences) -> None:
        # faster and enough 
        self.sentences = sentences[:MAX_PROCESS_SENTENCE_NUM]


        sentences_padded = self.padding_sentences(self.sentences)
        monograms_forward = self.get_ngram(N=2, sentences_padded=sentences_padded)
        bigrams_forward = self.get_ngram(N=3, sentences_padded=sentences_padded)
        trigrams_forward = self.get_ngram(N=4, sentences_padded=sentences_padded)
        monograms_backward = self.get_ngram(N=2, sentences_padded=sentences_padded, backward=True)
        bigrams_backward = self.get_ngram(N=3, sentences_padded=sentences_padded, backward=True)
        trigrams_backward = self.get_ngram(N=4, sentences_padded=sentences_padded, backward=True)

        vocabulary = self.get_vocab(sentences_padded)

        self.monogram_forward_model = self.create_language_model(monograms_forward, N=2, vocabulary=vocabulary)
        self.bigram_forward_model = self.create_language_model(bigrams_forward, N=3,vocabulary=vocabulary)
        self.trigram_forward_model = self.create_language_model(trigrams_forward, N=4,vocabulary=vocabulary)
        self.monogram_backward_model = self.create_language_model(monograms_backward, N=2,vocabulary=vocabulary)
        self.bigram_backward_model = self.create_language_model(bigrams_backward, N=3, vocabulary=vocabulary)
        self.trigram_backward_model = self.create_language_model(trigrams_backward, N=4, vocabulary=vocabulary)
        
        
    def create_language_model(self, ngrams, N, vocabulary): # N-gram言語モデルの作成
        ngram_language_model = MLE(order=N, vocabulary=vocabulary)
        ngram_language_model.fit(ngrams, vocabulary)
        return ngram_language_model
    

    def padding_sentences(self, sentences):
        sents = []
        for sent in sentences:
            sent = nltk.word_tokenize(sent)
            # pad_both_ends:
            # ['The' 'sentence', 'of', 'words']
            # ['<s>', '<s>', 'The', 'sentence', 'of', 'words', '</s>', '</s>']
            sents.append(list(pad_both_ends([word for word in sent], n=3)))
        return sents

    def get_vocab(self,sentences_padded):
        vocab = Vocabulary([word for sent in sentences_padded for word in sent], unk_cutoff=1)
        return vocab
        
    def get_ngram(self,N, sentences_padded, backward=False):
        if backward:
            word_ngrams = [ngrams(sent[::-1], N) for sent in sentences_padded]
        else:
            word_ngrams = [ngrams(sent, N) for sent in sentences_padded]
        return word_ngrams
    
    # Maximum Likelihood Estimator
    def get_mle_word(self,model, context):
        prob_list = []
        ngram_words = model.context_counts(model.vocab.lookup(context))
        if len(ngram_words) == 0:
            return '', 0
        for word in ngram_words:
            prob_list.append((word, model.score(word, context)))
        prob_list.sort(key=lambda x: x[1], reverse=True) # 出現確率順
        word = prob_list[0][0]
        score = prob_list[0][1]

        return word, score

    def is_word_in_exclude_str(self, word):
        return word in EXCLUDE_STR

    def check_word_and_score(self, word, score):
        if self.is_word_in_exclude_str(word):
            return (word, 0)
        else: 
            return (word, score)

    #TODO clean
    def create_example_sentence(self,word, min_length=4, max_length=6):
        # word not be abundunt in dataset
        if len(self.sentences) < 10:
            return word
        words = [word]
        example_sentence = ' '.join(words)
        score_sum = 0
        score_mean = 0
        while(len(words)) < max_length:
            
            prev_context = tuple(words[:3][::-1])
            trigram_prev_word, trigram_prev_score = self.get_mle_word(self.trigram_backward_model, prev_context)
            
            prev_context = tuple(words[:2][::-1])
            bigram_prev_word, bigram_prev_score = self.get_mle_word(self.bigram_backward_model, prev_context)
            
            prev_context = tuple(words[:1])
            monogram_prev_word, monogram_prev_score = self.get_mle_word(self.monogram_backward_model, prev_context)

            next_context = tuple(words[-3:])
            trigram_next_word, trigram_next_score = self.get_mle_word(self.trigram_forward_model, next_context)

            next_context = tuple(words[-2:])
            bigram_next_word, bigram_next_score = self.get_mle_word(self.bigram_forward_model, next_context)

            next_context = tuple(words[-1:])
            monogram_next_word, monogram_next_score = self.get_mle_word(self.monogram_forward_model, next_context)

            prevs = [(trigram_prev_word, trigram_prev_score), (bigram_prev_word, bigram_prev_score), (monogram_prev_word, monogram_prev_score)]
            prevs = [self.check_word_and_score(w,s) for w,s in prevs]
            prevs.sort(key=lambda x: x[1], reverse=True)
            prev_word, prev_score = prevs[0]
            nexts = [(trigram_next_word, trigram_next_score), (bigram_next_word, bigram_next_score), (monogram_next_word, monogram_next_score)]
            nexts = [self.check_word_and_score(w,s) for w,s in nexts]
            nexts.sort(key=lambda x: x[1], reverse=True)
            next_word, next_score = nexts[0]
            if prev_score == 0 and next_score == 0:
                return example_sentence
            elif prev_score > next_score:
                score_sum += prev_score
                score_mean_old = score_mean
                score_mean = score_sum / (len(words))
                if score_mean_old > score_mean and len(words) >= min_length:
                    return example_sentence
                else:
                    words = [prev_word] + words
            else:
                score_sum += next_score
                score_mean_old = score_mean
                score_mean = score_sum / (len(words))
                if score_mean_old > score_mean and len(words) >= min_length:
                    return example_sentence
                else:
                    words = words + [next_word]
            example_sentence = ' '.join(words)

            
        return example_sentence
            



