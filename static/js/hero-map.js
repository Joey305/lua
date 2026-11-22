const mapCanvas = document.querySelector('#hero-map');
if (mapCanvas && window.L) {
  const office = [42.23597, -8.72023];
  const map = L.map(mapCanvas, { attributionControl: true, zoomControl: false, dragging: false, scrollWheelZoom: false, doubleClickZoom: false, touchZoom: false, keyboard: false });
  map.setView(office, 16);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '&copy; OpenStreetMap contributors' }).addTo(map);
  L.circleMarker(office, { radius: 4, color: '#16202c', weight: 1, fillColor: '#c89b7b', fillOpacity: 1, interactive: false }).addTo(map);
}
