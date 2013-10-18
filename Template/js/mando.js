$(document).ready(function () {

var socket;

    $("#w").click(function () {
        console.log("send w");
        socket.send({action: 'w'});
    });
    $("#s").click(function () {
        socket.send({action: 's'});
    });
    $("#a").click(function () {
        socket.send({action: 'a'});
    });
    $("#d").click(function () {
        socket.send({action: 'd'});
    });
    $("#stop").click(function () {
        socket.send({action: 'q'});
    });




    var messaged = function(data) {
        console.log("messaged_data");
        switch(data.action){
            case 'update':
                $("#velocidad").html(data.ws) 
                $("#giro").html(data.ad)
            break;
        }
    };


    var connected = function() {
        console.log("connected");
        socket.subscribe('hand_control');

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
