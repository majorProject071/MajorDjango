from django.shortcuts import render, get_object_or_404
from .models import *

import os
import sys

import nltk

from modules.tagger import Tagger
from modules.extractor import DataExtractor
from modules.tokenizer import Tokenize

news_story = """A woman died after being hit by a bus in Sinamangal of Kathmandu on Monday.
The victim has been identified as Goshan Mikrani Begham (49) of Sarlahi.
Critically injured in the incident, she was rushed to the Bansbari-based Neuro Hospital where she breathed her last during the course of treatment, police said.
The incident took place at around 7 am yesterday.
Police said that they have impounded the vehicle Ba 2 Kha 7085 and arrested its driver for investigation."""

news = Tokenize(news_story)
splited_sentences = nltk.sent_tokenize(news_story)
tokenized_words = news.split_words()
tagger = Tagger(tokenized_words)
pos_tagged_sentences = tagger.tag()
data_extractor = DataExtractor(pos_tagged_sentences, news_story)
sentences = news.split_story()
data_extractor.day(news_story)

print("From the modular component")
print("--------------------------------")
print(data_extractor.location())
print(data_extractor.death_number())
print(data_extractor.injury_number())

# injuries = data_extractor.injury(nltk.sent_tokenize(news_story))

print("\nThe vehicles involved are:")
data_extractor.vehicle()

def index(request):
    return render(request, 'index.html',
                  context={'news': rssdata.objects.all()})