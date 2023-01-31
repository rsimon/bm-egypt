import json
import requests

# Meilisearch API endpoint
MEILISEARCH_URL = 'http://localhost:7700'

# Meilisearch index UID
INDEX_UID = 'pleiades'

# CSV file path
JSON_FILE = './pleiades_joined.json'

# Open the CSV file
with open(JSON_FILE, 'r') as file:
  data = json.load(file)

  # Create a Meilisearch index, if it doesn't already exist
  requests.post(f'{MEILISEARCH_URL}/indexes', json={ 'uid': INDEX_UID })

  print('Indexing...')

  for place in data:
    requests.post(f'{MEILISEARCH_URL}/indexes/{INDEX_UID}/documents', json=place)

print('Done.')