import spacy
import en_core_web_sm

from spacy.matcher import Matcher
from spacy.attrs import POS,LOWER,IS_PUNCT,LEMMA

nlp = en_core_web_sm.load()


vehicles = ['bus','car','truck','tipper','bike','zeep','jeep','scooter','scooty',
        'motorbike','motorcycle','container','SUV','tractor','moped','lorry',
        'minivan','minibus','trolley','tempo']
three_wheeler=set([
'tempo','three-wheeler','three wheeler'
])

two_wheeler = set([
'bike','scooter','scooty','motorbike','motorcycle','two-wheeler','two wheeler','moped'
])

four_wheeler = set([
'bus','car','truck','tipper','zeep','container','SUV','tractor','moped','lorry',
'minivan','minibus','trolley','four-wheeler','four wheeler','jeep'
])

scooty = ['scooter','scooty']
bike = ['bike','motorbike','motorcycle']
zeep = ['zeep','jeep']


CAUSUAL_WORDS = ["consequently", "as a result", "therfore", "as a result",
                 "as a consequence", "for these reason", "thus", "due",
                 "for all these reasons", "because of", "because", "since",
                 "thus", "cause", "occur", "accord", "say", "after", "off"]

matcher = Matcher(nlp.vocab)

cause_matcher = Matcher(nlp.vocab)
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
        is_four_wheeler=is_three_wheeler=is_two_wheeler = 0


        matches = matcher(doc)
        for ent_id, label, start, end in matches:
            vehicles_found.add(unicode(doc[start:end].text).encode('utf8'))
        all_vehicles = list(vehicles_found)
        for i in range(0,len(all_vehicles)):
            if all_vehicles[i] in zeep:
                all_vehicles[i] = "zeep"
            if all_vehicles[i] in scooty:
                all_vehicles[i] = "scooty"
            if all_vehicles[i] in bike:
                all_vehicles[i] = "bike"
        vehicles_found = set(all_vehicles)


        if(len(vehicles_found.intersection(two_wheeler))!=0):
            is_two_wheeler = 1
        if(len(vehicles_found.intersection(three_wheeler))!=0):
            is_three_wheeler = 1
        if(len(vehicles_found.intersection(four_wheeler))!=0):
            is_four_wheeler = 1
        return(vehicles_found,is_two_wheeler,is_three_wheeler,is_four_wheeler)

    def get_cause(self):
        CAUSUAL_SENTENCES = []
        DOCUMENT = unicode(self.news_story.decode('utf8'))
        DOC = nlp(DOCUMENT)
        for word in CAUSUAL_WORDS:
            matcher.add_pattern("Causual sentence", [{LEMMA: word}])

        for sent in DOC.sents:
            new_sent = nlp(unicode(str(sent).decode('utf8')))
            matches = matcher(new_sent)
            if len(matches) > 0:
                CAUSUAL_SENTENCES.append(sent)
        return CAUSUAL_SENTENCES