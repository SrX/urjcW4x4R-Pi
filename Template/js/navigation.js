$(document).ready(
    function() {

      routeID = -1;
      // esto igual no deberia llevar var
      // add zoom out button

     // var data = [ [ [ "/static/mapa.png", 40.2, -3.82, 40.3, -3.81 ] ] ];
     
     var data = [];

      var options = {
          
            series : { lines : { show : true }, points : { show : true },
            images : { show : false } },
           
        zoom : {
          interactive : true
        },
        pan : {
          interactive : true
        }
      };

      

      function updateMap() {
        $.plot("#navi_map", data, options);
        console.log(data)
      }
      ;

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
        updateMap();
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

        updateMap();

      }
      ;

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
          rid : routeID
        // rid Route ID
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
          console.log(rxdata.gpsData);
          if (rxdata.gpsData != '') {
            $("#gpsLat").html(rxdata.gpsData.lat);
            $("#gpsLon").html(rxdata.gpsData.lon);            
            var serie = {
              label : 'GPS',
              data : [ [ rxdata.gpsData.lon, rxdata.gpsData.lat ] ],
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
          $('#' + rxdata.id).remove();
          break;
        case 'init':
          $.each(rxdata.info, function(key, value) {
            var node = createnode('div', value[1], '', '')
            var nameroute = createnode('div', '', 'ruta', value[1] + ' '
                + value[0])
            var deleteroute = createnode('div', '', 'delete', 'Borrar')
            var confirm = createnode('div', '', 'confirm', 'Yes')
            var cancel = createnode('div', '', 'cancel', 'No')
            node.appendChild(nameroute)
            deleteroute.appendChild(confirm)
            deleteroute.appendChild(cancel)
            node.appendChild(deleteroute)
            $("#listarutas").append(node)
          });
          $(".ruta").click(function() {

            // Guardar el id de la ruta seleccionada
            routeID = $(this).parent().attr("id")

            socket.send({
              action : 'get_route',
              'route_id' : routeID
            });
          });
          $(".delete").click(function() {
            $(this).children(".confirm").show();
            $(this).children(".cancel").show();
          });
          $(".confirm").click(function() {
            var currentid = $(this).parent().parent().attr("id")
            if (currentid == routeID) {
              routeID = -1; // para no pasarle un ID en caso de startroute
              // si era el mismo
              var serie = {
                label : 'Ruta',
                data : [],

                color : 7,

                images: {show: false}, bars: {show: false}, points: {show: false}, lines: {show: true},
                clickable : true
              };
              loadRouteToMap(serie)
            }
            socket.send({
              action : 'delete_route',
              'route_id' : currentid
            });            
          });
          $(".cancel").click(function() {
            $(this).parent().children(".confirm").hide("fast");
            $(this).hide("fast");
          });    
          $(".confirm").hide("fast");
          $(".cancel").hide("fast");      
          if (rxdata.routestate == 1) {
            $("#startroute").removeClass('pure-button pure-button-success');
            $("#startroute").addClass('pure-button pure-button-disabled');
            if ($("#stoproute").is(":hidden")) {
              $("#stoproute").slideDown("fast");
            }
            var serie = {
              label : 'Ruta',
              data : rxdata.routecoords,

              color : 7,

              images: {show: false}, bars: {show: false}, points: {show: false}, lines: {show: true},
              clickable : true
            };
            loadRouteToMap(serie)
            break;

          }
          break;
        case 'nexpPointInfo':
          break;
        case 'routeIsStarted':
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
          $("#npDistance").html("-");
          $("#npLat").html("-");
          $("#npLon").html("-");
          break;
        case 'next_point':
          $("#npLat").html(rxdata.lat);
          $("#npLon").html(rxdata.lon);
          break;
        case 'state_route':
          var numero = rxdata.dist/100;
          $("#npDistance").html(numero.toFixed(3) + " m");
          break;
        default:
          break;
        }
      };

      var connected = function() {
        console.log("connected");
        socket.subscribe('navigation');

        socket.send({
          action : 'init'// get routes y comprobar si esta haciendo ruta
        });

        updateMap()

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
