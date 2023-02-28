import { writable } from 'svelte/store';
import Papa from 'papaparse';
import { CSV_FILES, COORDINATE_SOURCES } from './config';

/**
 * Returns the coordinates for the give source from the CSV row.
 */
const getCoordinatesForSource = (row, source) => {
  const lng = row[`${source} Lng`]?.trim();
  const lat = row[`${source} Lat`]?.trim();

  return (lng && lat) ? [ parseFloat(lng), parseFloat(lat) ] : null;
}

/**
 * Returns coordinates from any of the configured sources, in order
 * of configured priority.
 */
const getCoordinates = row =>
  COORDINATE_SOURCES.reduce((result, source) => {
    if (result) {
      // Already found - skip further searches
      return result;
    } else {
      const coordinates = getCoordinatesForSource(row, source);
      return coordinates ? { source, coordinates } : null;
    }
  }, null);

const toGeoJSON = rows => ({
  type: 'FeatureCollection',
  features: rows.map(row => {
    const result = getCoordinates(row);

    return result ? {
      id: row['System ID'],
      type: 'Feature',
      properties: {
        'Coord Source': result.source,
        ...row
      },
      geometry: {
        type: 'Point',
        coordinates: result.coordinates
      }
    } : null;
  }).filter(n => n) // Remove null
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