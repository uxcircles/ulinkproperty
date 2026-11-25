/* ULINK map: MapLibre + OpenFreeMap vector tiles in the site palette; the pin is the price tag. */
(() => {
  const C = {
    land: '#f2efe8', building: '#e4dfd4', buildingLine: '#d3ccbe', park: '#d9e6dc', water: '#c9d9e3',
    road: '#ffffff', roadCase: '#dcd6ca', major: '#ffffff', majorCase: '#c8b8a8', rail: '#9aa5a0',
    label: '#17191c', labelSoft: '#4c5157', halo: '#f2efe8',
  };
  const name = ['coalesce', ['get', 'name:en'], ['get', 'name_en'], ['get', 'name']];
  const width = (a, b, c) => ['interpolate', ['exponential', 1.6], ['zoom'], 13, a, 16, b, 18, c];
  const major = ['match', ['get', 'class'], ['motorway', 'trunk', 'primary', 'secondary'], true, false];
  const minor = ['match', ['get', 'class'], ['tertiary', 'minor', 'service', 'street', 'residential'], true, false];
  const style = {
    version: 8,
    glyphs: 'https://tiles.openfreemap.org/fonts/{fontstack}/{range}.pbf',
    sources: { omt: { type: 'vector', url: 'https://tiles.openfreemap.org/planet' } },
    layers: [
      { id: 'land', type: 'background', paint: { 'background-color': C.land } },
      { id: 'park', type: 'fill', source: 'omt', 'source-layer': 'park', paint: { 'fill-color': C.park } },
      { id: 'green', type: 'fill', source: 'omt', 'source-layer': 'landuse', filter: ['match', ['get', 'class'], ['park', 'grass', 'cemetery', 'pitch', 'playground', 'stadium'], true, false], paint: { 'fill-color': C.park } },
      { id: 'water', type: 'fill', source: 'omt', 'source-layer': 'water', paint: { 'fill-color': C.water } },
      { id: 'building', type: 'fill', source: 'omt', 'source-layer': 'building', minzoom: 13, paint: { 'fill-color': C.building, 'fill-outline-color': C.buildingLine } },
      { id: 'rail', type: 'line', source: 'omt', 'source-layer': 'transportation', filter: ['match', ['get', 'class'], ['rail', 'transit'], true, false], paint: { 'line-color': C.rail, 'line-width': 1.4, 'line-dasharray': [3, 2] } },
      { id: 'road-case', type: 'line', source: 'omt', 'source-layer': 'transportation', filter: minor, layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': C.roadCase, 'line-width': width(1.5, 6, 20) } },
      { id: 'major-case', type: 'line', source: 'omt', 'source-layer': 'transportation', filter: major, layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': C.majorCase, 'line-width': width(3, 10, 30) } },
      { id: 'road', type: 'line', source: 'omt', 'source-layer': 'transportation', filter: minor, layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': C.road, 'line-width': width(1, 4.5, 17) } },
      { id: 'major', type: 'line', source: 'omt', 'source-layer': 'transportation', filter: major, layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': C.major, 'line-width': width(2, 8, 27) } },
      { id: 'road-label', type: 'symbol', source: 'omt', 'source-layer': 'transportation_name', minzoom: 14, layout: { 'symbol-placement': 'line', 'text-field': name, 'text-font': ['Noto Sans Regular'], 'text-size': 12 }, paint: { 'text-color': C.labelSoft, 'text-halo-color': C.halo, 'text-halo-width': 1.4 } },
      { id: 'area-label', type: 'symbol', source: 'omt', 'source-layer': 'place', filter: ['match', ['get', 'class'], ['suburb', 'quarter', 'neighbourhood'], true, false], layout: { 'text-field': ['upcase', name], 'text-font': ['Noto Sans Bold'], 'text-size': 11, 'text-letter-spacing': 0.18 }, paint: { 'text-color': C.labelSoft, 'text-halo-color': C.halo, 'text-halo-width': 1.4 } },
    ],
  };
  const el = (html, cls) => { const d = document.createElement('div'); d.className = cls; d.innerHTML = html; return d; };

  window.ulMap = (box, root) => {
    const data = JSON.parse(document.getElementById('map-data').textContent);
    const { maplibregl } = window;
    const holder = document.createElement('div');
    holder.className = 'mapbox';
    box.appendChild(holder);
    const phone = window.matchMedia('(max-width: 760px)').matches;
    const map = new maplibregl.Map({ container: holder, style, center: data.home, zoom: 15, maxZoom: 18, minZoom: 11, dragRotate: false, pitchWithRotate: false, cooperativeGestures: true, attributionControl: { compact: true } });
    map.touchZoomRotate.disableRotation();
    if (!phone) map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-left');
    const bounds = new maplibregl.LngLatBounds(data.home, data.home);
    data.places.forEach((p) => bounds.extend(p.at));
    const fit = () => map.fitBounds(bounds, { padding: phone ? 70 : 110, duration: 0, maxZoom: 16 });
    fit();
    let touched = false;
    map.on('dragstart', () => { touched = true; });
    map.on('zoomstart', (e) => { if (e.originalEvent) touched = true; });
    window.addEventListener('resize', () => { if (!touched) fit(); });
    data.places.forEach((p) => new maplibregl.Marker({ element: el(`<span class="map-place">${p.name}</span>`, 'map-pl'), anchor: 'center' }).setLngLat(p.at).addTo(map));
    new maplibregl.Marker({ element: el(`<img src="${root}assets/img/favicon.svg" alt=""><span class="pin-label">${data.label}</span>`, 'map-pin'), anchor: 'top', offset: [0, -17] }).setLngLat(data.home).addTo(map);
    if (phone) map.on('load', () => holder.querySelectorAll('.maplibregl-compact-show').forEach((a) => a.classList.remove('maplibregl-compact-show')));
    return map;
  };
})();
