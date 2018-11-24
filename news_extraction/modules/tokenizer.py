#!/usr/bin/python
# -*- coding: latin-1 -*-
from __future__ import print_function

import re
import nltk
import datetime
from time import strptime



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
###################  GETTING THE DATE FROM THE NEWS ##################
    def get_date(self,complete_news):
        date_regex = r'(\d+-\d+-\d+)'
        contains_date = complete_news

        # #
        if contains_date[0] == '\n':
            contains_date = contains_date[1:]
        matches = re.search(date_regex, contains_date)
        # print (matches.group(1).strip())
        date = datetime.datetime.strptime(matches.group(1).strip(), "%Y-%m-%d")
        month,year, date = date.month, date.year, matches.group(1).strip()

        return(month,year,date)
####################### MODULE FOR FINDING DATE FINISHED HERE #############