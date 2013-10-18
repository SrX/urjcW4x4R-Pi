$(function() {

    var name, started = false;

    var addItem = function(selector, item){
        console.log("AddItem");
        var template = $(selector).find('script[type="text/x-jquery-tmpl"]');
        template.tmpl(item).appendTo(selector);
    };

    var messaged = function(data) {
        console.log("messaged");
        switch (data.action) {
        	case 'message':
                addMessage(data);
                break;
        }
    };

    var socket;

    var connected = function() {
        console.log("connected");
        socket.subscribe('logger');
    };

    var disconnected = function() {
        console.log("disconnected");
        setTimeout(start, 1000);
    };

    var start = function() {
	    console.log("start");
	    socket = new io.Socket();
	    socket.connect();
	    socket.on('connect', connected);
	    socket.on('disconnect', disconnected);
	    socket.on('message', messaged);
	};

    start();

});