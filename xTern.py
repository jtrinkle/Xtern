# import requests
# import pandas as pd

# # Define Overpass API URL
# overpass_url = "http://overpass-api.de/api/interpreter"

# # Define query to find food trucks in the city
# query = """
# [out:json];
# area[name="Indianapolis"]->.a;
# (
#   node["amenity"="fast_food"](area.a);
#   way["amenity"="fast_food"](area.a);
# );
# out center;
# """

# # Fetch data
# response = requests.get(overpass_url, params={'data': query})
# data = response.json()



# # Extract elements from data
# elements = data['elements']

# # Prepare a list to hold our data
# food_trucks = []

# for element in elements:
#     if element['type'] == 'node':
#         latitude = element['lat']
#         longitude = element['lon']
#     elif 'center' in element:
#         latitude = element['center']['lat']
#         longitude = element['center']['lon']
#     else:
#         continue

#     # Extract other details
#     name = element['tags'].get('name', 'N/A')
#     cuisine = element['tags'].get('cuisine', 'N/A')
#     website = element['tags'].get('website', 'N/A')

#     # Add to our list
#     food_trucks.append([name, latitude, longitude, cuisine, website])

# # Convert to a DataFrame
# df = pd.DataFrame(food_trucks, columns=['Name', 'Latitude', 'Longitude', 'Cuisine', 'Website'])
# print(df)
# df.to_csv('food_trucks.csv', index=False)

# #############################################################################

import requests
import pandas as pd
import time

API_KEY = 'AIzaSyDgUEizruo-PT_Sgr8JNrmOuVS0SrG8kJs'
URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
# Indianapolis city center coordinates
INDIANAPOLIS_COORDINATES = '39.7684,-86.1581'

# Keywords to search for
KEYWORDS = ['food truck', 'street food', 'mobile food']

# Collect all results across keywords
all_results = []

for keyword in KEYWORDS:
    next_page_token = None
    
    for _ in range(3):  # Maximum of 3 pages (60 results)
        parameters = {
            'location': INDIANAPOLIS_COORDINATES,
            'radius': '5000',
            'keyword': keyword,
            'key': API_KEY
        }
        
        if next_page_token:
            parameters['pagetoken'] = next_page_token
        
        response = requests.get(URL, params=parameters)
        data = response.json()
        
        if data['status'] == 'OK':
            all_results.extend(data['results'])
            next_page_token = data.get('next_page_token')
            
            if not next_page_token:
                break
            
            # Delay to ensure the token works for the next request
            time.sleep(1)
        else:
            break




# Extract relevant data
DETAILED_URL = "https://maps.googleapis.com/maps/api/place/details/json?"

food_trucks = []
for place in all_results:
    # Make a request for detailed information
    parameters = {
        'place_id': place['place_id'],
        'key': API_KEY
    }
    response = requests.get(DETAILED_URL, params=parameters)
    detailed_data = response.json()
    
    if detailed_data['status'] == 'OK':
        place_details = detailed_data['result']
        
        name = place_details.get('name', 'N/A')
        address = place_details.get('formatted_address', 'N/A')
        rating = place_details.get('rating', 'N/A')
        website = place_details.get('website', 'N/A')
        open_hour = place_details.get('opening_hours', {}).get('weekday_text', 'N/A') if 'opening_hours' in place_details else 'N/A'
        cuisine_type = 'N/A'  # This might still be N/A unless you parse reviews or descriptions
        
        food_trucks.append([name, address, rating, website, open_hour, cuisine_type])

# Convert to DataFrame
df = pd.DataFrame(food_trucks, columns=['Name', 'Address', 'Rating', 'Website', 'Open Hour', 'Cuisine Type'])
print(df)
try:
    df.to_csv('food_trucks_indianapolis.csv', index=False)
    print("Data successfully saved to food_trucks_indianapolis.csv")
except Exception as e:
    print(f"An error occurred while saving the file: {e}")

print(data)
