// $('title').innertext.equals("KGPExpress - Home"){
//     $('#home').addClass('active');
// };

// $('title').html(function(){
//     console.log("first");
//     if(this[0].text==="KGPExpress - Home"){
//         console.log("second");
//         $('#home').addClass('active');
//     }
// });

if($('title')[0].text==="KGPExpress - Home"){
    $('#home').addClass('active');
}
else if($('title')[0].text==="KGPExpress - Log In"){
    $('#login').addClass('active');
}
else if($('title')[0].text==="KGPExpress - Instructions"){
    $('#instructions').addClass('active');
}
else if($('title')[0].text==="KGPExpress - About Us"){
    $('#about_us').addClass('active');
}
else if($('title')[0].text==="KGPExpress - My Subjects"){
    $('#my_subjects').addClass('active');
}
// else if($('title')[0].text==="KGPExpress - "){
//     $('#').addClass('active');
// }