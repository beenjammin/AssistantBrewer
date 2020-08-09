from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
try:
    import RPi.GPIO as GPIO #incase we are in test mode
except: 
    print('could not import RPi.GPIO')

#to do, add the option for an always on relay

class EventFunctions():
    """A class which contains the function handling for the GUI EventFunctions"""
    def __init__(self, parameters):
        super(EventFunctions, self).__init__()
        self.parameters = parameters
        

    def checkPinStatus(self,pins):
        """takes a list of pins and checks their status and status of parent HW switching on and off as required"""
        for pin in pins: #self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['value']:
            #check to see if the pin value is true and it has hardware assigned
            hw = self.parameters.activePins[pin][1]
            #update the status of the hardware - pin may not need switching on
            try:
                self.parameters.brewGUI[hw]['object'].updateStatus()
            except:
                print('no hardware is associated with pin {}, try the connections tab'.format(pin))
            switch = self.parameters.activePins[pin][0]
            if hw in self.parameters.hwList:
                self.relay(pin,switch,hw)
       

    def relay(self,pin,switch,hw):
        """toggle the relay on or off and update the text in the GUI"""
        if not self.parameters.test:
            GPIO.setmode(GPIO.BCM) 
            RELAIS_1_GPIO = pin
            GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
        #get the current text of the widget so we can update it
        text=self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['widget'].text()
        if switch:
            #check for other dependencies and only switch on if these are also true
            print('switching on relay connected to pin {}'.format(pin))
            self.parameters.activePins[pin]=True
            text = text.replace(str(pin),'<a style="color:red;"><strong>{}</strong></a>'.format(pin))
            if not self.parameters.test:
                GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # turn on
        else:
            print('switching off relay connected to pin {}'.format(pin))
            self.parameters.activePins[pin]=False
            text = text.replace('<a style="color:red;"><strong>'+str(pin)+'</strong></a>','{}'.format(pin))
            if not self.parameters.test:
                GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # turn on
        self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['widget'].setText(text)

            
