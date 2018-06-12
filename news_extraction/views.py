from django.shortcuts import render, get_object_or_404
from .models import *

import os
import sys

import nltk

from modules.tagger import Tagger
from modules.extractor import DataExtractor
from modules.tokenizer import Tokenize
import spacy
import en_core_web_sm
import nltk
import sys

from spacy.matcher import Matcher,PhraseMatcher
from spacy.attrs import POS,LOWER,IS_PUNCT

from modules.vehicles_gazetter import VehicleInformation


# import spacy
# import en_core_web_sm
# import nltk
# import sys
#
# from spacy.matcher import Matcher,PhraseMatcher
# from spacy.attrs import POS,LOWER,IS_PUNCT
#
# from modules.vehicles_gazetter import VehicleInformation
# # from spacy import displacy
# # nlp = spacy.load('en_core_web_sm')
# nlp = en_core_web_sm.load()

#
nlp = en_core_web_sm.load()
news_story = """A woman died after being hit by a bus in Gyaneshwor on Monday.
The victim has been identified as Goshan Mikrani Begham (49) of Sarlahi.
Critically injured in the incident, she was rushed to the Bansbari-based Neuro Hospital where she breathed her last during the course of treatment, police said.
The incident took place at around 7 am yesterday.
Police said that they have impounded the vehicle Ba 2 Kha 7085 and Ko 2 Pa 7086 and arrested its driver for investigation."""

news = Tokenize(news_story)
splited_sentences = nltk.sent_tokenize(news_story)
tokenized_words = news.split_words()
tagger = Tagger(tokenized_words)
pos_tagged_sentences = tagger.tag()
data_extractor = DataExtractor(pos_tagged_sentences, news_story)
sentences = news.split_story()
data_extractor.day(news_story)

print("Extracting")
#
# vehicle_information = VehicleInformation(news_story)
# vehicle_information.make_gazetter()
# all_vehicles = vehicle_information.find_vehicles()
record = rssdata(header= "Heading",
                 body= news_story.replace("\n", ""),
                 death= data_extractor.deaths(nltk.sent_tokenize(news_story)),
                 death_no = data_extractor.death_number(),
                 injury = data_extractor.injury(nltk.sent_tokenize(news_story)),
                 injury_no = data_extractor.injury_number(),
                 location = data_extractor.location(),
                 vehicle_involved = data_extractor.vehicle_involved(),
                 vehicle_no = data_extractor.vehicle(),
                 day = data_extractor.day(news_story)
               )
# print(all_vehicles)
record.save()
vehicle_information = VehicleInformation(news_story)
vehicle_information.make_gazetter()
all_vehicles,two_wheeler,three_wheeler,four_wheeler = vehicle_information.find_vehicles()
#
# print(all_vehicles,two_wheeler,three_wheeler,four_wheeler)
# vehicles = ""
# for vehicle in all_vehicles:
#     vehicles = vehicles + " "+ vehicle
# vehicles = vehicles[1:]
#
# print(vehicles)
# print("contains four wheeler "+ str(four_wheeler))
# print("contains two wheeler "+ str(two_wheeler))
# print("contains three wheeler " + str(three_wheeler))
# print("Saved")

def index(request):
    return render(request, 'index.html',
                  context={'news': rssdata.objects.all()})
