$(document).ready(function () {
    $('#form-suscripcion').validate({
        rules: {
            email: {
                required: true,
                email: true,
            }
        }
    })
})
