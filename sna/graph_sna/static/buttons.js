$.ajax({
    url: uri,
    cache: false,
    beforeSend: function(){
        $('#loader').show();
    },
    complete: function(){
        $('#loader').hide();
    },
    success: function(html){
       $('.loader').append(html);
    }
});



function callmymethod(myVal){
        $('#loader').show();
        const Http = new XMLHttpRequest();
        const url = 'http://127.0.0.1:8000/vis/algorithm?type='+myVal;
        Http.open("GET", url);
        Http.send();
        Http.onreadystatechange = (e) => {
            if (Http.readyState === 4){
                alert(Http.responseText);
                $('#loader').hide();

            }

};
    return false;}

