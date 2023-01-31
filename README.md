# BM Egypt

Data enrichment utilities for the BM Egyptian place vocabulary.

## GeoNames

Harvester scripts that queries the GeoNames API endpoint with the 'Place name' value,
and collects the results into a folder of JSON files. Each file contains the original 
record and all result candidates from the API. Naming convention is that the JSON
file is named after the BM System ID number <system-id>.json. There are two scripts:

- Harvester for the standard GeoNames `searchJSON` endpoint
- Harvester for the `wikipediaSearchJSON` GeoNames Wikipedia search
- Utility scripts `reconcile_geonames.py` and `reconcile_wikipedia.py` that filter the API
  responses, pick the most plausible one for each place, and produce a flat CSV result file. 

## Pleiades

Utilities to build a searchable index of Pleiades places using [Meilisearch](https://www.meilisearch.com/)
and the [Pleiades GIS data download](https://atlantides.org/downloads/pleiades/gis/).

- The setup uses data from the Pleiades `places.csv` and `names.csv`. The script `create-index-dataset.py` 
  merges the relevant data from the tables and produces a JSON dump for indexing in Meilisearch.
- Deployment of Meilisearch via a `docker-compose.yml` file. Run `docker compose up`, Meilisearch is at 
  <http://localhost:7700>. With Meilisearch running, run the `index-pleiades.py` script.
- The `harvest-pleiades-meili.py` script harvests candidate results for each place name in the BM CSV.
- Utility script `reconcile_pleiades.py` which filters the responses, picks the most plausible one
  and produces a flat CSV result file.
