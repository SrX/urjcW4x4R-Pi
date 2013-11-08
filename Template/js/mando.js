$(document).ready(function() {

    var socket;

    var KEY_CODES = {
        87: 'straight', // W
        83: 'back',     // S
        65: 'left',     // A
        68: 'right',    // D
        32: 'stop',     // STOP
    };
    keys = {};


    $(window).keydown(function(event) {
        if (KEY_CODES[event.which]) {
            keys[KEY_CODES[event.which]] = true;
            return false;
        }
    });

    $(window).keyup(function(event) {
        if (KEY_CODES[event.which]) {
            keys[KEY_CODES[event.which]] = false;
            return false;
        }
    });

    $("#w").click(function () {
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
    $("#startroute").click(function () {
        socket.send({action: 'startroute'});
    });


    SendInputKey = function() {
        var move = ''
        if (keys['straight']) {
            move = 'w';
        } else if (keys['back']) {
            move = 's';
        } else if (keys['left']) {
            move = 'a';
        } else if (keys['right']) {
            move = 'd';
        } else if (keys['stop']) {
            move = 'q';
        };

        if (move != '') {
            socket.send({
                action: move
            });
        };
        setTimeout(SendInputKey, 50);
    };



    var messaged = function(data) {
        console.log("messaged_data");
        switch (data.action) {
            case 'update':
                $("#velocidad").html(data.ws)
                $("#giro").html(data.ad)
                break;
        }
    };


    var connected = function() {
        console.log("connected");
        socket.subscribe('hand_control');
        socket.send({
            action: 'update'
        });
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

        SendInputKey();

    };

    start();

});