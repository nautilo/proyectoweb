$(document).ready(function(){
    $("#formBuscar").submit(function (event) {
        event.preventDefault();
        var busqueda = encodeURIComponent($("#txtBuscar").val());
        const url = "https://serpapi.com/search.json?engine=google_events&q="+busqueda+"&hl=es&gl=cl&api_key=f318ac3c2aadbd5f8ff5f2a66ad0ee079e5e9eb0b40fa88dd33b6dec5647b687";
        const proxyUrl = "https://api.allorigins.win/get?url=" + encodeURIComponent(url);
                // allorigins.win permite usar headers que son protegidos por el servidor de la API mediante un proxy
                // en este caso se incluyó el header "api_key" en la url.
        $.get(proxyUrl,
        function(response){
            var data = JSON.parse(response.contents);
            $("#tbResultados").find("tbody tr").remove();
            $.each(data.events_results, function(i, item){
               
                var fila = "<tr><td><img class='miniatura-busqueda' src='"+item.thumbnail+"'>"+item.title
                            +"</td><td>"+item.date.when
                            +"</td><td>"+item.address[0]
                            +"</td><td>"+item.address[1]+"</td></tr>"
                  
                $("#tbResultados").append(fila);   
            
            });
        });
    });
});