from difflib import SequenceMatcher

heading1 = "1 killed, 3 injured in Sunsari bus accident"
heading2 = "1 killed, 3 injured in Sunsari bus accident"

body1 = "May 23, 2018-A person died and 3 others were injured when a commuter bus (Na 4 Kha 4258) overturned at Apachhi" \
        " in Itahari-1 of Sunsari along the Koshi Highway on Wednesday." \
        "According to the Area Police Office, Itahari, the incident occurred due to overspeed." \
        "The injured are undergoing treatment at the Dharan-based BP Koirala Institute of Health Sciences."

body2 = "May 23, 2018-A person died and 3 others were injured when a commuter bus (Na 4 Kha 4258) overturned at Apachhi" \
        " in Itahari-1 of Sunsari along the Koshi Highway on Wednesday." \
        "According to the Area Police Office, Itahari, the incident occurred due to overspeed." \
        "The injured are undergoing treatment at the Dharan-based BP Koirala Institute of Health Sciences."

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
    if heading_similarity(heading1, heading2) > 0.9 or heading_similarity(heading1, heading2) is None:
        if body_similarity(body1, body2) > 0.85:
            print ("News are same")
    elif date_similarity(date1, date2)\
            and location_similarity(location1, location2) > 0.9 or location_similarity(location1, location2) is None\
            and vehicle_similarity(vehicle1, vehicle2)\
            and vehicle_similarity(vehicle_number1, vehicle_number2):
        if death1 is not None and death2 is not None and injury1 is not None and injury2 is not None and \
                (death1==death2) and (injury1==injury2):
                print ("News are same")
    else:
        print ("News are different")

news_similarity()


# def news_similarity():
#     if date_similarity(date1,date2):
#         if location_similarity(location1,location2):
#             if vehicle_similarity(vehicle_nos1,vehicle_nos2):
#                 print("News are same")
#             elif vehicle_similarity(vehicles1,vehicles2):
#                 if (death1==death2) and (injury1==injury2):
#                     print("News are same")
#                 elif (death1 == None) and (death2 == None):
#                     if(injury1==injury2):
#                         print("News are same")
#                 elif (injury1 == None) and (injury2 == None):
#                     if(death1==death2):
#                         print("News are same")
#                 else:
#                     print("News are different")
#             else:
#                 print("News are different")
#         else:
#             print("News are different (location)")
#     else:
#         print("News are different (date)")

