
from .models import *
from forms import NameForm
import re

from django.shortcuts import render, get_object_or_404
from .models import *


from modules.tagger import Tagger
from modules.extractor import DataExtractor
from modules.tokenizer import Tokenize
import en_core_web_sm
import nltk
import feedparser

import datefinder
from modules.vehicles_gazetter import VehicleInformation
from goose import Goose
from requests import get

nlp = en_core_web_sm.load()

# #scrape rss feed
# url_link = "http://fetchrss.com/rss/59549c628a93f872018b4567709026440.xml"
# # get all the links of news title
# links = []
# text =[]
# rss = feedparser.parse(url_link)
# for post in rss.entries:
#     links.append(post.link)
#
# for link in links:
#     response = get(link)
#     extractor = Goose()
#     article = extractor.extract(raw_html=response.content)
#     texts = article.cleaned_text
#     text.append(texts)
# #
# #take individual text
# for i in range(0,len(text)):
#     news_story = text[i].encode('utf-8')
#     print(news_story)
#     news = Tokenize(news_story)
#     splited_sentences = nltk.sent_tokenize(news_story)
#     tokenized_words = news.split_words()
#     tagger = Tagger(tokenized_words)
#     pos_tagged_sentences = tagger.tag()
#     data_extractor = DataExtractor(pos_tagged_sentences, news_story)
#     sentences = news.split_story()
#
#     #vehicle gazetter
#     vehicle_information = VehicleInformation(news_story)
#     vehicle_information.make_gazetter()
#     all_vehicles, two_wheeler, three_wheeler, four_wheeler = vehicle_information.find_vehicles()
#     #
#     vehicles = ""
#     for vehicle in all_vehicles:
#         vehicles = vehicles + " "+ vehicle
#     vehicles = vehicles[1:]
#     #
#
#     record = rssdata(header="Heading",
#                      body=news_story.replace("\n", ""),
#                      death=data_extractor.deaths(nltk.sent_tokenize(news_story)),
#                      day=data_extractor.day(news_story),
#                      date = data_extractor.date(news_story),
#                      month = data_extractor.get_month(news_story),
#                      season= data_extractor.get_season(news_story),
#                      year=data_extractor.get_year(news_story),
#
#                      )
#     print("body", record.day)
#     print("body", record.date)
#     print("body", record.month)
#     print("body", record.season)
#     print("body", record.year)

news_story = """Jun 13, 2018-An irate mob torched a tipper following a road accident along the Koteshwor-Jadibudti road section in the Capital on Wednesday, police said.

The tipper (Na 4 Kha 3558) en route to Koteshwor from Jadibuti carrying sand had hit a scooter (Ba 70 Pa 9399) from behind, leaving the rider seriously injured. The injured scooter rider has been taken to Satdobato-based B&B Hospital for medical treatment.

Meanwhile, the tipper driver has been detained at Tinkune-based police office.

Two fire trucks were sent to douse the fire.

Road accidents are on the rise in the Capital roads in recent days and these accidents are often blamed for over-speeding tipper and trucks.

"""


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
                 day = data_extractor.day(news_story),
                 date = data_extractor.date(news_story),
                 month = data_extractor.get_month(news_story),
                 season= data_extractor.get_season(news_story),
                 year=data_extractor.get_year(news_story),

               )
record.save()
vehicle_information = VehicleInformation(news_story)
vehicle_information.make_gazetter()
all_vehicles,two_wheeler,three_wheeler,four_wheeler = vehicle_information.find_vehicles()

# print(all_vehicles,two_wheeler,three_wheeler,four_wheeler)
vehicles = ""
for vehicle in all_vehicles:
    vehicles = vehicles + " "+ vehicle
vehicles = vehicles[1:]

print(vehicles)
print("contains four wheeler "+ str(four_wheeler))
print("contains two wheeler "+ str(two_wheeler))
print("contains three wheeler " + str(three_wheeler))
print("Saved")
print("hello")
print("Saved")

def index(request):
    return render(request, 'index.html',
                  context={'news': rssdata.objects.all()})

def extraction(request):
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            story = rssdata()
            story.body = data['news_text']
            story.save()
        return render(request, 'extraction.html', {'form': form})

    else:
        form = NameForm()

    return render(request, 'extraction.html', {'form': form})