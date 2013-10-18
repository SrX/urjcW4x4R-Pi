$(function () {
    var options = {
        lines: { show: true },
        points: { show: false },
        xaxis: { tickDecimals: 0, tickSize: 1 }
    };
    var data = [];
    var placeholder = $("#placeholder");
    
    $.plot(placeholder, data, options);

    
    // fetch one series, adding to what we got
    var alreadyFetched = {};
    

        // then fetch the data with jQuery
        function onDataReceived(series) {
            console.log("onDataReceived");

    		if (!alreadyFetched[series.label]) {
    			alreadyFetched[series.label] = true;
    			data.push(series);
    		} else {
    			var dl = data.length;
    			for (var i = 0; i < dl; i++) {
    				if (data[i].label == series.label) {
    					data[i].data = data[i].data.concat(series.data);
    				}
    			}
    		}
            $.plot(placeholder, data, options);
            console.log("puntos pintados");
         }
  




        var messaged = function(data) {
        console.log("messaged_data_navigation");
        console.log(data);
        switch(data.action){
            case 'route':
            	onDataReceived(data.series);
            case 'coord_inLine':
            	onDataReceived(data.series);
            break;
        }
    };

    var connected = function() {
        console.log("connected");
        socket.subscribe('navigation');

        //socket.send({hola:"hola hola->"});
        socket.send({action:'get_route', 'route_id': 0});
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

