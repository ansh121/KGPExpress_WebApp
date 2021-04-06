$.getJSON("/static/assets/data/subject-list.json", function (data, textStatus, jqXHR) {
        var options = "";
        $.each(data, function (key, val) { 
            options += '<option value="' + val['value'] +' - '+ val['text'] + '" />';
        });

        // $("#subject-list").innerHTML = options;
        document.getElementById('subject-list').innerHTML = options;
        // console.log(options);
    }
);