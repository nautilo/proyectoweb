$(document).ready(function() {
    $("#contact-form").validate({
      rules: {
        name : {
          required: true,
          minlength: 3
        },
        email: {
          required: true,
          email: true
        },
        subject: {
            required: true,
            minlength: 3
        },
        message: {
            required: true,
            minlength: 3
        }
      }
    });
  });
  