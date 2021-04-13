$(document).ready(function () {
  $("#addRegisteredSubjectForm").submit(function (event) {
    event.preventDefault();
    $.ajax({
      type: "POST",
      url: "add_registered_subject/",
      data: { subject: $("#subject").val() },
      success: function (data1) {
        alert(data1['message']);
        if(data1['flag']=='success'){
            $('#registered_subjects').append("<li id=\""+data1['subject_id'].slice(0,7)+"\" class=\"list-group-item\"><div class=\"row\"><div class=\"col-10\"><a class=\"btn btn-sm text-truncate btn-block text-left\">"+$("#subject").val()+"</a></div><div class=\"col-2\"><a class=\"btn btn-sm text-truncate btn-block text-left\"><i class=\"fa fa-trash\" aria-hidden=\"true\"></i></a></div></div></li>");
          }
          $("#subject").val('');
          console.log(data)  
          console.log(data1)
          
          data=data.slice(0,-1)+','+data1['event'].slice(1)
          data_update();
          cal();
          fill_colors();
        },
    });
  });
  $.each( $('form[id^=deleteRegisteredSubjectForm]'), function () {
    $(this).submit(function (event) {
      event.preventDefault();
      $.ajax({
        type: "POST",
        url: "delete_registered_subject/",
        data: { subject_id: $(this).attr('id'), msg: "reached" },
        success: function (data1) {
          // alert(data1['message']);     
          // console.log(data1)
          location.reload();
          },
      });
    });
  });
});

function fill_colors(){
  var color_classes=["primary","secondary","success","info","dark","danger","warning","light"];
  var count=color_classes.length
  var IDs = [];
  $("#registered_subjects").find("li").each(function(){ IDs.push(this.id); });

  var dict = {};
  for (index = 0; index < IDs.length; index++) {
    
    $.each( $("#"+IDs[index]), function () {
      $(this).addClass("list-group-item-"+color_classes[index%count]);
      // console.log("hello");
    });

    dict[IDs[index]] = color_classes[index%count];

    // $.each( $("."+IDs[index]), function () {
    //   $(this).addClass(color_classes[index%count]);
    //   console.log("hello");
    // });
  }

  for (var i=0;i<event_list.length;i++){
    event_list[i].className.push("bg-"+dict[event_list[i].subject_id])
    event_list[i].className.push("text-white")
  }

  cal();
}

$(document).ready(fill_colors());
// $.each( $("input[name^='news-top-']"), function () {
//   alert( $(this).hide() );
// });

jQuery(document).ajaxSend(function (event, xhr, settings) {
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  function sameOrigin(url) {
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = "//" + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (
      url == origin ||
      url.slice(0, origin.length + 1) == origin + "/" ||
      url == sr_origin ||
      url.slice(0, sr_origin.length + 1) == sr_origin + "/" ||
      // or any other URL that isn't scheme relative or absolute i.e relative.
      !/^(\/\/|http:|https:).*/.test(url)
    );
  }
  function safeMethod(method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }

  if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
  }
});

