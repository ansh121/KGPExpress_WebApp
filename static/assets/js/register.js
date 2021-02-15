$('#password, #password_check').on('keyup', function () {
      if($('#password').val() == "" || $('#password_check').val() == "") {
        $('#message').html('').css('color', 'green');
      }
      else if ($('#password').val() == $('#password_check').val()) {
        $('#message').html('Matching').css('color', 'green');
      } else
        $('#message').html('Not Matching').css('color', 'red');
    }
);