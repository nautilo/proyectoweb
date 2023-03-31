$(document).ready(function() {
    $("#form-registro").validate({
      rules: {
        name : {
          required: true,
          minlength: 3
        },
        email: {
          required: true,
          email: true
        },
        contrasena: {
            required: true,
            minlength: 8
        },
        repetircontrasena: {
            required: true, 
            equalTo:contrasena,
            minlength: 8
        }
      }
    });
  });
  