<script>
  import { onMount, onDestroy } from 'svelte';
  import { Map, NavigationControl } from 'maplibre-gl';

  import 'maplibre-gl/dist/maplibre-gl.css';

	let map;

	let container;

	const API_KEY = import.meta.env.VITE_API_KEY;

	const STYLE = `https://api.maptiler.com/maps/outdoor/style.json?key=${API_KEY}`;

	const DEFAULT_LON = 17.0
  const DEFAULT_LAT = 41.5
  const DEFAULT_ZOOM = 6

  onMount(() => {
    map = new Map({
      container,
      style: STYLE,
      center: [ DEFAULT_LON, DEFAULT_LAT ],
      zoom: DEFAULT_ZOOM
    });

    map.addControl(new NavigationControl(), 'top-right');
  });

  onDestroy(() => map.remove());
</script>

<div class="map" bind:this={container}>

</div>

<style>
  .map {
    width: 100%;
    height: 100%;
  }
</style>