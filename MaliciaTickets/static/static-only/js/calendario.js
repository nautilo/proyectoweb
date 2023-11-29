$(document).ready(function() {
  //Calendario del mes actual
  var fecha_actual = new Date();
  var mes_actual = fecha_actual.getMonth();
  var dias_mes_actual = new Date(fecha_actual.getFullYear(), mes_actual + 1, 0).getDate();
  var primer_dia_mes = new Date(fecha_actual.getFullYear(), mes_actual, 1).getDay();
  
  var dia_mes = 1;
  var dia_semana = 1;
  var tbody = $('#calendarioMesActual tbody');
  
  while (dia_mes <= dias_mes_actual) {
    var tr = $('<tr></tr>');
    
    for (var i = 1; i <= 7; i++) {
      if (dia_semana < primer_dia_mes || dia_mes > dias_mes_actual) {
        tr.append($('<td></td>'));
      } else {

        tr.append($('<td id="DiaDelMesActual'+dia_mes+'"><h3 style="margin:10px;">' + dia_mes + '</h3></td>')); 
        
        
        dia_mes++;
      }
      
      dia_semana++;
    }
    
    tbody.append(tr);
  }
  // Calendario del mes siguiente
  var dias_mes_siguiente = new Date(fecha_actual.getFullYear(), mes_actual + 2, 0).getDate();
  var primer_dia_siguiente_mes = new Date(fecha_actual.getFullYear(), mes_actual + 1, 1).getDay();

  var dia_mes_siguiente = 1;
  var dia_semana_siguiente = 1;
  var tbody_siguiente = $('#calendarioMesSiguiente tbody');

    while (dia_mes_siguiente <= dias_mes_siguiente) {
      var tr = $('<tr></tr>');
  
    for (var i = 1; i <= 7; i++) {
      if (dia_semana_siguiente < primer_dia_siguiente_mes || dia_mes_siguiente > dias_mes_siguiente) {
        tr.append($('<td></td>'));
      } else {

        tr.append($('<td id="DiaDelMesSiguiente'+dia_mes_siguiente+'"><h3 style="margin:10px;">' + dia_mes_siguiente + '</h3></td>')); 
        
        
        dia_mes_siguiente++;
      }
      
      dia_semana_siguiente++;
    }

    tbody_siguiente.append(tr);
  }
  const urlMesActual = "https://serpapi.com/search.json?engine=google_events&q=Eventos+en+Chile&htichips=date:month&hl=es&gl=cl&api_key=f318ac3c2aadbd5f8ff5f2a66ad0ee079e5e9eb0b40fa88dd33b6dec5647b687";
  const proxyUrlMesActual = "https://api.allorigins.win/get?url=" + encodeURIComponent(urlMesActual);
          // allorigins.win permite usar headers que son protegidos por el servidor de la API mediante un proxy
          // en este caso se incluyó el header "api_key" en la url.
  $.get(proxyUrlMesActual,
  function(response){
      var data = JSON.parse(response.contents);
      $.each(data.events_results, function(i,item){
        var diaDelMes = item.date.start_date.split(" ")[1];
        var evento = '<div class="imgDiaCalendario" style=\'background-image: url("'+item.image+'");\'>'
        +"<div class='diaCalendario'><h3>"+diaDelMes+"</h3>"
        +"<p>"+item.title+"</p>"
        +"</div></div>";
        $('#DiaDelMesActual'+diaDelMes).html(evento); 
        

      });

    });
  const urlMesSiguiente = "https://serpapi.com/search.json?engine=google_events&q=Eventos+en+Chile&htichips=date:next_month&hl=es&gl=cl&api_key=f318ac3c2aadbd5f8ff5f2a66ad0ee079e5e9eb0b40fa88dd33b6dec5647b687";
  const proxyUrlMesSiguiente = "https://api.allorigins.win/get?url=" + encodeURIComponent(urlMesSiguiente);
          // allorigins.win permite usar headers que son protegidos por el servidor de la API mediante un proxy
          // en este caso se incluyó el header "api_key" en la url.
  $.get(proxyUrlMesSiguiente,
  function(response){
      var data = JSON.parse(response.contents);
      $.each(data.events_results, function(i,item){
        var diaDelMes = item.date.start_date.split(" ")[1];
        var evento = '<div class="imgDiaCalendario" style=\'background-image: url("'+item.image+'");\'>'
        +"<div class='diaCalendario'><h3>"+diaDelMes+"</h3>"
        +"<p>"+item.title+"</p>"
        +"</div></div>";
        $('#DiaDelMesSiguiente'+diaDelMes).html(evento); 
        

      });

    });
    
    
  });




  
