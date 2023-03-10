const HASH_CONFIG = window.location.hash.substring(1)
  .split('&')
  .filter(n => n)
  .map(str => str.split('='))
  .reduce((obj, tuple) => {
    obj[tuple[0]] = tuple[1];
    return obj;
  }, {});

// Which files to load on startup
export const CSV_FILES = 
  HASH_CONFIG.files ? HASH_CONFIG.files.split(',').map(str => str.trim()) : 
  [ 'raw_data_(machine_only).csv', 'pre_cleaned.csv', 'middle_egypt_coordinates_(manual).csv', 'upper_egypt_coordinates_(final).csv' ];
  // ['reconciled_all.csv']

// Which coordinate sources to map
export const COORDINATE_SOURCES = [ 'BM', 'Wikipedia', 'GeoNames', 'Pleiades', 'TM' ];

// Color by FILE or DB
export const COLOR_BY = 'FILE';
