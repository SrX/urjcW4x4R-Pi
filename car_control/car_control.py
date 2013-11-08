#!/usr/bin/env python
import serial, time

class Control:

    # arreglar el fallo del log
    def __init__ (self):
        self.arduino_conect = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.speed(90)
        self.turn(90)

    def speed(self, velocidad):
        self.arduino_conect.write(chr(255))
        self.arduino_conect.write(chr(2))
        self.arduino_conect.write(chr(velocidad))


    def turn(self, grados):
        self.arduino_conect.write(chr(255)) 
        self.arduino_conect.write(chr(1))
        self.arduino_conect.write(chr(grados))


    #def close(self):
        #self.fichero.close()

if __name__ == '__main__':
    Conect = Control()
    Conect.speed(96)
    time.sleep(2)
    Conect.turn(120)
    time.sleep(2)
    Conect.speed(90)
    time.sleep(2)
    Conect.turn(90)
    time.sleep(2)
