$(function () {

  $('#container').highcharts({
        chart: {
            events: {
                redraw: function() {
                    alert ('The chart was just redrawn');
                }
            }
        },
        xAxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },

        series: [{
            data: [29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6]
        }]
    });

// Let the music play

    var messaged = function(data) {
        console.log("messaged_data_navigation");
        console.log(data);
        switch(data.action){
            case 'coord':
            var chart = $('#container').highcharts();
        chart.series[0].data.update(chart.series[0].data, false);
        left.update(leftVal, false);
        chart.redraw();
    //chart.addSeries({data: [216.4, 194.1, 95.6, 54.4, 29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5]});

            break;
        }
    };

    var connected = function() {
        console.log("connected");
        socket.subscribe('navigation');

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