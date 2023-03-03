<script>
  import { onMount, onDestroy } from 'svelte';
  import { Map, NavigationControl, Popup } from 'maplibre-gl';
  import Legend from './LegendDatasets.svelte';
  import { store } from './store';
  import { PALETTE, pointStyle } from './style';

  import 'maplibre-gl/dist/maplibre-gl.css';

	let map;

	let container;

	const API_KEY = import.meta.env.VITE_API_KEY;

	const STYLE = `https://api.maptiler.com/maps/outdoor/style.json?key=${API_KEY}`;

	const DEFAULT_LON = 31.0;
  const DEFAULT_LAT = 26.5;
  const DEFAULT_ZOOM = 5;

  const addData = () => {
    Object.entries($store).forEach(([name, data], idx) => {      
      map.addSource(`source-${name}`, {
        type: 'geojson', data
      });

      const color = PALETTE[idx];

      map.addLayer({
        ...pointStyle(color),
        id: name,
        source: `source-${name}`,
        layout: {
          visibility: 'visible'
        }
      });
    });
  }

  const onClick = evt => {
    const features = map.queryRenderedFeatures(evt.point)
      .filter(f => f.layer.id.startsWith('data-'));
    
    if (features.length > 0) {
      const { properties } = features[0];

      const rows = Object.entries(properties).reduce((rows, [key, value]) => {
        const html = value.startsWith('http') ? `<a href="${value}" target="_blank">${value}</a>` : value;
        return rows + `<tr><td>${key}</td><td>${html}</td></tr>`; 
      }, '');
      
      new Popup()
        .setLngLat(evt.lngLat)
        .setHTML(`<table><tbody>${rows}</tbody></table>`)
        .addTo(map);
    }
  }

  const onChangeLayer = ({ detail }) => {
    const { layer, visible } = detail;
    map.setLayoutProperty(layer, 'visibility', visible ? 'visible' : 'none');
  }

  onMount(() => {
    map = new Map({
      container,
      style: STYLE,
      center: [ DEFAULT_LON, DEFAULT_LAT ],
      zoom: DEFAULT_ZOOM
    });

    map.addControl(new NavigationControl(), 'top-right');

    map.on('load', addData);

    map.on('click', onClick);
  });

  onDestroy(() => map.remove());

  $: Object.entries($store).forEach(([name, data]) => map?.getSource(`source-${name}`)?.setData(data));
</script>

<div class="map" bind:this={container} />
  
<Legend on:change={onChangeLayer} />

<style>
  .map {
    width: 100%;
    height: 100%;
  }

  :global(.maplibregl-popup-content.mapboxgl-popup-content) {
    max-height: 70vh;
    width: 500px;
    overflow-y: scroll;
    padding: 0;
    box-shadow: 2px 2px 24px 0 rgba(0, 0, 0, 0.25);
    position: relative;
  }

  :global(.maplibregl-popup-content.mapboxgl-popup-content table) {
    border-collapse: collapse;
    width: 100%;
  }

  :global(.maplibregl-popup-content.mapboxgl-popup-content td:first-child) {
    font-weight: 600;
  }

  :global(.maplibregl-popup-content.mapboxgl-popup-content td) {
    padding: 5px;
  }

  :global(.maplibregl-popup-content.mapboxgl-popup-content tr:nth-child(even) td) {
    background-color: rgba(0, 0, 0, 0.08);
  }
</style>