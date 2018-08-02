from .models import *
import re
import unicodedata
from modules.tagger import Tagger
from modules.extractor import DataExtractor
from modules.tokenizer import Tokenize
import en_core_web_sm
import feedparser
from modules.vehicles_gazetter import VehicleInformation
from goose import Goose
from requests import get
from bs4 import BeautifulSoup
import urllib

nlp = en_core_web_sm.load()

def extract_info(news_story):
    news = Tokenize(news_story)
    tokenized_words = news.split_words()
    tagger = Tagger(tokenized_words)
    pos_tagged_sentences = tagger.tag()
    extracted_data = DataExtractor(pos_tagged_sentences, news_story)
    extracted_data.day(news_story)
    return extracted_data


def vehicleinfo(news_story):
    vehicle_information = VehicleInformation(news_story)
    vehicle_information.make_gazetter()
    all_vehicles, two_wheeler, three_wheeler, four_wheeler = vehicle_information.find_vehicles()

    if (all_vehicles==set([])):
        return('[]','[]','[]')
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
    print ("old links are: \n ",oldlinks)
    for i in range(0, len(links)):
        if links[i] not in oldlinks:
            response = get(links[i])
            extractor = Goose()
            article = extractor.extract(raw_html=response.content)
            texts = article.cleaned_text
            news_story = texts.encode('utf-8')
            print ("new links:\n", links[i])
            extract(links[i], news_story, title[i])


def extract(link, news_story, title):
    a = re.search(r'[A-Z]\w+\s\d+[,.]\s\d+', news_story)
    num = a.start()
    news_story = news_story[num:]
    news_story = unicode(news_story.decode('utf-8'))
    # for news in news_story:
    new_news_story = unicodedata.normalize('NFKD', news_story).encode('ascii', 'ignore')
    news_story = new_news_story
    news_story = news_story.replace("\n", "")
    news = Tokenize(news_story)
    date, day, month, year, news_story = news.get_date(news_story)
    tokenized_words = news.split_words()
    tagger = Tagger(tokenized_words)
    pos_tagged_sentences = tagger.tag()
    data_extractor = DataExtractor(pos_tagged_sentences, news_story)
    injury_no, injuries = data_extractor.injury_number()
    death_no, death = data_extractor.death_number()
    cause = data_extractor.get_cause()
    if death_no == injury_no:
        injury_no = '0'
    vehicle0, vehicle1, vehicle_type = vehicleinfo(news_story)



    record = rssdata(
                     header=title,
                     source="Kathmandu Post",
                     body=news_story.replace("\n", ""),
                     death=death,
                     link=link,
                     injury_no=injury_no,
                     death_no=death_no,
                     location=data_extractor.location(),
                     vehicleone=vehicle0,
                     vehicletwo=vehicle1,
                     cause=cause,
                     injury=injuries,
                     vehicle_type=vehicle_type,
                     vehicle_no=data_extractor.vehicle(),
                     day=data_extractor.day(news_story),
                     date=date,
                     month=month,
                     year=year
                     )
    record.save()
    return record.id
    # # news_id = record.id
    # save_record_by_id(news_id)


def manual_extract(link):

    url = urllib.urlopen(link)
    content = url.read()
    soup = BeautifulSoup(content, 'lxml')

    article_text = []
    article = soup.find("div", {"class": "content-wrapper"}).findAll('p')
    title = soup.find("div", {"class": "no-space"}).h1

    for element in article:
        for e in element.findAll(text=True):
            if len(e)>2:
                article_text.append(e)

    return (link, str(article_text), title.text)

