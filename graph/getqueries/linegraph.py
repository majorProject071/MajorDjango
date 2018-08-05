from __future__ import print_function
from __future__ import division
from django.db.models import Count, Sum
from news_extraction.models import rssdata
from news_extraction.modules.location_tree import LocationInformation
import operator


class Graph:
    def __init__(self, districtlist):
        self.district = districtlist

    def linequery(self):
        yearlistdata = rssdata.objects.values('year').order_by('year').annotate(count=Count('year'))
        linelistquery = []
        for query in yearlistdata:
            linelistquery.append({'year': query['year'], 'value': query['count']})
        yearlast = linelistquery[0]['year']
        return linelistquery, yearlast

    def districtquery(self):
        ktm_location = LocationInformation().all_ktm_locations()
        bkt_location = LocationInformation().all_bkt_locations()
        ltp_location = LocationInformation().all_ltp_locations()
        outside_location = LocationInformation().all_locations()
        yearlistdata = rssdata.objects.values('location', 'year').order_by('year').annotate(count=Count('year'))
        linelistquery = []
        years = []
        for listdata in yearlistdata:
            if listdata['year'] not in years:
                years.append(listdata['year'])
        yearlast = years[0]
        ktmvalley = ['kathmandu', 'lalitpur','bhaktapur']
        for year in years:
            ktm_count = 0
            ltp_count = 0
            bkt_count = 0
            locationdata = yearlistdata.filter(year=year)
            for listdata in locationdata:
                if listdata['location'] in ktm_location or listdata['location'] == 'kathmandu':
                    ktm_count += listdata['count']
                elif listdata['location'] in ltp_location or listdata['location'] == 'lalitpur':
                    ltp_count += listdata['count']
                elif listdata['location'] in bkt_location or listdata['location'] == 'bhaktapur':
                    bkt_count += listdata['count']
                else:
                    linelistquery.append({'year': year, 'value': listdata['count'], 'location': listdata['location']})

            linelistquery.append({'year': year, 'value': bkt_count,'location': 'bhaktapur'})
            linelistquery.append({'year': year, 'value': ktm_count, 'location': 'kathmandu'})
            linelistquery.append({'year': year, 'value': ltp_count, 'location': 'lalitpur'})


        yearlist = []
        listquery = []
        for location in linelistquery:
            if location['location'] == self.district.lower():
                yearlist.append(location['year'])
                listquery.append({ 'year': location['year'], 'value': location['value']})
        for item in years:
            if item not in yearlist:
                listquery.append({ 'year': item , 'value': 0})

        nb = sorted(listquery, key=lambda k: int(k['year']))

        return nb, yearlast
        #         listquery.append({'year':location['year'], 'value': location['value']})
        # return listquery, yearlast