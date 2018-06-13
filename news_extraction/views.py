from django.shortcuts import render, get_object_or_404
from .models import *
import json
import os
import sys

import nltk

from modules.tagger import Tagger
from modules.extractor import DataExtractor
from modules.tokenizer import Tokenize
import spacy
import en_core_web_sm
import nltk
import feedparser
from goose import Goose
import sys
import html2text
import requests
from spacy.matcher import Matcher,PhraseMatcher
from spacy.attrs import POS,LOWER,IS_PUNCT

from modules.vehicles_gazetter import VehicleInformation
from goose import Goose
from requests import get

nlp = en_core_web_sm.load()

#scrape rss feed
url_link = "http://fetchrss.com/rss/59549c628a93f872018b4567709026440.xml"
# get all the links of news title
links = []
text =[]
rss = feedparser.parse(url_link)
for post in rss.entries:
    links.append(post.link)
for link in links:
    response = get(link)
    extractor = Goose()
    article = extractor.extract(raw_html=response.content)
    texts = article.cleaned_text
    text.append(texts)

#take individual text
for i in range(0,len(text)):
    news_story = text[i].encode('utf-8')
    news = Tokenize(news_story)
    splited_sentences = nltk.sent_tokenize(news_story)
    tokenized_words = news.split_words()
    tagger = Tagger(tokenized_words)
    pos_tagged_sentences = tagger.tag()
    data_extractor = DataExtractor(pos_tagged_sentences, news_story)
    sentences = news.split_story()
    data_extractor.day(news_story)

    #vehicle gazetter
    vehicle_information = VehicleInformation(news_story)
    vehicle_information.make_gazetter()
    all_vehicles, two_wheeler, three_wheeler, four_wheeler = vehicle_information.find_vehicles()
    #
    vehicles = ""
    for vehicle in all_vehicles:
        vehicles = vehicles + " "+ vehicle
    vehicles = vehicles[1:]
    #
    print(vehicles)
    print("contains four wheeler "+ str(four_wheeler))
    print("contains two wheeler "+ str(two_wheeler))
    print("contains three wheeler " + str(three_wheeler))
    print("Saved")
    record = rssdata(header="Heading",
                     body=news_story.replace("\n", ""),
                     death=data_extractor.deaths(nltk.sent_tokenize(news_story)),
                     )
    print("body", record.body)

news_story = """A woman died after being hit by a bus in Baneshwor on Monday.
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
print("hello")
print("Saved")

def index(request):
    return render(request, 'index.html',
                  context={'news': rssdata.objects.all()})
