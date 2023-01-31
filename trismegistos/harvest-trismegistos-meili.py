import csv
import json
import requests
import urllib.parse
import time

CSV_PATH = '../BM_place_terms_egypt.csv'

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
Queries Meilisearch
"""
def search_meilisearch(query):
  q_escaped = urllib.parse.quote(query)

  url = f'http://localhost:7700/indexes/trismegistos/search?q={q_escaped}&hitsPerPage=100'
  response = requests.get(url)

  if response.status_code == 200:
    return response.json()
  else:
    print('Error')

records = read_csv()

"""
Script starts here!
"""
for record in records:
  system_id = record['System ID'] 
  place_name = record['Place name']

  discriminator = record['Discriminator']

  query = record['Place name'] + ' ' + discriminator if len(discriminator) > 0 else record['Place name']
  
  results = search_meilisearch(query)

  with open(f'./results/responses/{system_id}.json', 'w') as file:
    merged = {
      'query': query,
      'record': record,
      'results': results
    }

    json.dump(merged, file, indent = 2)

  time.sleep(0.1)

print('Done.')