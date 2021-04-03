for (var i=0;i<event_list.length;i++){
    if (!('className' in event_list[i])){
        event_list[i].className = [];
    }
    event_list[i].className.push("bg-primary text-white");
}
