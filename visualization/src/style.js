import chroma from 'chroma-js';

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

export const pointStyle = color => ({
  'type': 'circle',
  'paint': {
    'circle-radius': 6,
    'circle-color': color,
    'circle-stroke-color': chroma(color).darken().darken().hex(),
    'circle-stroke-width': 1
  }
})