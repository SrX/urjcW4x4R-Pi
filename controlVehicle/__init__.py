import gps
import sys
import serial
import time



class Control(object):
    def __init__ (self):
        self.ws_value = 90
        self.ad_value = 90
        
        # Paso del incremento
        self.inc = 3;
        
        try:
            self.arduino_conect = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        except:  # except (StopIteration):
            print "Unexpected error: Control ", sys.exc_info()[0]
            self.arduino_conect = ''
            pass
        
        self.reset()
        
        
    def reset(self):
        self.ws_value = 90
        self.ad_value = 90
        self.set(self.ws_value, self.ad_value)
        
    def action(self, action):
        if action == 'w':
            self.ws_value += self.inc
        elif action == 's':
            self.ws_value -= self.inc
        elif action == 'd':
            self.ad_value -= self.inc
        elif action == 'a':
            self.ad_value += self.inc
        else:  # action == 'q':
            # por medidas de seguridad, si el coche se escapa 
            # y/o el piloto se pone nervioso
            self.reset()
        
        self.evalue_wa()
        self.set(self.ws_value, self.ad_value)
        
        #devolver el valor, el que se ha pasado al coche
        return self.ws_value, self.ad_value
            
    def set(self, speed, angle):
        

        print 'Vehicle: s-' + str(speed) + ' a-' + str(angle)
        
        if self.arduino_conect != '':
            self.speed(speed)
            self.turn(angle)
        
    def speed(self, velocidad):
            self.arduino_conect.write(chr(255))
            self.arduino_conect.write(chr(2))
            self.arduino_conect.write(chr(velocidad))


    def turn(self, grados):
            self.arduino_conect.write(chr(255)) 
            self.arduino_conect.write(chr(1))
            self.arduino_conect.write(chr(grados))
            
    def evalue_wa(self):
        if self.ws_value > 120:
            self.ws_value = 120
        elif self.ws_value < 60:
            self.ws_value = 60
        
        if self.ad_value > 120:
            self.ad_value = 120
        elif self.ad_value < 60:
            self.ad_value = 60


vehicle = Control();






