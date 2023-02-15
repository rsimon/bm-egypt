import csv
from fuzzywuzzy import fuzz
import json

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

def get_coords(record):
  coords = record['coordinates;'][:-1]
  coords = coords.split(',') if len(coords) > 0 else None

  if coords != None:
    coords = [ float(x) for x in coords ]

  return coords

def is_in_bounds(record):
  min_lat = 21.62
  min_lon = 24.70
  max_lat = 31.76
  max_lon = 34.97

  coords = get_coords(record)

  if coords != None:
    lat = coords[0] 
    lon = coords[1]
  
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
    if candidate['country'] != 'Egypt':
      top_scores.append(0)
    elif not is_in_bounds(candidate):
      top_scores.append(0)
    else:
      # Original place name from the BM CSV
      place_name = record['record']['Place name']

      # All names from this candidate
      name_latin = candidate['name_latin']
      name_standard = candidate['name_standard']

      names = [ n for n in [ name_latin, name_standard ] if len(n) > 0 ]
      
      # These are descriptions rather than names
      full_name = candidate['full_name']
      location = candidate['location']

      top_score = 0

      for n in names:
        similarity = fuzz.token_sort_ratio(place_name, n) / 100

        if similarity > top_score:
          top_score = similarity

      if place_name in full_name:
        top_score *= 2 # Boost!

      if place_name in location:
        top_score *= 2 # Boost!

      top_scores.append(round(min(100, 50 * top_score)))

  # Return top scoring candidate
  top_score = 0
  top_candidate = None

  for idx, s in enumerate(top_scores): 
    if s > top_score:
      top_score = s
      top_candidate = record['results']['hits'][idx]

  if top_candidate and top_score >= 40:
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

    row['TM Score'] = top_match['score']
    row['TM URI'] = 'https://www.trismegistos.org/place/' + top_match['id']
    row['TM Standard Name'] = top_match['name_standard']
    row['TM Full Name'] = top_match['full_name']

    coords = get_coords(top_match)

    if coords != None:
      row['TM Lat'] = coords[0]
      row['TM Lng'] = coords[1]
  else:
    misses += 1

with open('./results/reconciled_trismegistos_pre_cleaned.csv', 'w') as csvfile:
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
    'TM Score',
    'TM URI',
    'TM Standard Name',
    'TM Full Name',
    'TM Lat',
    'TM Lng'
  ]

  writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
  writer.writeheader()

  for row in bm_places:
    writer.writerow(row)

print('Done.')
print('matches ' + str(matches))
print('misses ' + str(misses))
