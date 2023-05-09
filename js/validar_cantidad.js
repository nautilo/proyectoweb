$(document).ready(function () {
    $.validator.addMethod("positive_integer", function (value, element) {
      // Sólo permite números enteros positivos mayores que 0
      return this.optional(element) || /^[1-9]\d*$/.test(value);
    }, "Ingresa un número entero mayor que 0");

    $('#formPagar').validate({
      rules: {
        txtCantidad: {
          required: true,
          positive_integer: true
        }
      },
    });
  });