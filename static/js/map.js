const mymap = L.map('CovidMap').setView([10.968638, -74.806644,], 14);
const attribution =
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

var customIcon = new L.Icon({
    iconUrl: '/static/png/masca.png',
    iconSize: [30, 30],
    iconAnchor: [15, 15]
});

const tiles = L.tileLayer(tileUrl, { attribution });
tiles.addTo(mymap);
var search, estado
search = document.getElementById('buscar').value 
estado = document.getElementById('estado').value 


const http = new XMLHttpRequest() // metodo de javascript, para hacer peticiones a una url
    http.open('GET', "/ubic?param1=" + search)
    http.onreadystatechange = () => {
        if (http.readyState == 4 && http.status == 200) {
            var coords = JSON.parse(http.responseText);
            casa = L.marker([coords[0][2], coords[0][3]], { icon: customIcon }).addTo(mymap).bindPopup('Trabajo').openPopup();
            trabajo = L.marker([coords[0][0], coords[0][1]], { icon: customIcon }).addTo(mymap).bindPopup('Casa').openPopup();

            mymap.setView([coords[0][0], coords[0][1]], 14);


        } else {
            console.log("Ready state", http.readyState);
            console.log("Ready status", http.status);
        }
    }
    http.send(null);


