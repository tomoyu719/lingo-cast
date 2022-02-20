import re

import tensorflow_datasets as tfds
from utility.russian.word_morph import WordMorph


class MakeExampleSentenceFromWiki40b():
    def __init__(self, wiki40b_language_code) -> None:
        self.sentences = self._get_sentences_from_wiki40b(
            wiki40b_language_code)
        self.morph = WordMorph()

    def _get_sentences_from_wiki40b(self, wiki40b_language_code) -> list:
        ds = tfds.load('wiki40b/' + wiki40b_language_code, split='test')
        # ds = tfds.load('wiki40b/' + wiki40b_language_code, split='train')

        texts = []
        for wiki in ds.as_numpy_iterator():
            raw_text = wiki['text'].decode()
            text = self._remove_matetags(raw_text)
            texts.append(text)
        sentences = []
        for text in texts:
            sentences += re.split('[.\n]', text)
        # remove empty sentence
        sentences = list(filter(lambda x: x != '', sentences))
        return sentences

    def _remove_matetags(self, raw_text):
        SA = '_START_ARTICLE_'
        SS = '_START_SECTION_'
        SP = '_START_PARAGRAPH_'
        NL = '_NEWLINE_'
        META_TAGS = [SA, SS, SP, NL]
        for meta_tag in META_TAGS:
            raw_text = raw_text.replace(meta_tag, '')
        return raw_text

    def _get_around_words(self, words, exclude_pos_list) -> list:
        around_words = []
        for s in self.sentences:
            split = s.split()
            for word in words:
                if word in split:
                    index = split.index(word)
                    try:
                        prev = split[index - 1]
                    except IndexError:
                        prev = ''
                    try:
                        next = split[index + 1]
                    except IndexError:
                        next = ''
                    prev_pos = self.morph.get_word_pos(prev)
                    next_pos = self.morph.get_word_pos(next)

                    if prev_pos not in exclude_pos_list and next_pos not in exclude_pos_list:
                        s = prev + ' ' + word + ' ' + next
                        around_words.append(s)
                        # around_words.append((prev, next))

        return around_words

    def make_example_sentence(self, words, exclude_pos_list) -> str:
        around_words = self._get_around_words(words, exclude_pos_list)
        counter = {}
        for a in around_words:
            if a not in counter:
                counter[a] = 1
            else:
                counter[a] += 1

        # most_frequent_sentence = max(counter.items())[0]
        counter = sorted(counter.items(),
                         key=lambda x: x[1], reverse=True)
        most_frequent_sentence = counter[0][0]

        return most_frequent_sentence


# wiki40b_language_code = 'ru'
# m = MakeExampleSentenceFromWiki40b(wiki40b_language_code)

# word = 'дайте'
# # word = 'пятьдесят'

# morph = WordMorph()
# word_inflected_forms = morph.get_inflected_forms(word)

# exclude_pos_list = ['CONJ']
# s = m.make_example_sentence(word_inflected_forms, exclude_pos_list)
# print(s)
