import csv
from fuzzywuzzy import fuzz
import json

# GeoNames alternative names for Egypt
alt_names = {}

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
Loads the list of GeoNames alternative names for Egypt
"""
def load_names():
  with open('./EG.txt', 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
      gn_id = row[0]

      name = row[1]
      ascii_name = row[2]
      names = row[3].split(',')

      alt_names[gn_id] =  list(dict.fromkeys([ name, ascii_name ] + [s for s in names if len(s) > 0]))

"""
Loads one data file
"""
def load(system_id):
  with open('./results/batch_pre_cleaned/responses_geonames/' + system_id + '.json') as f:
    return json.load(f)

"""
Reduces the list of candidates to the most 'plausible' one, using
simple fuzzy string matching heuristics.
"""
def reduce_geonames_record(record):
  # Record top score of most similar name variant for each candidate
  top_scores = []

  # Original place name from the BM CSV
  place_name = record['record']['Place name']
  use_for = record['record']['Use For']

  for candidate in record['results']['geonames']:
    if 'countryCode' in candidate and candidate['countryCode'] != 'EG':
      top_scores.append(0)
    else:
      # All names from this candidate
      id = str(candidate['geonameId'])

      candidate_titles = [ candidate['toponymName'], candidate['name'] ]
      candidate_names = alt_names[id] if id in alt_names else []

      tokens = place_name.split() + use_for.split('~')

      top_score = 0

      for n in candidate_titles + candidate_names:
        for token in tokens:
          similarity = fuzz.token_sort_ratio(token, n)

          # similarity = fuzz.token_sort_ratio(place_name, n)

          if similarity > top_score:
            top_score = similarity

      top_scores.append(top_score)

  # Return top scoring candidate
  top_score = 0
  top_candidate = None

  for idx, s in enumerate(top_scores): 
    if s > top_score:
      top_score = s
      top_candidate = record['results']['geonames'][idx]

  if top_candidate:
    id = str(top_candidate['geonameId'])

    top_candidate['score'] = top_score
    top_candidate['alt_names'] = alt_names[id] if id in alt_names else []

  return top_candidate

"""
Script starts here!
"""

load_names()

bm_places = load_bm_places()

matches = 0
misses = 0

for row in bm_places:
  system_id = row['System ID']

  record = load(system_id)

  top_match = reduce_geonames_record(record)

  if top_match:
    matches += 1

    row['GeoNames Score'] = top_match['score']
    row['GeoNames URI'] = f'https://sws.geonames.org/{top_match["geonameId"]}'
    row['GeoNames toponymName'] = top_match['toponymName']
    row['GeoNames lat'] = float(top_match['lat'])
    row['GeoNames lng'] = float(top_match['lng'])
    row['GeoNames fcodeName'] = top_match['fcodeName']
    row['GeoNames altNames'] = '|'.join(top_match['alt_names'])
  else:
    misses += 1

with open('./results/batch_pre_cleaned/reconciled_geonames.csv', 'w') as csvfile:
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
    'GeoNames Score',
    'GeoNames URI',
    'GeoNames toponymName',
    'GeoNames lat',
    'GeoNames lng',
    'GeoNames fcodeName',
    'GeoNames altNames'
  ]

  writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
  writer.writeheader()

  for row in bm_places:
    writer.writerow(row)

print('Done.')
print('matches ' + str(matches))
print('misses ' + str(misses))
