$(document).ready(function () {
  $('#form-login').validate({
    rules: {
      email: {
        required: true,
        email: true,
      },
      contrasena: {
        required: true,
        minlength: 8,
      },
    },
  })
})
