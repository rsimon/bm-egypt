import csv
from fuzzywuzzy import fuzz
import json

"""
Reads BM places CSV
"""
def load_bm_places():
  with open('../BM_place_terms_egypt.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    data = []
        
    for row in reader:
      data.append(row)
    
    return data

"""
Loads one data file
"""
def load(system_id):
  with open('./results/responses_wikipedia/' + system_id + '.json') as f:
    return json.load(f)

def is_in_bounds(record):
  min_lat = 21.62
  min_lon = 24.70
  max_lat = 31.76
  max_lon = 34.97

  lat = record['lat'] if 'lat' in record else None
  lon = record['lng'] if 'lng' in record else None

  if lat and lon:
    return lat >= min_lat and lat <= max_lat and lon >= min_lon and lon <= max_lon
  else:
    return True

"""
Reduces the list of candidates to the most 'plausible' one, using
simple fuzzy string matching heuristics.
"""
def reduce_wikipedia_record(record):
  # Record top score of most similar name variant for each candidate
  top_scores = []

  for candidate in record['results']['geonames']:
    # Original place name from the BM CSV
    if 'countryCode' in candidate and candidate['countryCode'] != 'EG':
      top_scores.append(0)
    elif not is_in_bounds(candidate):
      top_scores.append(0)
    else:
      place_name = record['record']['Place name']

      title = candidate['title']
      summary = candidate['summary'] if 'summary' in candidate else ''

      # Compute a score for each candidate: title ratio via fuzzwuzzy *
      # ratio of exact mentions in summary

      title_similarity = fuzz.token_sort_ratio(place_name, title) 

      summary_mentions = summary.count(place_name)
      summary_ratio = (len(place_name) * summary_mentions / len(summary)) if len(summary) > 0 else 0

      top_scores.append(title_similarity + summary_ratio)

  # Return top scoring candidate
  top_score = 0
  top_candidate = None

  for idx, s in enumerate(top_scores): 
    if s > top_score:
      top_score = s
      top_candidate = record['results']['geonames'][idx]

  if top_candidate and top_score > 48:
    top_candidate['score'] = top_score
    return top_candidate
  else:
    return None

"""
Script starts here!
"""

bm_places = load_bm_places()

matches = 0
misses = 0

for row in bm_places:
  system_id = row['System ID']

  record = load(system_id)

  top_match = reduce_wikipedia_record(record)

  if top_match:
    matches += 1

    row['Wikipedia Score'] = round(top_match['score'])
    row['Wikipedia URI'] = top_match['wikipediaUrl']
    row['Wikipedia Title'] = top_match['title']
    row['Wikipedia Lat'] = float(top_match['lat'])
    row['Wikipedia Lng'] = float(top_match['lng'])
    row['Wikipedia Summary'] = top_match['summary'] if 'summary' in top_match else ''
    row['Wikipedia Feature'] = top_match['feature'] if 'feature' in top_match else ''
  else:
    misses += 1

with open('./results/reconciled_wikipedia.csv', 'w') as csvfile:
  csv_columns = [
    'System ID',
    'Place name',
    'Discriminator',
    'Place name type',
    'Place type',
    'Broader Terms',
    'Display Term',
    'Use For',
    'Related Terms',
    'Scope Note',
    'Wikipedia Score',
    'Wikipedia URI',
    'Wikipedia Title',
    'Wikipedia Lat',
    'Wikipedia Lng',
    'Wikipedia Summary',
    'Wikipedia Feature'
  ]

  writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
  writer.writeheader()

  for row in bm_places:
    writer.writerow(row)

print('Done.')
print('matches ' + str(matches))
print('misses ' + str(misses))
