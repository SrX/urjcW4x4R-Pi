#! /usr/bin/python
import gps, gps.clienthelpers

# session = gps.gps(mode=gps.WATCH_ENABLE)
session = gps.gps(mode=gps.WATCH_ENABLE)
try:
    while True:
        # Do stuff
        session.next()
        print session
        print session.fix.speed
        # Do more stuff
except StopIteration:
    print "GPSD has terminated"

# <dictwrapper: {u'track': 205.43, u'ept': 0.005, u'lon': -3.819696667,
# 				 u'lat': 40.282943333, u'tag': u'RMC', u'mode': 2,
 #				  u'time': u'2013-03-22T16:31:54.400Z', u'device': u'/dev/pts/3',
 #				   u'speed': 1.389, u'class': u'TPV'}>   