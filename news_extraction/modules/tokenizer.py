from __future__ import print_function

import nltk

class Tokenize:
    """
    Splits news story into sentences and words.
    """
    def __init__(self,paragraph):
        self.paragraph = paragraph

    def split_story(self):
        """ Splits the news story into list of sentences.

            Input is the news story.
            Output is the list of individual sentences.
        """
        sentences = nltk.sent_tokenize(self.paragraph)
        return sentences

    def split_words(self):
        """ Splits individual sentences into words.

            Inputs are the list of sentences.
            Output is the list of tokenized sentences.
        """
        sentences = self.split_story()
        words = [nltk.word_tokenize(sent) for sent in sentences]
        return words
