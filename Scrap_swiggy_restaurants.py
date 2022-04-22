import requests
import json
from bs4 import BeautifulSoup
from re import sub
import re
import time
from urllib.request import urlopen


def getRestaurantsByOffset(offset):
    print("Getting Restaurants: ",offset)
    response = requests.get("https://www.swiggy.com/dapi/restaurants/list/v5?lat=28.41024565252829&lng=77.03608687967062&offset=" + str(offset) + "&sortBy=RELEVANCE&pageType=SEE_ALL&page_type=DESKTOP_SEE_ALL_LISTING")
    json_data= response.json()
    # print(json_data)
    try:
        restaurants_array = json_data['data']['cards']
    except:
        return
    if(restaurants_array == None or len(restaurants_array) == 0):
        return

    restaurents_data = []
    for restaurent in restaurants_array:
        restaurent_details = {}
        details = restaurent['data']['data']
        name = details['name']
        address = details['address']
        cuisines= details['cuisines']
        rating= details['avgRating']
        restaurent_details['Restaurent Name'] = name
        restaurent_details['Restaurent Address'] = address
        restaurent_details['Restaurent Cuisines'] = cuisines
        restaurent_details['Restaurent Rating'] = rating
        restaurents_data.append(restaurent_details)

    jsonstr= json.dumps(restaurents_data)
    print("Saving: ",'restaurents_page_offset'+ str(offset) + '.json')
# Saving details according pages
    # with open('/Users/poonamdhankher/Downloads/test/Task_folder/swiggy_data/Swigggy_restaurents_page_offset'+ str(offset) + '.json', 'a+') as f:
    #     print(jsonstr, file=f)

    offset += 15
    getRestaurantsByOffset(offset)
    
offset = 0
swiggy_data = []
getRestaurantsByOffset(offset)
print("SAVIND DATA ......................")
jsonstr= json.dumps(swiggy_data)
with open('/Users/poonamdhankher/Downloads/test/Task_folder/Swigggy_restaurents_data.json', 'w') as f:
        print(jsonstr, file=f)










