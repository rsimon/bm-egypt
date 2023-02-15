import csv
from fuzzywuzzy import fuzz
import json
import os

"""
Reads BM places CSV
"""
def load_bm_places():
  # with open('../BM_place_terms_egypt.csv', newline='', encoding='utf-8') as file:
  with open('../BM_pre_cleaned_terms_upper_egypt.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    data = []
        
    for row in reader:
      data.append(row)
    
    return data

"""
Loads one data file
"""
def load(system_id):
  with open('./results/responses_pre_cleaned/' + system_id + '.json') as f:
    return json.load(f)

def is_in_bounds(record):
  min_lat = 21.62
  min_lon = 24.70
  max_lat = 31.76
  max_lon = 34.97

  lat = float(record['lat']) if ('lat' in record and len(record['lat']) > 0) else None
  lon = float(record['lon']) if ('lon' in record and len(record['lon']) > 0) else None

  if lat and lon:
    return lat >= min_lat and lat <= max_lat and lon >= min_lon and lon <= max_lon
  else:
    return True

"""
Reduces the list of candidates to the most 'plausible' one, using
simple fuzzy string matching heuristics.
"""
def reduce_pleiades_record(record):
  # Record top score of most similar name variant for each candidate
  top_scores = []

  for candidate in record['results']['hits']:
    if is_in_bounds(candidate):
      # Original place name from the BM CSV
      place_name = record['record']['Place name']

      # All names from this candidate
      title = candidate['title']
      names = candidate['names']

      top_score = 0

      for n in names:
        similarity = fuzz.token_sort_ratio(place_name, n) / 100

        if similarity > top_score:
          top_score = similarity

      # "Boost" title, by multiplying the title similarity with the highest scoring name
      top_score = top_score * fuzz.token_sort_ratio(place_name, title)

      if place_name in candidate['description']:
        top_score *= 2 # Boost!

      top_scores.append(round(min(100, top_score)))
    else:
      top_scores.append(0)

  # Return top scoring candidate
  top_score = 0
  top_candidate = None

  for idx, s in enumerate(top_scores): 
    if s > top_score:
      top_score = s
      top_candidate = record['results']['hits'][idx]

  if top_candidate and top_score >= 60:
    top_candidate['score'] = top_score
    return top_candidate

"""
Script starts here!
"""

bm_places = load_bm_places()

matches = 0
misses = 0

for row in bm_places:
  system_id = row['System ID']

  record = load(system_id)

  top_match = reduce_pleiades_record(record)

  if top_match:
    matches += 1

    row['Pleiades Score'] = top_match['score']
    row['Pleiades URI'] = top_match['uri']
    row['Pleiades Title'] = top_match['title']
    row['Pleiades Lat'] = float(top_match['lat']) if len(top_match['lat']) > 0 else ''
    row['Pleiades Lng'] = float(top_match['lon']) if len(top_match['lon']) > 0 else ''
    row['Pleiades Description'] = top_match['description']
    row['Pleiades Names'] = '|'.join(top_match['names'])
  else:
    misses += 1

with open('./results/reconciled_pleiades_pre_cleaned.csv', 'w') as csvfile:
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
    'Pleiades Score',
    'Pleiades URI',
    'Pleiades Title',
    'Pleiades Lat',
    'Pleiades Lng',
    'Pleiades Description',
    'Pleiades Names'
  ]

  writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
  writer.writeheader()

  for row in bm_places:
    writer.writerow(row)

print('Done.')
print('matches ' + str(matches))
print('misses ' + str(misses))
