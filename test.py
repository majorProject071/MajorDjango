import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyB0jbM6o1NAMZPhtlexx521CAj5VaQg_I4')

# Geocoding an address
geocode_result = gmaps.geocode('kathmandu')
print(geocode_result[0]['geometry']['location']['lat'])
# print(directions_result)
