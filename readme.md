TODO:
- [ ] Reconfigurar GPS (1 Hz) - (No sacar bateria despues)
- [ ] Arreglo de grabar ruta, no funciona bien.
- [ ] Script para arancar el servidor:
 - Comprobar si esta el GPS
 - Arrancar gpsd
 - Arrancar cgps -s
 - Levantar el servidor web(para eth0 y wla0)
- [ ] Logger en la web para GPS y control del vehiculo
- [ ] Mejorar algoritmo de navegacion
 - Distancia que tiene que recorrer el coche para sacar el *track* util.


____________________________________________________________
Para correr el servidor en local:




1. Arrancar gpsd o gpsfake antes del servidor django
2. cgps -s
3. sudo python manage.py runserver_socketio localhost:3000




---Pluguins
https://github.com/django-debug-toolbar/django-debug-toolbar
https://github.com/yohanboniface/django-leaflet-storage


--Mapa
https://www.mapbox.com/
http://openlayers.org/


