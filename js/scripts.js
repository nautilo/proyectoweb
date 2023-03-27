document.addEventListener("mousemove", parallax);

function parallax(event) {
    const x = -event.pageX/100;
    const y = -event.pageY/100;
    document.getElementById("info-perfil-productora").style.transform = `translateX(${-x}px) translateY(${y}px)`;
    document.getElementById("info-perfil-artista").style.transform = `translateX(${x}px) translateY(${y}px)`;  
}

jQuery.noConflict();jQuery(document).ready(function(){jQuery('#spoiler1').click(function(){jQuery('.mostrar1').slideToggle("slow");});});