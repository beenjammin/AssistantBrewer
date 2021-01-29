import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json, ast
try:
    import RPi.GPIO as GPIO #incase we are in test mode
except: 
    print('could not import RPi.GPIO')
#from Event_Functions import EventFunctions
from Widget_Styles import *

class RelayWidgets():
    def __init__(self):
        super().__init__()

    def __updateRelayHardware(self):
        try:
            self.parameters.relayHardware
        except:
            self.parameters.relayHardware = set()
        self.parameters.relayHardware.add(self.name)

    #adds basic relay to the GUI
    def addRelay(self,dock):
        self.__updateRelayHardware()
        self.hwStatus['relayButtonGUI']=False
        gb = groupBox('Relay')
        # VLayout = QVBoxLayout()
        HLayout = QHBoxLayout()
        currentPins = bodyLabel('Relay pins attached --> no relays attached')
        HLayout.addWidget(currentPins)       
        switch = bodyButton()
        switch.setText(self.name+' - Off')
        switch.setCheckable(True)
        switch.clicked.connect(lambda ignore, a=self.name:self.whichbtn(a))
        HLayout.addWidget(switch)
        # VLayout.addLayout(HLayout)

        gb.setLayout(HLayout)          
        dock.addThisWidget(gb)

        #update widget dictionary with all widgets we created
        relayGroupBox = {'widget':gb,
                        'QLabelCurrentPins':{'widget':currentPins,'value':'no relays attached'},
                        'QPushButton':{'widget':switch,'value':False}
                        }
        self.parameters.brewGUI[self.name]['relayGroupBox'] = relayGroupBox

    #handles the QPushButton click event
    def whichbtn(self,hardware):
        b = self.parameters.brewGUI[hardware]['relayGroupBox']['QPushButton']['widget']
        hw = self.name
#        print('hw is {} and self.name is {}'.format(hw,self.name))
        if b.isChecked():
            b.setText(b.text()[:-6]+' - On')
            switch = True
        else:
            b.setText(b.text()[:-5]+' - Off')
            switch = False
        #updating the status dictionary
        self.hwStatus['relayButtonGUI']=switch
#        print('hwstatus is {} and self.hwstatus is {}'.format(self.hwStatus,self.parameters.brewGUI[hw]['object'].hwStatus))
        print('Trying to switch {}{}'.format(hw,b.text()[b.text().find('-')+1:]))
        
        #check to see if any pins are connected to the hardware
        pins = self.pinList['relay']
        print(pins)
        if not pins:
            print('Warning, no relays connected')
        else:
            self.checkRelayPinStatus()
            
    def checkRelayPinStatus(self):
        """takes a list of pins and checks their status and status of parent HW switching on and off as required"""
        pins = self.pinList['relay']
        for pin in pins:
            self.updateStatus()
            # print('no hardware is associated with pin {}, try setting a connection for the pin in the connections tab'.format(pin))
            self.setRelay(pin)
       

    def setRelay(self,pin):
        """toggle the relay on or off and update the text in the GUI"""
        hw = self.name #set the hardare
        switch = self.status #set the switch status (true = on, false = off)
        if not self.parameters.test:
            GPIO.setmode(GPIO.BCM) 
            RELAIS_1_GPIO = int(pin)
            GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
        #get the current text of the widget so we can update it
        text=self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['widget'].text()
        if switch:
            print('switching on relay connected to pin {}'.format(pin))
#            self.parameters.relayPins[pin][0]=True
            self.lastRelayState=True
            text = text.replace(str(pin),'<a style="color:red;"><strong>{}</strong></a>'.format(pin))
            if not self.parameters.test:
                GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # turn on
        else:
            print('switching off relay connected to pin {}'.format(pin))
#            self.parameters.relayPins[pin][0]=False
            self.lastRelayState=False
            text = text.replace('<a style="color:red;"><strong>'+str(pin)+'</strong></a>','{}'.format(pin))
            if not self.parameters.test:
                GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # turn on
        self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['widget'].setText(text)
