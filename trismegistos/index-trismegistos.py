import csv
import requests

# Meilisearch API endpoint
MEILISEARCH_URL = 'http://localhost:7700'

# Meilisearch index UID
INDEX_UID = 'trismegistos'

# CSV file path
TRISMEGISTOS_CSV = './data/trismegistos_export_geo.csv'

"""
Load Trismegistos CSV dump
"""
def read_csv():
  with open(TRISMEGISTOS_CSV, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    data = []
        
    for row in reader:
      data.append(row)
    
    return data


data = read_csv()

for record in data:
  requests.post(f'{MEILISEARCH_URL}/indexes/{INDEX_UID}/documents', json=record)

print('Done.')