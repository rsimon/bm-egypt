export const pointStyle = {
  'type': 'circle',
  'paint': {
    'circle-radius': [
      'interpolate', 
      ['linear'],
      ['number', ['get','point_count'], 1 ],
      0, 4, 
      10, 18
    ],
    'circle-color': '#eb585b',
    'circle-stroke-color': '#472a2d' ,
    'circle-stroke-width': 1
  }
} 