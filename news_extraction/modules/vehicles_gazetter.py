import spacy
import en_core_web_sm

from spacy.matcher import Matcher
from spacy.attrs import POS,LOWER,IS_PUNCT,LEMMA

nlp = en_core_web_sm.load()


vehicles = ['bus','car','truck','tipper','bike','zeep','scooter','scooty',
        'motorbike','container','SUV','tractor','moped','lorry','minivan',
        'minibus','trolley']

matcher = Matcher(nlp.vocab)
class VehicleInformation:
    def __init__(self,news_story):
        self.news_story = news_story


    def make_gazetter(self):
        for vehicle in vehicles:
            matcher.add_pattern("Vehicles", [{LEMMA:vehicle}])
        matcher.add_pattern("Vehicles", [{LEMMA:'two'},{IS_PUNCT:True},{LEMMA:'wheeler'}])
        matcher.add_pattern("Vehicles", [{LEMMA:'two'},{LEMMA:'wheeler'}])
        matcher.add_pattern("Vehicles", [{LEMMA:'four'},{IS_PUNCT:True},{LEMMA:'wheeler'}])
        matcher.add_pattern("Vehicles", [{LEMMA:'four'},{LEMMA:'wheeler'}])

    def find_vehicles(self):
        vehicles_found = set()
        document = unicode(self.news_story.decode('utf8'))
        doc = nlp(document)
        # matcher = Matcher(nlp.vocab)

        matches = matcher(doc)
        for ent_id, label, start, end in matches:
            vehicles_found.add(unicode(doc[start:end].text).encode('utf8'))
        return(vehicles_found)
