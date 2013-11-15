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
     $("#stoproute").click(function () {
        socket.send({action: 'stoproute'});
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
        setTimeout(SendInputKey, 70);
    };



    var messaged = function(data) {
        console.log("messaged_data");
        switch (data.action) {
            case 'init':
                $("#velocidad").html(data.ws)
                $("#giro").html(data.ad)
                if (data.recording=='1'){
                    if ($("#stoproute").is(":hidden")) {
                        $("#stoproute").show();
                    }
                    $("#startroute").removeClass('pure-button pure-button-success');
                    $("#startroute").addClass('pure-button pure-button-disabled');                    
                }
                break
            case 'update':
                $("#velocidad").html(data.ws)
                $("#giro").html(data.ad)
                break
            case 'startedroute':
                if ($("#stoproute").is(":hidden")) {
                    $("#stoproute").show();
                }
                $("#startroute").removeClass('pure-button pure-button-success');
                $("#startroute").addClass('pure-button pure-button-disabled');
                break
            case 'stoppedroute':
                $("#startroute").removeClass('pure-button pure-button-disabled');
                $("#startroute").addClass('pure-button pure-button-success');
                $("#stoproute").hide("fast");
                break
        }
    };

    $("#stoproute").hide();

    var connected = function() {
        console.log("connected");
        socket.subscribe('hand_control');
        socket.send({
            action: 'init'
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