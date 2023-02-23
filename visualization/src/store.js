import { writable } from 'svelte/store';
import Papa from 'papaparse';

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
})

const EMPTY_GEOJSON = {
  type: 'FeatureCollection',
  features: []
};

const createStore = () => {

	const { subscribe, set } = writable(EMPTY_GEOJSON);

  Papa.parse('reconciled_all.csv', {
    download: true,
    header: true,
    complete: function(results) {
      set(toGeoJSON(results.data));
    }
  });

	return {
		subscribe
	};
}

export const store = createStore();