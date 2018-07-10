from .models import *
from forms import NameForm
import re
import os
import sys
import spacy

from django.shortcuts import render, get_object_or_404
from .models import *
from BeautifulSoup import BeautifulSoup
import urllib2
import re


from modules.tagger import Tagger
from modules.extractor import DataExtractor
from modules.tokenizer import Tokenize
import en_core_web_sm
import nltk
import feedparser
from spacy.matcher import Matcher,PhraseMatcher
from spacy.attrs import POS,LOWER,IS_PUNCT
import datefinder
from modules.vehicles_gazetter import VehicleInformation
from goose import Goose
from requests import get

nlp = en_core_web_sm.load()


# sample_news_heading = "Accident happened"
# sample_news_story = """In Thamel, A woman died after being hit by a bus on Monday.
#     The victim has been identified as Goshan Mikrani Begham (49) of Sarlahi.
#     Critically injured in the incident, she was rushed to the Bansbari-based Neuro Hospital where she breathed her last during the course of treatment, police said.
#     The incident took place at around 7 am yesterday.
#     Police said that they have impounded the vehicle Ba 2 Kha 7085 and Ko 2 Pa 7086 and arrested its driver for investigation."""

def extract_info(news_story):
    news = Tokenize(news_story)
    splited_sentences = nltk.sent_tokenize(news_story)
    tokenized_words = news.split_words()
    tagger = Tagger(tokenized_words)
    pos_tagged_sentences = tagger.tag()
    extracted_data = DataExtractor(pos_tagged_sentences, news_story)
    sentences = news.split_story()
    extracted_data.day(news_story)
    return extracted_data

def vehicleinfo(news_story):
    vehicle_information = VehicleInformation(news_story)
    vehicle_information.make_gazetter()
    all_vehicles, two_wheeler, three_wheeler, four_wheeler = vehicle_information.find_vehicles()
    vehicles = []
    vehicle0 = ''
    vehicle1 = ''
    for vehicle in all_vehicles:
        vehicles.append(vehicle)
    vehicle_type = []
    if two_wheeler is 1:
        vehicle_type.append("two wheeler")
    if three_wheeler is 1:
        vehicle_type.append("three wheeler")
    if four_wheeler is 1:
        vehicle_type.append("four wheeler")
    for x in range(0, len(vehicles)):
        if x < 1:
            vehicle0 = vehicles[0]
            vehicle1 = '[]'
        if x > 0:
            vehicle0 = vehicles[0]
            vehicle1 = vehicles[1]

    return (vehicle0, vehicle1, vehicle_type)

def save_extracted_info(news_heading, news_story, extracted_data):
    vehicle0, vehicle1, vehicle_type = vehicleinfo(news_story)
    print vehicle0
    news = Tokenize(news_story)
    date, day, month, year, news_story = news.get_date(news_story)
    print("Extracting")
    record = rssdata(header= news_heading,
                     body= news_story.replace("\n", ""),
                     death= extracted_data.deaths(nltk.sent_tokenize(news_story)),
                     death_no = extracted_data.death_number(),
                     injury = extracted_data.injury(nltk.sent_tokenize(news_story)),
                     injury_no = extracted_data.injury_number(),
                     location = extracted_data.location(),
                     vehicleone=vehicle0,
                     vehicletwo=vehicle1,
                     vehicle_type=vehicle_type,
                     vehicle_no = extracted_data.vehicle(),
                     day = day,
                     date = date,
                     month = month,
                     season= extracted_data.get_season(month),
                     year= year,
                   )
    record.save()
    return record


def save_record_by_id(news_id):
    record = rssdata.objects.get(id=news_id)
    news_story = record.body
    extracted_data = extract_info(news_story)
    record.location = extracted_data.location()
    record.save()


# print(VehicleInformation.names())

#scrape rss feed
url_link = "http://fetchrss.com/rss/59549c628a93f872018b4567709026440.xml"
# get all the links of news title
links = []
text =[]
title = []
rss = feedparser.parse(url_link)

for post in rss.entries:
    links.append(post.link)
    title.append(post.title_detail.value)
oldlinks = rssdata.objects.values_list('link', flat=True)
# print oldlinks
for i in range(0, len(links)):
    if links[i] not in oldlinks:
        print links[i]
        response = get(links[i])
        extractor = Goose()
        article = extractor.extract(raw_html=response.content)
        texts = article.cleaned_text
        news_story = texts.encode('utf-8')
        # print i
        a = re.search(r'[A-Z]\w+\s\d+[,.]\s\d+', news_story)
        num = a.start()
        news_story = news_story[num:]
        news = Tokenize(news_story)
        #news.get_date()
        date,day,month,year,news_story = news.get_date(news_story)
        news = Tokenize(news_story)

        splited_sentences = nltk.sent_tokenize(news_story)
        tokenized_words = news.split_words()
        tagger = Tagger(tokenized_words)
        pos_tagged_sentences = tagger.tag()
        data_extractor = DataExtractor(pos_tagged_sentences, news_story)
        sentences = news.split_story()
        vehicle0, vehicle1, vehicle_type = vehicleinfo(news_story)
        record = rssdata(header=title[i],
                         source = "Kathmandu Post",
                         body=news_story.replace("\n", ""),
                         death=data_extractor.deaths(nltk.sent_tokenize(news_story)),
                         link = links[i],
                         injury_no= data_extractor.injury_number(),
                         death_no = data_extractor.death_number(),
                         vehicleone = vehicle0,
                         vehicletwo = vehicle1,
                         injury = data_extractor.injury(nltk.sent_tokenize(news_story)),
                         vehicle_type=vehicle_type,
                         vehicle_no=data_extractor.vehicle(),
                         day=data_extractor.day(news_story),
                        date= date,
                        month = month,
                        year = year,
                         season = data_extractor.get_season(month),

                         )
        record.save()
        news_id = record.id
        save_record_by_id(news_id)



def index(request):
    # extracted_data = extract_info(sample_news_story)
    # save_extracted_info(sample_news_heading, sample_news_story, extracted_data)
    return render(request, 'index.html',
                  context={'news': rssdata.objects.all().order_by("-id")})


def extraction(request):
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            extracted_data = extract_info(data['news_text'])

            # If you want to save the input news
            story = save_extracted_info(data['news_title'], data['news_text'], extracted_data)

        return render(request, 'extraction.html', {'form': form,
                                                   'news_id': story.pk,
                                                   'article': rssdata.objects.get(pk=story.pk)})

    else:
        form = NameForm()

    return render(request, 'extraction.html', {'form': form})