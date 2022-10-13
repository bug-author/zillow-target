import requests
from bs4 import BeautifulSoup

url = 'https://www.zillow.com/homedetails/504-Lexington-Ct-Carbondale-IL-62901/105612960_zpid'

req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

with requests.Session() as s:
    r = s.get(url, headers=req_headers)

soup = BeautifulSoup(r.content, 'lxml')

title = soup.find('title')

address = title.text.split(' |')[0]

import json
 
data = {
    "address": address,
    "url": url    
}

with open("zillow_data.json", "w") as outfile:
    json.dump(data, outfile)

"""## Get Coords"""

# !pip install geopy

from geopy.geocoders import Nominatim

geolocator = Nominatim()

location = geolocator.geocode(data["address"])

_, coords = location

# Here API
# https://discover.search.hereapi.com/v1/discover
# ?at=37.733348761581105,-89.25503994058744
# &q=Target
# &apikey=
# &limit=5

API_KEY = ""
URL = f"https://discover.search.hereapi.com/v1/discover?at=37.733348761581105,-89.25503994058744&q=Target&apikey={API_KEY}"

r = requests.get(URL)

for item in r.json()['items']:
  print(item['address']['label'], item['distance'])
  print('\n')

meters_to_miles = 0.000621371

import json 

with open('./zillow_data.json', 'r') as inFile:
  data = json.load(inFile)

target_match = {}
  
# api-call
# filter addresses withing threshold miles (20)

for item in r.json()['items']:
  miles = meters_to_miles * int(item['distance'])

  if miles <= 20:
    target_match[item['address']['label']] = 'yes'
  else:
    target_match[item['address']['label']] = 'no'
  
data['match'] = target_match

with open('./zillow_data.json', 'w') as outFile:
  json.dump(data, outFile)

with open('./zillow_data.json', 'a+', encoding='utf-8') as in_json:
 
    # Reading from json file
    json_object = json.load(in_json)
