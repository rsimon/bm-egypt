import csv 

PATH_BM_PLACES = './BM_place_terms_egypt.csv'
PATH_GEONAMES  = './geonames/results/reconciled_geonames.csv'
PATH_WIKIPEDIA = './geonames/results/reconciled_wikipedia.csv'
PATH_PLEIADES  = './pleiades/results/reconciled_pleiades.csv'

"""
Reads a CSV file
"""
def read_csv(path):
  with open(path, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    data = []
        
    for row in reader:
      data.append(row)
    
    return data

bm_places = read_csv(PATH_BM_PLACES)

results_gn = read_csv(PATH_GEONAMES)
results_wp = read_csv(PATH_WIKIPEDIA)
results_pl = read_csv(PATH_PLEIADES)

"""
Script starts here!
"""

total = 0
complete_misses = 0

for idx, row in enumerate(bm_places):
  total += 1

  row_gn = results_gn[idx]
  row_wp = results_wp[idx]
  row_pl = results_pl[idx]

  row.update(row_gn)
  row.update(row_wp)
  row.update(row_pl)

  no_gn = len(row['GeoNames URI'].strip()) == 0
  no_wp = len(row['Wikipedia URI'].strip()) == 0
  no_pl = len(row['Pleiades URI'].strip()) == 0

  if no_gn and no_wp and no_pl:
    complete_misses += 1

# Log stats
print('Total rows: ' + str(total))
print('Misses: ' + str(complete_misses))

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
  'GeoNames altNames',
  'Wikipedia Score',
  'Wikipedia URI',
  'Wikipedia Title',
  'Wikipedia Lat',
  'Wikipedia Lng',
  'Wikipedia Summary',
  'Wikipedia Feature',
  'Pleiades Score',
  'Pleiades URI',
  'Pleiades Title',
  'Pleiades Lat',
  'Pleiades Lng',
  'Pleiades Description',
  'Pleiades Names'
]

with open('./reconciled_all.csv', 'w') as csvfile:
  writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
  writer.writeheader()

  for row in bm_places:
    writer.writerow(row)

