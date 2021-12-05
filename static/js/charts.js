const http = new XMLHttpRequest() // metodo de javascript, para hacer peticiones a una url
http.open('GET', "/api/data")
http.onreadystatechange = () => {
    if (http.readyState == 4 && http.status == 200) {
        var coords = JSON.parse(http.responseText);
      

        var algo = document.getElementById("lineChart").getContext("2d");
        var lineChart = new Chart(algo, {

          type: "line",
          data:{
            labels: coords[0],
            datasets: [
            {
            label: "Infectados",
            data: coords[1],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
            },
            
          ]
          }, 
          options: {
            responsive: true
          }})
          

          var algo = document.getElementById("lineChart2").getContext("2d");
          var lineChart = new Chart(algo, {

            type: "line",
            data:{
              labels: coords[2],
              datasets: [
              {
              label: "Muertes",
              data: coords[3],
              fill: false,
              borderColor: 'rgb(255, 99, 132)',
              tension: 0.1
              },
              
            ]
            }, 
            options: {
              responsive: true
            }})

          var algo = document.getElementById("pie").getContext("2d");
          var pie = new Chart(algo, {
        
            type: "pie",
            data:{
              labels: [
                'Infectados',
                'Muertes',
                'Curados'
              ],
              datasets: [{
                label: 'My First Dataset',
                data: [coords[4],coords[6], coords[5]],
                backgroundColor: [
                  'rgb(255, 99, 132)',
                  'rgb(54, 162, 235)',
                  'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
              }]
            }, 
            options: {
              responsive: true
            }
          })

          var algo = document.getElementById("pie2").getContext("2d");
          var pie2 = new Chart(algo, {
        
            type: "pie",
            data:{
              labels: [
                'Tratamiento en casa',
                'Tratamiento Hospital',
                'UCI',
                'Muertos'
              ],
              datasets: [{
                label: 'My First Dataset',
                data: [coords[12], coords[11], coords[10],coords[9]],
                backgroundColor: [
                  'rgb(255, 99, 132)',
                  'rgb(54, 162, 235)',
                  'rgb(255, 205, 86)',
                  'rgb(51, 204, 51)'
                ],
                hoverOffset: 4
              }]
            }, 
            options: {
              responsive: true
            }
          })

          var algo = document.getElementById("pie3").getContext("2d");
          var pie3 = new Chart(algo, {
        
            type: "pie",
            data:{
              labels: [
                'Positivos',
                'Negativos'
              ],
              datasets: [{
                label: 'Resultados',
                data: [coords[8],coords[7]],
                backgroundColor: [
                   'rgb(255, 99, 132)',
                  'rgb(51, 204, 51)',
                ],
                hoverOffset: 4
              }]
            }, 
            options: {
              responsive: true
            }
          })

    } else {
        console.log("Ready state", http.readyState);
        console.log("Ready status", http.status);
    }
}
http.send(null);