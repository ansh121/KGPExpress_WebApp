console.log($('#notification_checkbox').is(":checked"))
if ($('#notification_checkbox').is(":checked")) 
    $('#notification_checkbox').prop('checked', true);
else 
    $('#notification_checkbox').prop('checked', false);
// console.log(this.checked)

// $(function () {

$('#notification_checkbox').change(function() {
    // console.log(this.checked)
    if(this.checked) {
        $.ajax({
            type: "POST",
            url: "notification/",
            data: { notification: true },
            });
            // $('#notification').prop('checked', false); 
            $('#notification_checkbox').html('checked');
    }
    else{
        $.ajax({
            type: "POST",
            url: "notification/",
            data: { notification: false },
            });
            // $('#notification').prop('checked', true);
            $('#notification_checkbox').html('unchecked');
    }
});
   
// });