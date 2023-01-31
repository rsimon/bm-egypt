import csv
import json
import requests
import urllib.parse
import time

CSV_PATH = '../BM_place_terms_egypt.csv'

# SOURCE = 'GEONAMES'
SOURCE = 'WIKIPEDIA'

"""
Reads BM places CSV
"""
def read_csv():
  with open(CSV_PATH, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    data = []
        
    for row in reader:
      data.append(row)
    
    return data

"""
Queries GeoNames API (endpoint configurable - searchJSON or wikipediaSearchJSON)
"""
def search_geonames(query, endpoint):
  q_escaped = urllib.parse.quote(query)

  url = f'http://api.geonames.org/{endpoint}?q={q_escaped}&countryBias=EG&username=aboutgeo'
  response = requests.get(url)

  if response.status_code == 200:
    return response.json()
  else:
    print('Error')

"""
Script starts here!
"""
records = read_csv()

for record in records:
  system_id = record['System ID'] 
  place_name = record['Place name']

  endpoint = 'searchJSON' if SOURCE == 'GEONAMES' else 'wikipediaSearchJSON'

  results = search_geonames(place_name, endpoint)

  with open(f'./results/responses_{SOURCE.lower()}/{system_id}.json', 'w') as file:
    merged = {
      'query': place_name,
      'record': record,
      'results': results
    }

    json.dump(merged, file, indent = 2)

  time.sleep(0.25)

print('Done.')