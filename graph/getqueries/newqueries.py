from __future__ import print_function
from __future__ import division
from django.db.models import Count, Sum
from news_extraction.models import rssdata


class Query:
    def __init__(self,valueslist, ktmlocationlist,ltplocationlist,bktlocationlist):
        self.valueslist = valueslist
        self.ktmlocationlist = ktmlocationlist
        self.ltplocationlist = ltplocationlist
        self.bktlocationlist = bktlocationlist



    def getqueries(self):
        """filter database using users input to search filter and return required queryset"""

        """ import all information from database """
        allinformation = rssdata.objects.all().values('location', 'year', 'month', 'vehicleone','vehicletwo','date','vehicle_type')\
            .order_by('location').annotate(count=Count('location')).annotate(deathno=Sum('death_no')).annotate(injuryno=Sum('injury_no'))

        """list and string definition"""
        information = ''
        distinctlocations = []
        querieslist = []
        countlist = []
        filterlist = []
        alldate = []

        """take one information at a time and filter it with user input"""
        for info in self.valueslist:

            """ check for all available search query"""

            if info['locationinfo'] != '1':
                allinformation = self.location_check(info['locationinfo'])
                string = ' at ' + str(info['locationinfo'])
                information = information + string

            if info['ltplocationinfo'] != '1':
                allinformation = allinformation.filter(location=info['ltplocationinfo'].lower())
                information = information + ' in ' + info['ltplocationinfo']

            if info['ktmlocationinfo'] != '1':
                allinformation = allinformation.filter(location=info['ktmlocationinfo'].lower())
                information = information + ' in ' + info['ktmlocationinfo']

            if info['bktlocationinfo'] != '1':
                allinformation = allinformation.filter(location=info['bktlocationinfo'].lower())
                information = information + ' in ' + info['bktlocationinfo']

            if info['yearinfo'] != '1':
                allinformation = allinformation.filter(year=info['yearinfo'])
                information = information + ' in ' + str(info['yearinfo'])

            if info['monthinfo'] != '1':
                allinformation = allinformation.filter(month=info['monthinfo'])
                information = information + ' in ' + info['monthinfo']

            if info['vehicletypeinfo'] != '1':
                allinformation = allinformation.filter(vehicle_type__icontains=info['vehicletypeinfo'])
                information = information + ' by ' + info['vehicletypeinfo']

            if info['vehicletwoinfo'] != '1':
                allinformation = allinformation.filter(vehicleone=info['vehicletwoinfo']) or allinformation.filter(
                    vehicleone=info['vehicletwoinfo'])
                information = information + ' by ' + info['vehicletwoinfo']

            if info['vehiclethreeinfo'] != '1':
                allinformation = allinformation.filter(vehicleone=info['vehiclethreeinfo']) or allinformation.filter(
                    vehicleone=info['vehiclethreeinfo'])
                information = information + ' by ' + info['vehiclethreeinfo']

            if info['vehiclefourinfo'] != '1':
                allinformation = allinformation.filter(vehicleone=info['vehiclefourinfo']) or allinformation.filter(
                    vehicleone=info['vehiclefourinfo'])
                information = information + ' by ' + info['vehiclefourinfo']

            if info['dateto'] != '1':
                allinformation = allinformation.filter(date__range=(info['datefrom'], info['dateto']))



        """extract all the distincts location from query so that you can easily
         group them to find total death and injury number"""
        print(allinformation)

        for samelocation in allinformation:
            """ check if location is not null"""
            if len(samelocation['location']) > 2:
                if samelocation['location'] in distinctlocations:
                    pass
                else:
                    distinctlocations.append(samelocation['location'])
            else:
                pass


        """ now use that location name and find their death and injury"""
        for distlocation in distinctlocations:
            newqueries = allinformation.filter(location=distlocation)
            death = 0
            injury = 0
            count = 0
            for queries in newqueries:
                death += queries['deathno']
                injury += queries['injuryno']
                count += queries['count']
            querieslist.append({'location': distlocation.capitalize(), 'death': death, 'injury': injury})
            countlist.append({'location': distlocation.capitalize(), 'count': count})
            filterlist.append({'location': distlocation.capitalize(), 'death': death, 'injury': injury, 'count': count})

        """ return back"""
        return querieslist, information, len(filterlist), countlist, filterlist



    def location_check(self, location):
        """filter location . filter queryset based on location input."""

        """get all information order by location"""

        allinformation = rssdata.objects.all().values('location', 'year', 'month', 'vehicleone','vehicletwo','date','vehicle_type')\
            .order_by('location').annotate(count=Count('location')).annotate(deathno=Sum('death_no')).annotate(injuryno=Sum('injury_no'))

        """ check for kathmandu , lalitpur, bhaktapur or others"""
        if location == 'Kathmandu':
            locationlist = allinformation.filter(location="kathmandu")

            """ since kathmandu only returns accidents in kathmandu.
            so we have to individually filter all the locations of kathmandu valley privately."""
            for z in range(0, len(self.ktmlocationlist)):
                if z == 0 and len(locationlist) == 0:
                    locationlist = allinformation.filter(location=self.ltplocationlist[0]['location'].lower())
                else:
                    locationlist = allinformation.filter(
                        location=self.ktmlocationlist[z]['location'].lower())| locationlist

        elif location == 'Lalitpur':
            locationlist = allinformation.filter(location="lalitpur")
            for z in range(0, len(self.ltplocationlist)):
                if z == 0 and len(locationlist) == 0:
                    locationlist = allinformation.filter(location=self.ltplocationlist[0]['location'].lower())
                else:
                    locationlist = allinformation.filter(
                        location=self.ltplocationlist[z]['location'].lower()) | locationlist

        elif location == 'Bhaktapur':
            locationlist = allinformation.filter(location="bhaktapur")
            for z in range(0, len(self.bktlocationlist)):
                if z == 0 and len(locationlist) == 0:
                    locationlist = allinformation.filter(location=self.bktlocationlist[0]['location'].lower())
                if z > 0:
                    locationlist = allinformation.filter(
                        location=self.bktlocationlist[z]['location'].lower()) | locationlist
        else:
            locationlist = allinformation.filter(location=location.lower())
        return locationlist
