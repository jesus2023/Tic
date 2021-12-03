const mymap = L.map('CovidMap').setView([10.968638, -74.806644,], 14);
const attribution =
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

var negativo = new L.Icon({
    
    iconUrl: '/static/png/coronavirus_verde.png',
    iconSize: [30, 30],
    iconAnchor: [15, 15]
});

var tratamiento = new L.Icon({
    
    iconUrl: '/static/png/coronavirus_amarillo.png',
    iconSize: [30, 30],
    iconAnchor: [15, 15]
});

var uci = new L.Icon({
    
    iconUrl: '/static/png/coronavirus_naranja.png',
    iconSize: [30, 30],
    iconAnchor: [15, 15]
});

var curado = new L.Icon({
    
    iconUrl: '/static/png/coronavirus_rosado.png',
    iconSize: [30, 30],
    iconAnchor: [15, 15]
});

var muerto = new L.Icon({
    
    iconUrl: '/static/png/coronavirus_rojo.png',
    iconSize: [30, 30],
    iconAnchor: [15, 15]
});

const tiles = L.tileLayer(tileUrl, { attribution });
tiles.addTo(mymap);

/*const http = new XMLHttpRequest() // metodo de javascript, para hacer peticiones a una url
    http.open('GET', "/mapa_general")
    http.onreadystatechange = () => {
        if (http.readyState == 4 && http.status == 200) {
            var cedulas = JSON.parse(http.responseText);
            console.log(cedulas)

        } else {
            console.log("Ready state", http.readyState);
            console.log("Ready status", http.status);
        }
    }
    http.send(null);*/

var cedulas
cedulas = document.getElementById('cedulas').value 

    console.log(cedulas)

    cedulas.forEach((cedula) =>{
        const httpc = new XMLHttpRequest() // metodo de javascript, para hacer peticiones a una url
        httpc.open('GET', "/ubic?param1=" + cedula)
        httpc.onreadystatechange = function () {
            if (httpc.readyState == 4 && httpc.status == 200) {
                
            }else {
                console.log("Ready state", httpc.readyState);
                console.log("Ready status", httpc.status);
            }
        }
        httpc.send(null);

    });    