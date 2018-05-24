from __future__ import print_function

import nltk
class Tagger:
    """ Tags the tokens in a sentence.
    """
    def __init__(self,sentences):
        self.sentences = sentences

    def tag(self):
        """ Tags the tokens.

            Inputs are the tokenized words.
            Output is the words along with their respective POS it tags
        """
        tags = [nltk.pos_tag(sent) for sent in self.sentences]
        return tags
