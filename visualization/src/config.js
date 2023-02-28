const HASH_CONFIG = window.location.hash.substring(1)
  .split('&')
  .filter(n => n)
  .map(str => str.split('='))
  .reduce((obj, tuple) => {
    obj[tuple[0]] = tuple[1];
    return obj;
  }, {});

// Which files to load on startup
export const CSV_FILES = HASH_CONFIG.files ? HASH_CONFIG.files.split(',').map(str => str.trim()) : ['reconciled_all.csv']

// Which coordinate sources to map
export const COORDINATE_SOURCES = [ 'Wikipedia', 'GeoNames', 'Pleiades', 'TM' ];

// Color by FILE or DB
export const COLOR_BY = 'FILE';
