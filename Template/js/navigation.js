$(function () {
    // add zoom out button 



    var options = {
        lines: { show: true },
        points: { show: false },
        xaxis: { tickDecimals: 0, tickSize: 1 },
        zoom: { interactive: true },
        xaxis: {
				//zoomRange: [0.1, 10],
				//panRange: [-3.815, 10]
			},
			yaxis: {
				//zoomRange: [0.1, 10],
				//panRange: [-3.8, -3.82]
			},
			pan: {
				interactive: true
			}
    };
    var data = [];
    var navi_map = $("#navi_map");
    
    $.plot(navi_map, data, options);

    
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
            $.plot(navi_map, data, options);
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

        addArrows();
    start();


		$("<div class='button' style='right:20px;top:20px'>zoom out</div>")
			.appendTo(navi_map)
			.click(function (event) {
				event.preventDefault();
				plot.zoomOut();
			});

		// and add panning buttons

		// little helper for taking the repetitive work out of placing
		// panning arrows

		function addArrow(dir, right, top, offset) {
			$("<img class='button' src='arrow-" + dir + ".gif' style='right:" + right + "px;top:" + top + "px'>")
				.appendTo(navi_map)
				.click(function (e) {
					e.preventDefault();
					plot.pan(offset);
				});
		}
        function addArrows(){
        addArrow("left", 55, 60, { left: -100 });
		addArrow("right", 25, 60, { left: 100 });
		addArrow("up", 40, 45, { top: -100 });
		addArrow("down", 40, 75, { top: 100 });
        }

});

