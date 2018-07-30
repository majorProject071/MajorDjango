from __future__ import print_function

import nltk
import re
import inflect
from getdeathinjury import *
from location_tree import LocationInformation

from word2number import w2n
class DataExtractor:
    """ A class to extract the required data like location, month, deaths,etc.
        from the news story.
    """
    def __init__(self, pos_tagged_words, news_story):
        self.pos_tagged_words = pos_tagged_words
        self.splitted_sentences = nltk.sent_tokenize(news_story)

    def location_extractor(self):
        individual_sentences = self.splitted_sentences

        locations = []

        for sent in individual_sentences:
            words = nltk.word_tokenize(sent)
            if ("died" or "death" or "injured" or "injury" or "injuries" or "killed") in words:
                chunked_sentence = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent)))
                for i in chunked_sentence.subtrees(filter=lambda x: x.label() == 'GPE'):
                    for i in i.leaves():
                        locations.append(i[0])
        return_value = locations
        try:
            if (locations[0] == "New") or (locations[0] == "Old"):
                return_value = []
                return_value.append(locations[0] + " " + locations[1])
        except:
            pass
        return (return_value)


    def location(self):
        """ Gets the location from the news story.

            Inputs include the parts of speech tagged words.
            Output is the phrase containing the location of mishap.
        """
        ktm_location = LocationInformation().all_ktm_locations()
        bkt_location = LocationInformation().all_bkt_locations()
        ltp_location = LocationInformation().all_ltp_locations()
        outside_location = LocationInformation().all_locations()
        all_locations = ktm_location + outside_location + bkt_location + ltp_location

        locations = self.location_extractor()
        return_location = []
        max_ratio = 0
        max_location = []

        for glocation in locations:
            for location in all_locations:
                dist = nltk.edit_distance(glocation, location)
                ratio = (1 - (dist / len(glocation))) * 100
                max_ratio = max(max_ratio, ratio)
                if max_ratio >= 70:
                    max_location = location
                    if max_ratio == ratio:
                        if max_location in ktm_location:
                            return_location = max_location
                        elif max_location in ltp_location:
                            return_location = max_location
                        elif max_location in bkt_location:
                            return_location = max_location
                        elif max_location in outside_location:
                            return_location = max_location
        if return_location == "lalitpur":
            return_location = "patan"
        if return_location == "kathmandu":
            return_location = "ratna park"
        if return_location == "bhaktapur":
            return_location = "thimi"
        return (return_location)

    def day(self,complete_news):
        """ Gets the day of mishap.
        """
        day_regex = re.compile('\w+day')
        day = day_regex.findall(complete_news)[0]
        print("The day when the accident occured is: \n"+day)



    def vehicle(self):
        """ Gets the vehicle number from the news story.

            Inputs inclue the POS tagged words from the news.
            Output is the phrase containing the vehicle number.
        """

        vehicle_regex = "Vehicle: {<.*><CD><.*><CD>}"
        vehicle_parser = nltk.RegexpParser(vehicle_regex)
        vehicles = []
        for i in self.pos_tagged_words:
            vehicle = vehicle_parser.parse(i)
            for i in vehicle.subtrees(filter=lambda x:x.label() == 'Vehicle'):
                vehicle = ""
                for p in i.leaves():
                    # print(p[0],end=' ')
                    # print(p)
                    vehicle = vehicle + str(p[0]) + " "
                    # vehicle = vehicle[:-1]
                # print("\n")
                vehicles.append(vehicle[:-1])

        return(vehicles)

    def deaths(self,sentences):
        """ Gets the number of deaths from the news story.

            Inputs include the POS tagged words from the news story.
            Output includ the number of deaths mentioned in the news.
        """

        death_words = ["died","death","killed","life"]
        # death_regex = "Deaths: {<NNP>?<CD><NNS|NNP>?<VBD|VBN>?<VBD|VBN>}"
        death_regex = "Deaths: {<CD>}"
        has_deaths = [sent for sent in sentences if("died" or "death") in
                        nltk.word_tokenize(sent)]
        print(has_deaths)
        print(has_deaths[0].split("and"))
        # death_regex = r"""
        #     Deaths:
        #     """
        death_parser = nltk.RegexpParser(death_regex)

        for i in self.pos_tagged_words:
            deaths = death_parser.parse(i)
            for i in deaths.subtrees(filter = lambda x:x.label() == 'Deaths'):
                print(i.leaves())

    def injury(self,sentences):
        has_injuries = [sent for sent in sentences if("injured" or "injury"
                        or "injuries" or "injur") in nltk.word_tokenize(sent)]
        print(has_injuries)

        has_injuries_words = nltk.word_tokenize(has_injuries[0])

        injury_pos_tagged = nltk.pos_tag(has_injuries_words)
        print(injury_pos_tagged)

        injury_regex = r"""
                      INjury:
                        {<.*>+}          # Chunk everything
                        }<CC|IN|NNS|NN|DT|WRB>+{      # Chink sequences of VBD and IN
                  """
        injury_parser = nltk.RegexpParser(injury_regex)
        injury_occurence = injury_parser.parse(injury_pos_tagged)
        print(injury_occurence)

    def death_number(self):
        integer_regex = re.compile(r'\d{1,2}')
        new_sentences = []
        p = inflect.engine()
        # print(self.splitted_sentences)
        for sent in self.splitted_sentences:

            numbers = integer_regex.findall(sent)
            for i in numbers:
                sent = sent.replace('\\xa0', '')
                sent = sent.replace(i, p.number_to_words(i))
                sent = sent.replace('-', ' ')
                sent = sent.replace('\\r', '')
                sent = sent.replace('\r', '')

            new_sentences.append(sent)
        death = death_no(new_sentences)
        if death == "None":
            actualdeath = death
            deathNo = 0
        else:
            actualdeath = remove_date(death)
            deathNo = convertNum(death)
        return(deathNo, actualdeath)

    def injury_number(self):
        integer_regex = re.compile(r'\d{1,2}')
        new_sentences = []
        p = inflect.engine()
        for sent in self.splitted_sentences:

            numbers = integer_regex.findall(sent)
            for i in numbers:
                sent = sent.replace('\\xa0', '')
                sent = sent.replace(i, p.number_to_words(i))
                sent = sent.replace('-', ' ')
                sent = sent.replace('\\r', '')
                sent = sent.replace('\r', '')

            new_sentences.append(sent)
        print("new sentence")
        print(new_sentences)
        injury = injury_no(new_sentences)
        # print(injury)
        if injury == "None":
            actualinjury = "None"
            injuryNo = 0
        else:
            actualinjury = remove_date(injury)
            try:
                injuryNo = w2n.word_to_num(actualinjury)
            except:
                injuryNo = 1
        print("here")
        print (injuryNo, actualinjury)
        return(injuryNo, actualinjury)
