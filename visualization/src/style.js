import { COORDINATE_SOURCES } from './config';

export const PALETTE = [
  '#fd7f6f',
  '#7eb0d5',
  '#b2e061',
  '#bd7ebe',
  '#ffb55a',
  '#ffee65',
  '#beb9db', 
  '#fdcce5',
  '#8bd3c7'
];

const MATCH_LIST = COORDINATE_SOURCES.reduce((list, source, idx) => {
  return [...list, source, PALETTE[idx]];
}, []);

export const pointStyle = {
  'type': 'circle',
  'paint': {
    'circle-radius': 6,
    'circle-color': [ // '#eb585b',
      'match',
      ['get', 'Coord Source'],
      ...MATCH_LIST,
      '#cccccc' // fallback    
    ],
    'circle-stroke-color': '#472a2d' ,
    'circle-stroke-width': 1
  }
} 