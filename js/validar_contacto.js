$(document).ready(function(event) {
    event.preventDefault();
    $("#contact-form").validate({
      rules: {
        name : {
          required: true,
        },
        email: {
          required: true,
          email: true
        },
        asunto: {
            required: true,
            minlength: 3
        },
        mensaje: {
            required: true,
            minlength: 3
        },
      },
      messages : {
        name: {
          required: "Debe ingresar un nombre"
        },
        email: {
            required: "Debe ingresar un email",
            email: "Debe tener sintaxis de email"
        },
        asunto: {
            required: "Ingrese un asunto",
            minlength: "Largo min 3 caracteres"
        },
        message: {
            required: "Ingrese texto del mensaje",
            minlength: "Largo min 3 caracteres"
        }
      }
    });
  });
