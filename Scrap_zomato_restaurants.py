from __future__ import print_function
from re import sub
from urllib.error import URLError
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import csv
import requests
import re

headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get("https://www.zomato.com/delivery-cities",headers=headers)
response_obj= response.content.decode('utf8')
soup = BeautifulSoup(response.text, "html.parser")

script = soup.findAll('script')[9]
json_script= script.text.replace("\\", "")
json_script= json_script.replace('window.__PRELOADED_STATE__ = JSON.parse("', "").rstrip()[:-3]

try:
    json_data= json.loads(json_script)
except ValueError as e:
    print("Json is not valid...")

pages_obj = json_data.get("pages",{})
cities_array= pages_obj['deliverycities']['allO2Cities']

# fetching top restaurants from all cities
for city in cities_array:
    url = city['url']
    print("Fetching City: ", url)
    URL= url + "top-restaurants"
    city_name = city['name']
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL,headers=headers)
    response_obj= response.content.decode('utf8')
    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.findAll('script')[12]
    json_script= script.text.replace("\\", "")
    json_script= json_script.replace('window.__PRELOADED_STATE__ = JSON.parse("', "").rstrip()[:-3]
    try:
        json_data= json.loads(json_script)
    except ValueError as e:
        print("Json is not valid...")
    restaurant_array = json_data['pages']['collectionDetails']["1"]['SECTION_ENTITIES_DATA']
    restaurant_data = []
    for restaurant in restaurant_array:
        restaurent_details={}
        name = restaurant['name']
        print("Fetching Restaurant: ", name)
        address= restaurant['subtitleData']['locality']['text']
        rating= restaurant['rating']['aggregate_rating']
        cuisines= restaurant['subtitleData']['cuisines']
        cuisines_data = []
        if(cuisines != None):
            for cuisine in cuisines:
                cuisine_name = cuisine['name']
                cuisines_data.append(cuisine_name)

        restaurent_details['Restaurent Name'] = name
        restaurent_details['Restaurent Address'] = address
        restaurent_details['Restaurant Rating']= rating
        restaurent_details['Restaurant Cuisines']= cuisines_data
        restaurant_data.append(restaurent_details)
    jsonstr= json.dumps(restaurant_data)
# Save restaurants according city
    with open('/Users/poonamdhankher/Downloads/test/Task_folder/Zomato_folder/' + city_name + '_Zomato.restaurants.json', 'w') as f:
        print(jsonstr, file=f)

# Save restaurant information in single file
# with open('/Users/poonamdhankher/Downloads/test/Task_folder/Zomato.restaurants.details.json', 'a+') as f:
#     print(jsonstr, file=f)








































































































