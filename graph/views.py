from __future__ import division
from django.db.models import Q, Count, Sum, Max, Value
from django.shortcuts import render

import json
from news_extraction.models import rssdata
from news_extraction.modules.location_tree import LocationInformation
from getqueries.newqueries import Query
import geocoder
import datetime
import re


def parameters():
    """ provide parameter to select tag for location in location.html """

    """import all location from database"""
    listoflocation = rssdata.objects.values('location').order_by('location').annotate(count=Count('location'))

    """ import all location from kathmandu, bhaktapur, lalitpur and outside from location_tree.py """
    ktm_location = LocationInformation().all_ktm_locations()
    bkt_location = LocationInformation().all_bkt_locations()
    ltp_location = LocationInformation().all_ltp_locations()
    outside_location = LocationInformation().all_locations()

    """ list definition"""
    alllocationlist = []
    ktmlocationlist = []
    ltplocationlist = []
    bktlocationlist = []

    for findlocation in listoflocation:

        """ check if defined location is in kathmandu or lalitpur or bhaktapur or others"""
        if findlocation['location'] in ktm_location:
            """ add location to kathmandu location list and
            add kathmandu to all location"""
            ktmlocationlist.append({'location': findlocation['location'].capitalize()})
            if 'Kathmandu' not in alllocationlist:
                alllocationlist.append('Kathmandu')

        elif findlocation['location'] in ltp_location:
            """ add location to Lalitpur location list and
            add Lalitpur to all location"""
            ltplocationlist.append({'location': findlocation['location'].capitalize()})
            if 'Lalitpur' not in alllocationlist:
                alllocationlist.append('Lalitpur')

        elif findlocation['location'] in bkt_location:
            """ add location to Bhaktapur location list and
                add Bhaktapur to all location"""
            bktlocationlist.append({'location': findlocation['location'].capitalize()})
            if 'Bhaktapur' in alllocationlist:
                alllocationlist.append('Bhaktapur')

        elif findlocation['location'] in outside_location:
            alllocationlist.append(findlocation['location'].capitalize())

        else:
            pass

    return alllocationlist, ktmlocationlist, ltplocationlist, bktlocationlist


def finalquery(countlist):
    """after getting queries from newquries, convert it to required format needed"""

    """ import all location from location tree"""
    ktm_location = LocationInformation().all_ktm_locations()
    bkt_location = LocationInformation().all_bkt_locations()
    ltp_location = LocationInformation().all_ltp_locations()
    outside_location = LocationInformation().all_locations()
    """ initialize all necessary parameter"""
    ktm_death = 0
    ktm_count = 0
    ktm_injury = 0
    ltp_death = 0
    ltp_count = 0
    ltp_injury = 0
    bkt_death = 0
    bkt_count = 0
    bkt_injury = 0
    maplocations = []
    barlocations = []
    maplocation = []

    """ now return query for map location and bar location."""
    for location in countlist:
        if location['location'].lower() in ktm_location or location['location'] == "kathmandu":
            ktm_death += location['death']
            ktm_injury += location['injury']
            ktm_count += location['count']
            barlocations.append({'location': 'Kathmandu', 'injury': ktm_injury, 'value': ktm_death})
            maplocation.append(
                {'location': 'Kathmandu', 'injury': ktm_injury, 'value': ktm_death, 'count': ktm_count})
        elif location['location'].lower() in ltp_location or location['location'] == "lalitpur":
            ltp_death += location['death']
            ltp_injury += location['injury']
            ltp_count += location['count']
            barlocations.append({'location': 'Lalitpur', 'injury': ltp_injury, 'value': ltp_death})
            maplocation.append(
                {'location': 'Lalitpur', 'injury': ltp_injury, 'value': ltp_death, 'count': ltp_count})
        elif location['location'].lower() in bkt_location or location['location'] == "bhaktapur":
            bkt_death += location['death']
            bkt_injury += location['injury']
            bkt_count += location['count']
            barlocations.append({'location': 'Bhaktapur', 'injury': bkt_injury, 'value': bkt_death})
            maplocation.append(
                {'location': 'Bhaktapur', 'injury': bkt_injury, 'value': bkt_death, 'count': bkt_count})
        elif location['location'].lower() in outside_location:
            maplocation.append({'location': location['location'].capitalize(), 'value': location['death'],
                                 'injury': location['injury'], 'count': location['count']})
            barlocations.append({'location': location['location'].capitalize(), 'value': location['death'],
                                 'injury': location['injury']})
        else:
            pass


    for mlocation in maplocation:
        rate = int(mlocation['count']/len(maplocation)*100)
        maplocations.append(
            {'location': mlocation['location'], 'injury': mlocation['injury'], 'death': mlocation['value'],
             'count': mlocation['count'], 'rate': rate})

    red = int(25/100*len(maplocations))
    yellow = int(10/100* len(maplocations))
    return red, yellow, barlocations, maplocations


def vehicleparameters():

    """ provide vehicle related data to select parameter"""

    """initialization of array"""
    vehicledata = []
    vehicletype = []
    vehicletwowheeler = []
    vehiclethreewheeler = []
    vehiclefourwheeler = []

    """required queryset"""
    vehicletypelist = rssdata.objects.values('vehicle_type')
    vehiclelistone = rssdata.objects.values('vehicleone').order_by('vehicleone').annotate(count=Count('vehicleone'))
    vehiclelisttwo = rssdata.objects.values('vehicletwo').order_by('vehicletwo').annotate(count=Count('vehicletwo'))

    """required search parameters"""
    vehicle_types = ['two wheeler', 'three wheeler', 'four wheeler']
    three_wheeler = ['tempo', 'three-wheeler', 'three wheeler']

    two_wheeler = ['bike', 'scooter', 'scooty', 'motorbike', 'motorcycle', 'two-wheeler', 'two wheeler', 'moped']

    four_wheeler = ['bus', 'car', 'truck', 'tipper', 'zeep', 'container', 'SUV', 'tractor', 'moped', 'lorry',
                    'minivan', 'minibus', 'trolley', 'four-wheeler', 'four wheeler', 'jeep']

    """ vehicle type lieke 2-3-4 wheeler in database"""
    for newv in vehicletypelist:
        for v in vehicle_types:
            if v in newv['vehicle_type']:
                if v not in vehicletype:
                    vehicletype.append(v)

    """ make combine list of vehicle data from vehicle one and vehicle two"""
    for data in vehiclelistone:
        try:
            if len(data['vehicleone']) > 2:
                vehicledata.append(data['vehicleone'])
        except:
            pass
    for newdata in vehiclelisttwo:
        try:
            if len(newdata['vehicletwo']) > 2:
                if newdata['vehicletwo'] in vehicledata:
                    pass
                else:
                    vehicledata.append(newdata['vehicletwo'])
        except:
            pass

    """ assign vehicles to 2-3-4 categories"""
    for vdata in vehicledata:
        if vdata in two_wheeler:
            vehicletwowheeler.append(vdata)
        if vdata in three_wheeler:
            vehiclethreewheeler.append(vdata)
        if vdata in four_wheeler:
            vehiclefourwheeler.append(vdata)

    return vehicletype, vehicletwowheeler, vehiclethreewheeler, vehiclefourwheeler


def location(request):
    """ main function to control all the call all the subfunctions"""

    """ list of locations for select tag"""
    listoflocation, ktmlocationlist, ltplocationlist, bktlocationlist = parameters()

    """ list of vehicles for select tag"""
    vehicletype, vehicletwowheeler, vehiclethreewheeler, vehiclefourwheeler = vehicleparameters()

    """ yearlist for select tag"""
    yearlist = rssdata.objects.values('year').order_by('year').annotate(count=Count('year'))

    """ monthlist for select tag"""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    """ this is to get months in calender order"""
    monthlists = rssdata.objects.values('month').order_by('date').annotate(count=Count('month'))
    monthlist = []
    for month in monthlists:
        if month['month'] in months and month['month'] not in monthlist:
            monthlist.append(month['month'])

    """ starting and ending point for date from and date to"""
    datelistinc = rssdata.objects.values('date').order_by('date').annotate(count=Count('date'))
    date = datelistinc[0]['date']
    todaydate = datetime.datetime.now().date()

    """ location list to show initial data in visualization table """
    locationlist = rssdata.objects.values('location').order_by('location')\
        .annotate(count=Count('location')).annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no'))

    valueslist = []

    # working in search query
    if request.POST:
            """ above values are taken so that select tag could have this value 
            even when submit"""
            vehicletypeinfo = request.POST.get('vehicletype', None)
            yearinfo = request.POST.get('year', None)
            locationinfo = request.POST.get('location', None)
            monthinfo = request.POST.get('month', None)
            dateto = request.POST.get('to', None)
            datefrom = request.POST.get('from', None)

            """ assign user input to a list"""
            valueslist.append({'vehicletwoinfo': request.POST.get('vehicle_two', None), 'vehiclethreeinfo': request.POST.get('vehicle_three', None),
                               'vehiclefourinfo': request.POST.get('vehicle_four', None), 'vehicletypeinfo': vehicletypeinfo,
                               'yearinfo': yearinfo,  'locationinfo': locationinfo,'ktmlocationinfo': request.POST.get('ktmlocation', None),
                               'ltplocationinfo': request.POST.get('ltplocation', None), 'bktlocationinfo': request.POST.get('bktlocation', None),
                               'datefrom': datefrom, 'dateto': dateto, 'monthinfo': monthinfo})

            """ get required query for filter"""
            query = Query(valueslist, ktmlocationlist, ltplocationlist, bktlocationlist)
            newlocationlist, information, totalno, countlist = query.getqueries()

            """ get values in required format """
            red, yellow, barlocations, maplocations = finalquery(countlist)

            """ if querylength is zero """
            if (len(barlocations) == 0):
                context = {
                    'listoflocation': listoflocation, 'ktm_location': ktmlocationlist, 'ltp_location': ltplocationlist,
                    'bkt_location': bktlocationlist,'vehicletwo': vehicletwowheeler,'vehiclethree': vehiclethreewheeler,
                    'vehiclefour': vehiclefourwheeler,'vehicletype': vehicletype,
                    'yearlist': yearlist,'monthlist': monthlist, 'today': todaydate, 'start': date,
                    'monthvalue': monthinfo,'yearvalue': yearinfo, 'locationvalue': locationinfo, 'vehiclevalue': vehicletypeinfo, 'datetovalue': dateto,
                    'datefromvalue': datefrom,
                }
                return render(request, "findlocation.html", context)

            """ if querylength is greater than 0"""
            for location in barlocations:

                """ if both injury and death are zero then 
                it cannot be shown in bar graph"""
                if location['value'] == 0 and location['injury'] == 0:
                    context = {
                        'listoflocation': listoflocation, 'ktm_location': ktmlocationlist,'ltp_location': ltplocationlist,
                        'bkt_location': bktlocationlist, 'vehicletwo': vehicletwowheeler, 'vehiclethree': vehiclethreewheeler,
                        'vehiclefour': vehiclefourwheeler, 'vehicletype': vehicletype,
                        'yearlist': yearlist, 'monthlist': monthlist, 'today': todaydate, 'start': date,
                        'monthvalue': monthinfo, 'yearvalue': yearinfo, 'locationvalue': locationinfo,
                        'vehiclevalue': vehicletypeinfo, 'datetovalue': dateto, 'datefromvalue': datefrom,
                        'locationinfos': newlocationlist,
                        'totalno': totalno,
                        'info': information,
                        'checkparam': "none",
                    }
                    return render(request, "location.html", context)

            """ it is for bar graph and nepal map"""
            context = {
                'listoflocation': listoflocation, 'ktm_location': ktmlocationlist, 'ltp_location': ltplocationlist,
                'bkt_location': bktlocationlist, 'vehicletwo': vehicletwowheeler, 'vehiclethree': vehiclethreewheeler,
                'vehiclefour': vehiclefourwheeler, 'vehicletype': vehicletype,
                'yearlist': yearlist, 'monthlist': monthlist, 'today': todaydate, 'start': date,
                'monthvalue': monthinfo, 'yearvalue': yearinfo, 'locationvalue': locationinfo,
                'vehiclevalue': vehicletypeinfo, 'datetovalue': dateto, 'datefromvalue': datefrom,
                'locationinfos': newlocationlist,
                'location_data': json.dumps(barlocations),
                'totalno': totalno,
                'info': information,
                'newdata': json.dumps(maplocations),
                'red': red, 'yellow': yellow
            }
            return render(request, "location.html", context)

    totalno = len(locationlist)
    red, yellow, barlocations, maplocations = finalquery(locationlist)
    print maplocations
    context = {
        'listoflocation': listoflocation, 'ktm_location': ktmlocationlist, 'ltp_location': ltplocationlist,
        'bkt_location': bktlocationlist, 'vehicletwo': vehicletwowheeler, 'vehiclethree': vehiclethreewheeler,
        'vehiclefour': vehiclefourwheeler, 'vehicletype': vehicletype,
        'yearlist': yearlist, 'monthlist': monthlist, 'today': todaydate, 'start': date,
        'location_data': json.dumps(barlocations),
        'totalno': totalno,
        'newdata': json.dumps(maplocations),
        'red': red, 'yellow': yellow,
    }
    return render(request, "location.html", context)


def getLat(location):
    g = geocoder.google(location)
    return location, g.lat, g.lng


#query for kathmandu valley map
def index(request):
    location = rssdata.objects.values('location').order_by('location').annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no')).annotate(count=Count('location'))
    totalno = rssdata.objects.values('date').aggregate(total=Count('date'))
    datelistinc = rssdata.objects.values('date').order_by('date').annotate(count=Count('date'))
    datefrom = datelistinc[0]['date']
    dateto = datelistinc[len(datelistinc)-1]['date']
    latitude = []
    for locations in location:
        if locations['location'] is not None:
            if (len(locations['location']) > 2):
                location, lat, lng = getLat(locations['location'])
                while lat == None:
                    location, lat, lng = getLat(locations['location'])
                latitude.append(
                            {'location': location, 'latitude': lat, 'longitude': lng, 'death': locations['death'],
                                'injury': locations['injury'], 'count': locations['count']})



                # geolocator = Nominatim()
                # g = geolocator.geocode(loc)
                # latitude.append({'location': loc, 'latitude': g.latitude, 'longitude': g.longitude, 'death': locations['death'],
                #                      'injury': locations['injury']})


    context = {
        'latitude': latitude,
        'totalno': totalno,
        'datefrom': datefrom,
        'dateto': dateto,
    }
    return render(request, "heatmap.html", context)


def searchnumber(request):
    tablevehiclelist = rssdata.objects.all().values('vehicle_no').order_by('vehicle_no')

    tablevehicle = []
    vehiclenolist = []
    smalllist = []
    # if vehicle no search is not found then data base is shown
    for loc in tablevehiclelist:
        if len(loc['vehicle_no']) > 2:
            tablevehicle.append({'vehicleno': loc['vehicle_no']})

    for vehicle in tablevehicle:
        newv = vehicle['vehicleno']
        newv = unicode(newv).encode('ascii')
        word = re.findall(r'[A-Za-z]{1,3}\s[0-9]{0,1}\s[A-Za-z]{2,4}\s[0-9]{2,4}', newv)
        for w in word:
            if w not in vehiclenolist:
                vehiclenolist.append(w)
                smalllist.append(w.lower())
    vehiclenolist.sort()

    if request.POST:
        search = request.POST.get('location', None) or request.POST.get('query', None)
        if search.lower() in smalllist:
            queryset_list = rssdata.objects.filter(Q(vehicle_no__icontains=search)).values('location', 'date', 'death_no',
                                                                                    'injury_no', 'vehicle_no')

            latitude = []
            tabled = []
            for locations in queryset_list:
                if locations['location'] is not None:
                    if (len(locations['location']) > 2):
                        location, lat, lng = getLat(locations['location'])
                        i=0
                        while lat == None and i<5:
                            location, lat, lng = getLat(locations['location'])
                            i+=1
                        if lat is not None:
                            latitude.append(
                                    {'location': locations['location'], 'latitude': lat, 'longitude': lng, 'death': locations['death_no'],
                                     'injury': locations['injury_no'], 'date': locations['date'], 'vehicle_involved': locations['vehicle_no']})
                            context = {
                                'location_data': latitude,
                                'search': search,
                                'vehicledata': vehiclenolist,
                            }
                            return render(request, "search.html", context)
                    # if location is not present then only return the tabular value
                    else:
                        tabled.append(
                            {'location': locations['location'], 'death': locations['death_no'], 'injury': locations['injury_no'], 'date': locations['date'],
                             'vehicle_involved': locations['vehicle_no']})
                        context = {
                            'table_data': tabled,
                            'search': search,
                            'vehicledata': vehiclenolist,
                        }
                        return render(request, "search.html", context)


        else:
            context = {
                'nodetail': search,
                'vehicledata': vehiclenolist,
            }
            return render(request, "search.html", context)

    context = {
        'vehicledata': vehiclenolist,
    }
    return render(request, "search.html", context)