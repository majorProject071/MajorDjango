from .models import *
import re

from modules.tagger import Tagger
from modules.extractor import DataExtractor
from modules.tokenizer import Tokenize
import en_core_web_sm
import nltk
import feedparser
from modules.vehicles_gazetter import VehicleInformation
from goose import Goose
from requests import get

nlp = en_core_web_sm.load()

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
    print(news_story)
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


#scrape rss feed
def initial_check():
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
            a = re.search(r'[A-Z]\w+\s\d+[,.]\s\d+', news_story)
            num = a.start()
            news_story = news_story[num:]
            news = Tokenize(unicode(news_story, 'utf-8'))
            date,day,month,year,news_story = news.get_date(news_story)
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

