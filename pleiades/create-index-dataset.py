import csv
import json

def read_csv(filename):
  with open(filename, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    data = []
        
    for row in reader:
      data.append(row)
    
    return data

places = read_csv('./data/places.csv')
names = read_csv('./data/names.csv')

records = []

print('Joining tables...')

for row in places:
  id = row['id']
  uri = row['uri']

  title = row['title']
  description = row['description']

  lat = row['representative_latitude']
  lon = row['representative_longitude']

  name_rows = [ n for n in names if n['place_id'] == id]

  alt_names = []

  for n in name_rows:
    fields = [
      n['attested_form'],
      n['romanized_form_1'],
      n['romanized_form_2'],
      n['romanized_form_3']
    ]

    alt_names += [n for n in fields if len(n) > 0]

  # Remove duplicates
  alt_names = list(dict.fromkeys(alt_names))

  records.append({
    'id': id,
    'uri': uri,
    'title': title,
    'description': description,
    'lat': lat,
    'lon': lon,
    'names': alt_names
  })

print('Writing JSON')

with open(f'./data/pleiades_joined.json', 'w') as file:
  json.dump(records, file, indent = 2)

print('Done.')
