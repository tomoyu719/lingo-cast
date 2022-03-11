from decode_wiki40b import DecodeWiki40b
from is_idiom import is_idiom
from ngram_language_model import NgramLanguageModel


class MakeExampleSentence():
    def __init__(self, wiki40b_language_code) -> None:
        self.wiki40b = DecodeWiki40b(wiki40b_language_code)

    def make_example_sentence(self, word, max_sentence_length):
        if is_idiom(word):
            tokenized_sentences = self.wiki40b.get_tokenized_sentences_contain_idiom(word)
        else:
            tokenized_sentences = self.wiki40b.get_tokenized_sentences_contain_word(word)
        # for debug
        self.word_contain_num = len(tokenized_sentences)
        model = NgramLanguageModel(tokenized_sentences)
        example_sentence = model.create_example_sentence(word, max_sentence_length)
        return example_sentence

        