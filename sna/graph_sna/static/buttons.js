/*
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
});*/

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



function callmymethodwithinput(){
        $('#loader').show();
        let input1 = $("#input1")["0"].value;
        let input2 = $("#input2")["0"].value;
        let algType = $("#submit_button").attr("data-algType");


        const Http = new XMLHttpRequest();
        const url = 'http://127.0.0.1:8000/vis/algorithm?type='+algType+'&in1='+input1+'&in2='+input2;
        Http.open("POST", url);
        Http.send();
        Http.onreadystatechange = (e) => {
            if (Http.readyState === 4){
                alert(Http.responseText);
                $('#loader').hide();
             }
 };
    return false;}


function showinputs(alg,count,input1name,input2name){

    $("#submit_button").attr("data-algType",alg);

    if (count===1){
        $('#input1').show();
        $('#input1').attr('placeholder',input1name);
        $('#input2').hide();

    }
    if (count===2){
        $('#input1').show();
        $('#input1').attr('placeholder',input1name);

        $('#input2').show();
        $('#input2').attr('placeholder',input2name);
    }
    return false;
}

function fill_inputs(myVal){

    if ($("#input1")["0"].value === ''){
        $("#input1")["0"].value = myVal;
        }

    else{
        $("#input2")["0"].value = myVal;
    }
}

