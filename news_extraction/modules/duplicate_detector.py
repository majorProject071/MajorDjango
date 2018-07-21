from difflib import SequenceMatcher

heading1 = "2 dead in auto collision"
heading2 = "Two die in Saptari road accident"

body1 = "Two persons died when a speeding bus hit a motorcycle in Saptari district on Wednesday night.Police said Rupesh " \
        "Chaudhary, 35, and Roshan Chaudhary, 20, of Shambhunath Municipality-2 died during treatment.The bus driver was " \
        "taken into custody for investigation."

body2 = "Two persons died when a speeding bus hit a motorcycle in Saptari district on Wednesday night." \
        "The police have identified the deceased as Rupesh Chaudhary, 35, and Roshan Chaudhary, 20, of " \
        "Shambhunath Municipality-2 in the district.The Chaudhary duo were critically injured during the accident" \
        " and died while undergoing treatment.The bus driver has been taken into police custody for investigation."

date1 = "2018-05-23"
date2 = "2018-05-23"

death1 = 1
death2 = 1

injury1 = 3
injury2 = 3

location1 = "Itahari-1 of Sunsari"
location2 = "Itahari-1 of Sunsari"

vehicle_number1 = ["Na 4 Kha 4258"]
vehicle_number2 = ["Na 4 Kha 4258"]

vehicle1 = ["bus", "car"]
vehicle2 = ["bus"]

def heading_similarity(h1,h2):
    ratio = SequenceMatcher(None, h1, h2).ratio()
    if ratio != 0:
        return ratio

def body_similarity(b1,b2):
    return SequenceMatcher(None, b1, b2).ratio()

def date_similarity(d1,d2):
    return SequenceMatcher(None, d1, d2).ratio()

def location_similarity(loc1,loc2):
    return SequenceMatcher(None, loc1, loc2).ratio()

def vehicle_similarity(v1,v2):
    difference = list(set(v1) - set(v2))
    difference.extend(list(set(v2) - set(v1)))
    if difference is not None:
        return False
    else:
        return True

vehicle_similarity(vehicle2, vehicle1)

def news_similarity():
    print (body_similarity(body1, body2))
    if heading_similarity(heading1, heading2) > 0.9 or heading_similarity(heading1, heading2) is None:
        if body_similarity(body1, body2) > 0.80:
            print ("News are same.")
    elif body_similarity(body1, body2) > 0.80:
        print ("News are sameee.")
    # elif date_similarity(date1, date2)\
    #         and location_similarity(location1, location2) > 0.9 or location_similarity(location1, location2) is None\
    #         and vehicle_similarity(vehicle1, vehicle2)\
    #         and vehicle_similarity(vehicle_number1, vehicle_number2):
    #     if death1 is not None and death2 is not None and injury1 is not None and injury2 is not None and \
    #             (death1==death2) and (injury1==injury2):
    #             print ("News are same")
    else:
        print ("News are different")

news_similarity()
