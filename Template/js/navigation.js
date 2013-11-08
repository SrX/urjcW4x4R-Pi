$(function() {
    // add zoom out button 

    var options = {
            series: {
                lines: { show: true },
                points: { show: true }
            },
        xaxis: {
            tickDecimals: 0,
            tickSize: 1
        },
        zoom: {
            interactive: true
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
    // insert checkboxes 
    var choiceContainer = $("#choices");
    $.each(data, function(key, val) {
        choiceContainer.append("<br/><input type='checkbox' name='" + key +
            "' checked='checked' id='id" + key + "'></input>" +
            "<label for='id" + key + "'>" + val.label + "</label>");
    });

    choiceContainer.find("input").click(plotAccordingToChoices);

    function plotAccordingToChoices() {

        var xdata = [];

        choiceContainer.find("input:checked").each(function() {
            var key = $(this).attr("name");
            if (key && data[key]) {
                xdata.push(data[key]);
            }
        });
        if (data.length > 0) {
            $.plot(navi_map, xdata, options);
        }

    };

    plotAccordingToChoices();



    var messaged = function(data) {
        console.log("messaged_data_navigation");
        console.log(data);
        switch (data.action) {
            case 'route':
                onDataReceived(data.series);
                break;

            case 'coord_inLine':
                onDataReceived(data.series);
                break;

            case 'gpsInfo':
                console.log(data.gpsData);
                console.log(data.bla);
                if (data.gpsData != '') {
                    var series = {
                        label: 'GPS',
                        data: [
                            [data.gpsData.lat, data.gpsData.lon]
                        ]
                    };
                    onDataReceived(series);
                }
                break;

        }
    };

    var connected = function() {
        console.log("connected");
        socket.subscribe('navigation');

        //socket.send({hola:"hola hola->"});
        socket.send({
            action: 'get_route',
            'route_id': 0
        });
        get_gps_data();
    };

    var get_gps_data = function() {
        socket.send({
            action: 'get_gps_data'
        });
        setTimeout(get_gps_data, 1500);
    }

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