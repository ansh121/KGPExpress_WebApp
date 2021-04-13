$(function () {

    $('#notification').change(function() {
        if(this.checked) {
            $.ajax({
                type: "POST",
                url: "notification/",
                data: { notification: false },
              });
              $('#notification').prop('checked', false); 
        }
        else{
            $.ajax({
                type: "POST",
                url: "notification/",
                data: { notification: true },
              });
              $('#notification').prop('checked', true);
        }
    });
   
});