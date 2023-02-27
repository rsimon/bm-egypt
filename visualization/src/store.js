import { writable } from 'svelte/store';
import Papa from 'papaparse';
import { CSV_FILES } from './config';

const hasCoordinates = row =>
  row['GeoNames lng'] && row['GeoNames lat'];

const toGeoJSON = rows => ({
  type: 'FeatureCollection',
  features: rows.filter(hasCoordinates).map(row => ({
    id: row['System ID'],
    type: 'Feature',
    properties: {
      ...row
    },
    geometry: {
      type: 'Point',
      coordinates: [
        parseFloat(row['GeoNames lng']),
        parseFloat(row['GeoNames lat']) 
      ]
    }
  }))
});

const createStore = () => {

	const { subscribe, update } = writable([]);

  CSV_FILES.forEach(f => {
    Papa.parse(f, {
      download: true,
      header: true,
      complete: function(results) {
        update(layers => [...layers, toGeoJSON(results.data) ]);
      }
    })
  });

	return {
		subscribe
	};
}

export const store = createStore();