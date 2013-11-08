#! /usr/bin/python
import gps

class Start(object):

	def __init__(self):
        print "init gps"
		self._gps = gps.gps(mode=gps.WATCH_ENABLE|gps.WATCH_NEWSTYLE)

	def Update(self):
		try:
			self._gps.next()
        except StopIteration:
            print "stop Iteration"
			pass				#Hay que decidir que hacer si se produce un error.

		return	{	'lat'	:	self._gps.fix.latitude,
					'lon'	:	self._gps.fix.longitude,
                    'track' :	self._gps.fix.track,
                    'speed' :	self._gps.fix.speed,
                    'time'	:	self._gps.fix.time, #le pasa algo raro
			#'date' 	:	self._gps.fix.date,
			#'alt'	: 	self._gps.fix.altitude,
 }

if __name__ == '__main__':
	q = Start()
	while 1:
		print q.update()


#Respeco del tiempo:
	#'time': u'2013-03-22T16:35:35.400Z
	#'time': 1363970134.4
