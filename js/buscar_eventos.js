$(document).ready(function(){
    $("#formBuscar").submit(function (event) {
        event.preventDefault();
        var busqueda = encodeURIComponent($("#txtBuscar").val());
        const url = "https://serpapi.com/search.json?engine=google_events&q="+busqueda+"&hl=es&gl=cl&api_key=4f3fb89abbb1230ce9cd4bed2c80d7e2564964382dbf5a894a07da59e2e5405f";
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