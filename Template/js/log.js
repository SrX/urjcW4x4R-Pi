$(function() {

    var name, started = false;

    var addItem = function(selector, item){
        console.log("AddItem");
        var template = $(selector).find('script[type="text/x-jquery-tmpl"]');
        template.tmpl(item).appendTo(selector);
    };

    var addMessage = function(data) {
        console.log("addMessage");
        var d = new Date();
        var win = $(window), doc = $(window.document);
        var bottom = win.scrollTop() + win.height() == doc.height();
        data.time = $.map([d.getHours(), d.getMinutes(), d.getSeconds()],
                          function(s) {
                              s = String(s);
                              return (s.length == 1 ? '0' : '') + s;
                          }).join(':');
        addItem('#messages', data);
        if (bottom) {
            window.scrollBy(0, 10000);
        }
    };

    var messaged = function(data) {
        console.log(data);
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