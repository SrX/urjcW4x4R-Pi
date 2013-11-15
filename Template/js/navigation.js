$(function() {
	// add zoom out button 

	function createnode(elem, id, nameclass, html) {
		var item = document.createElement(elem);
		item.setAttribute("id", id);
		item.setAttribute('class', nameclass);
		item.innerHTML = html;
		return item
	}

	var options = {

		series : {
			lines : {
				show : true
			},
			points : {
				show : true
			}
		},
		xaxis : {
			tickDecimals : 0,
			tickSize : 1
		},
		zoom : {
			interactive : true
		},
		pan : {
			interactive : true
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
			if (series.label == 'nextPoint') {

				var dl = data.length;
				for (var i = 0; i < dl; i++) {
					if (data[i].label == series.label) {
						data[i] = series
						console.log(data[i]);
					}
				}
			} else {

				var dl = data.length;
				for (var i = 0; i < dl; i++) {
					if (data[i].label == series.label) {
						data[i].data = data[i].data.concat(series.data);
					}
				}
			}
		}

		$.plot(navi_map, data, options);
		console.log("puntos pintados");
	}

	$("#do_route").click(function() {
		console.log('do_route');
		socket.send({
			action : 'do_route',
			'route_id' : 4
		});
	});

	var messaged = function(rxdata) {
		console.log("messaged_data_navigation");
		console.log(rxdata.action);
		switch (rxdata.action) {
		case 'route':
			onDataReceived(rxdata.series);
			break;

		case 'coord_inLine':
			onDataReceived(rxdata.series);
			break;

		case 'gpsInfo':
			if (rxdata.gpsData != '') {
				var series = {
					label : 'GPS',
					data : [ [ rxdata.gpsData.lat, rxdata.gpsData.lon ] ]
				};
				onDataReceived(series);
			}
			break;
		case 'get_routes':
			$.each(rxdata.info, function(key, value) {
				var node = createnode('div', value[1], 'ruta', value[0])
				$("#listarutas").append(node)
			});
			$("#listarutas").hide();
			$(".ruta").click(function() {
				socket.send({
					action : 'get_route',
					'route_id' : $(this).attr("id")
				});
			});
			break;
		case 'do_route':
			console.log(rxdata.gpsData);
			//console.log(data);
			//socket.broadcast_channel({"action": "do_route", "gpsData": gpsData,
			//"nextPoin": point, 'distance_to': dist}, 'navigation')
			var upData = {
				label : 'nextPoint',
				data : [ rxdata.nextPoint,
						[ rxdata.gpsData.lat, rxdata.gpsData.lon ] ],
				color : 7
			}
			onDataReceived(upData);
			if (rxdata.gpsData != '') {
				var series = {
					label : 'GPS',
					data : [ [ rxdata.gpsData.lat, rxdata.gpsData.lon ] ],
					color : 4
				};
				onDataReceived(series);
			}
			console.log("DOXROUTE");
			break;
		case 'blublu':
			console.log('blueblue');
			break;
		default:
			console.log("BlaBlaBLa");
		}
	};

	var connected = function() {
		console.log("connected");
		socket.subscribe('navigation');

		socket.send({
			action : 'get_routes'
		});

		socket.send({
			action : 'blublu'
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
	};

	$("#switchrutas").click(function(i) {
		if ($(this).parent().children("#listarutas").is(":hidden")) {
			$(this).parent().children("#listarutas").slideDown("slow");
		} else {
			$(this).parent().children("#listarutas").hide("slow");
		}
	})

	start();

});