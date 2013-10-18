$(document).ready(function () {

var socket;

    $("#w").click(function () {
        socket.send({type: 'manual_control',action:"messaged", actionx: 'w'});
        console.log("send w");
    });
    $("#s").click(function () {
        socket.send({type: 'manual_control',action:"messaged", actionx: 's'});
    });
    $("#a").click(function () {
        socket.send({type: 'manual_control',action:"messaged", actionx: 'a'});
    });
    $("#d").click(function () {
        socket.send({type: 'manual_control',action:"messaged", actionx: 'd'});
    });
    $("#stop").click(function () {
       socket.send({type: 'manual_control',action:"messaged", actionx: 'stop'});
    });




    var messaged = function(data) {
        console.log("messaged_data");
        switch(data.actionx){
            case 'w':
            case 's':
            $("#velocidad").html(data.value)
            break;
            
            case 'a':
            case 'd':
            $("#giro").html(data.value)
            break;
        }


        switch (data.action) {
            case 'in-use':
                alert('Name is in use, please choose another');
                break;
            case 'started':
                started = true;
                break;
            case 'message':
                break;  
            case 'system':
                data['name'] = 'SYSTEM';
                
                break;
        }
    };


    var connected = function() {
        console.log("connected");
        socket.subscribe('manual_control');

        socket.send({hola:"hola hola->"});
    };

    var disconnected = function() {
        console.log("disconnected");
        setTimeout(start, 1000);
    };

    var start = function() {
        socket = new io.Socket();
        socket.connect();
        socket.on('connect', connected);
        socket.on('disconnect', disconnected);
        socket.on('message', messaged);

    };

    start();

});