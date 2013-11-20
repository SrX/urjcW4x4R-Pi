$(document).ready(function() {
	routeID = -1;//esto igual no deberia llevar var
	// add zoom out button

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

	// Optimizar de alguna manera esto
	function loadRouteToMap(series) {

		if (!alreadyFetched[series.label]) {
			alreadyFetched[series.label] = true;
			data.push(series);
		} else {
			var dl = data.length;
			for (var i = 0; i < dl; i++) {
				if (data[i].label == series.label) {
					data[i].data = series.data;
				}
			}
		}

		$.plot(navi_map, data, options);

	}
	;

	function onDataReceived(series) {

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

	};

	function createnode(elem, id, nameclass, html) {
		var item = document.createElement(elem);
		item.setAttribute("id", id);
		item.setAttribute('class', nameclass);
		item.innerHTML = html;
		return item
	}

	$("#switchrutas").click(function(i) {
		if ($(this).parent().children("#listarutas").is(":hidden")) {
			$(this).parent().children("#listarutas").slideDown("slow");
		} else {
			$(this).parent().children("#listarutas").hide("slow");
		}
	})	

	// HTML - CSS
	$("#startroute").click(function() {
		socket.send({
			action : 'startRoute',
			rid: routeID //rid Route ID
		});
	});

	$("#stoproute").click(function() {
		socket.send({
			action : 'stopRoute'
		});	
	});
	$("#stoproute").hide();

	var messaged = function(rxdata) {
		console.log("messaged_data_navigation");
		console.log(rxdata.action);
		switch (rxdata.action) {
		case 'loadRoute':
			var serie = {
				label : 'Ruta',
				data : rxdata.route,

				color : 7,

				lines : {
					show : false
				},
				points : {
					show : true
				},
				clickable : true
			};
			loadRouteToMap(serie)

			break;

		case 'gpsInfo':
			if (rxdata.gpsData != '') {
				var serie = {
					label : 'GPS',
					data : [ [ rxdata.gpsData.lat, rxdata.gpsData.lon ] ],
					lines : {
						show : true
					},
					points : {
						show : false
					},
					color : 9
				};
				onDataReceived(serie);
			}
			break;
		case 'deleted_route':
			$('#'+rxdata.id).remove();
			break;
		case 'init':
			$.each(rxdata.info, function(key, value) {
				var node = createnode('div', value[1], '', '')
				var nameroute = createnode('div', '', 'ruta', value[1] + ' ' + value[0])
				var deleteroute = createnode('div', '', 'delete', 'Borrar')
				node.appendChild(nameroute)
				node.appendChild(deleteroute)
				$("#listarutas").append(node)
			});
			$(".ruta").click(function() {
				
				//Guardar el id de la ruta seleccionada
				routeID = $(this).parent().attr("id")
				
				socket.send({
					action : 'get_route',
					'route_id' : routeID
				});
			});
			$(".delete").click(function() {		
				var currentid = $(this).parent().attr("id")
				if (currentid == routeID){
					routeID=-1
					var serie = {
						label : 'Ruta',
						data : [],

						color : 7,

						lines : {
							show : false
						},
						points : {
							show : true
						},
						clickable : true
					};
					loadRouteToMap(serie)
				}		
				socket.send({
					action : 'delete_route',
					'route_id' : currentid
				});
			});
			if (rxdata.routestate==1){
				$("#startroute").removeClass('pure-button pure-button-success');
				$("#startroute").addClass('pure-button pure-button-disabled');
				if ($("#stoproute").is(":hidden")) {
					$("#stoproute").slideDown("fast");
				}		
			}	
			break;
		case 'nexpPointInfo':
			break;
		case 'routeIsStarted':
			if ($("#stoproute").is(":hidden")) {
				$("#stoproute").slideDown("fast");
			}
			$("#startroute").removeClass('pure-button pure-button-success');
			$("#startroute").addClass('pure-button pure-button-disabled');
			break;
		case 'routeIsStopped':
			$("#startroute").removeClass('pure-button pure-button-disabled');
			$("#startroute").addClass('pure-button pure-button-success');
			$("#stoproute").hide("fast")
			break;
		default:
			console.log("Recibido algo fuera de lo comun");
		}
	};

	var connected = function() {
		console.log("connected");
		socket.subscribe('navigation');

		socket.send({
			action : 'init'//get routes y comprobar si esta haciendo ruta
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

	start();

});