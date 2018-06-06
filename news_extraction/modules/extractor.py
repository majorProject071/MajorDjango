from __future__ import print_function
from __future__ import division
import nltk
import re
import os
import sys

from tagger import Tagger
from tokenizer import Tokenize
from getdeathinjury import *

class DataExtractor:
    """ A class to extract the required data like location, month, deaths,etc.
        from the news story.
    """
    def __init__(self,pos_tagged_words,news_story):
        self.pos_tagged_words = pos_tagged_words
        self.splitted_sentences = nltk.sent_tokenize(news_story)


    def location(self):
        """ Gets the location from the news story.

            Inputs include the parts of speech tagged words.
            Output is the phrase containing the location of mishap.
        """
        # individual_sentences = nltk.sent_tokenize(news_story)
        individual_sentences = self.splitted_sentences

        locations = []
        # main_location = ['baneshwor','koteshwor','lagankhel','Sinamangal']
        for sent in individual_sentences:
            words = nltk.word_tokenize(sent)
            if("died" or "death" or "injured" or "injury" or "injuries") in words:
                # print(sent)
                chunked_sentence = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent)))
                # print(chunked_sentence)
                for i in chunked_sentence.subtrees(filter = lambda x:x.label() == 'GPE'):
                    for i in i.leaves():
                        locations.append(i[0])
        # for location in main_location:
        #     for glocation in locations:
        #         dist = nltk.edit_distance(glocation, location)
        #         ratio = (1-(dist/len(glocation)))*100
        #         if ratio >= 80:
        #             words = [w.replace(glocation, location) for w in locations]
        #             locations = words
        return(locations)


    def day(self,complete_news):
        """ Gets the day of mishap.
        """
        day_regex = re.compile('\w+day')
        day = day_regex.findall(complete_news)[0]
        # print("The day when the accident occured is: \n"+day)
        return day


    def vehicle(self):
        """ Gets the vehicle number from the news story.
            Inputs include the POS tagged words from the news.
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
                    vehicle = vehicle + str(p[0]) + " "
                    # vehicle = vehicle[:-1]
                    # print("\n")
                vehicles.append(vehicle[:-1])
        return (vehicles)


    def vehicle_involved(self):
        vehicle_regex = "Vehicle: {<.*><CD><.*><CD>}"
        vehicle_parser = nltk.RegexpParser(vehicle_regex)

        vehicle_code = []
        for i in self.pos_tagged_words:
            vehicle = vehicle_parser.parse(i)
            for i in vehicle.subtrees(filter=lambda x: x.label() == 'Vehicle'):
                vehicle_code.append(i.leaves()[2][0])
        # print(vehicle_code)

        vehicle = []
        for vcode in vehicle_code:
            if vcode == 'Kha':
                vehicle.append('Bus')
            elif vcode == 'Pa':
                vehicle.append('Bike')
            elif vcode == 'Ba':
                vehicle.append('Bike')
            elif vcode == 'Cha':
                vehicle.append('Car')
            elif vcode == 'Ya':
                vehicle.append('Bus')
            elif vcode == 'CD' or 'C D':
                vehicle.append('Car')

        return (vehicle)


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
        #print(has_deaths)
        #print(has_deaths[0].split("and"))
        # death_regex = r"""
        #     Deaths:
        #     """
        death_parser = nltk.RegexpParser(death_regex)

        for i in self.pos_tagged_words:
            deaths = death_parser.parse(i)
            for i in deaths.subtrees(filter = lambda x:x.label() == 'Deaths'):
                # print(i.leaves())
                pass

    def injury(self,sentences):
        has_injuries = [sent for sent in sentences if("injured" or "injury"
                        or "injuries" or "injur") in nltk.word_tokenize(sent)]
        #print(has_injuries)

        has_injuries_words = nltk.word_tokenize(has_injuries[0])

        injury_pos_tagged = nltk.pos_tag(has_injuries_words)
        #print(injury_pos_tagged)

        injury_regex = r"""
                      INjury:
                        {<.*>+}          # Chunk everything
                        }<CC|IN|NNS|NN|DT|WRB>+{      # Chink sequences of VBD and IN
                  """
        injury_parser = nltk.RegexpParser(injury_regex)
        injury_occurence = injury_parser.parse(injury_pos_tagged)
        #print(injury_occurence)


    def death_number(self):
        death = death_no(self.splitted_sentences)
        if death == "None":
            actualdeath = death
            deathNo = 0
        else:
            actualdeath = remove_date(death)
            deathNo = convertNum(death)
        # print("Death No: ")
        # print(death, actualdeath, deathNo)
        #
        # print("\n No of dead people: " + str(deathNo))
        return(deathNo)


    def injury_number(self):
        injury = injury_no(self.splitted_sentences)
        if injury == "None":
            actualinjury = "None"
            injuryNo = 0
        else:
            actualinjury = remove_date(injury)
            injuryNo = convertNum(injury)
        # print("Injury No:")
        # print(injury, actualinjury, injuryNo)
        # print("\n No of injured people: " + str(injuryNo))
        return(injuryNo)
