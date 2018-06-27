from __future__ import print_function

import re
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
###################  GETTING THE DATE FROM THE NEWS ##################
    def get_date(self,complete_news):
        splited_sentences = self.split_story()
        date_regex = r"([a-zA-Z]+)\s(\d{1,2})\W{1,2}(\d{4})(\-)"
        contains_date = splited_sentences[0]
        dates = re.findall(r'[A-Z]\w+\s\d+[,.]\s\d+', complete_news)
        for date in dates:
            newdates = date

        if contains_date[0] == '\n':
            contains_date = contains_date[1:]
        matches = re.search(date_regex, contains_date)

        month,day,year = matches.group(1).strip(),matches.group(2).strip(),matches.group(3).strip()


        for match in re.finditer(date_regex, contains_date):
            start,end = match.span()


        self.paragraph = self.paragraph[end:]

        return(newdates,day,month,year,self.paragraph)
####################### MODULE FOR FINDING DATE FINISHED HERE #############