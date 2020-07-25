# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:18:03 2020

@author: BTHRO
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json, ast

from Widget_Styles import *

class BreweryGUI(QMainWindow):
    def __init__(self,parameters):
        super().__init__()
        self.parameters=parameters
        # self.parameters.colour = 'blue'
        # self.setDockOptions(self.parameters._DOCK_OPTS)
        VLayoutP = QVBoxLayout()       
        for key, value in self.parameters.hardware.items():
            self.parameters.hardwareDict[key] = []
            self.parameters.brewGUI[key] = {}
            self.key = key

            #create a dockable widget which will contain child widgets only if at least one vlau
            if any(value):
                self.dock = dockable(key)
                self.parameters.brewGUI[key]['dockwidget']=[self.dock]

            #check if we are adding temperature functionality to the hardware
            if value[0]:
                self.addTemperature()
            else:
                self.parameters.hardwareDict[key]=[False,False,False]

            #check if we are adding relay functionality to the hardware
            if value[1]:
                self.addRelay()

            #check if we are adding timer functionality to the hardware
            if value[2]:pass 

            self.dock.setCentralWidget()
            self.addDockWidget(Qt.RightDockWidgetArea,self.dock)
        # print (self.parameters.brewGUI)


    #adding the temperature funcitonality
    #multiple probes connected to one hardware item - use min, max or average of readings

    def addTemperature(self):
        gb = groupBox('Temperature')

        VLayout = QVBoxLayout()
        HLayout = QHBoxLayout()
        tgtTemp = bodyLabel('Target temperature:')
        tgtLineTemp = bodyLineEdit()
        HLayout.addWidget(tgtTemp)
        HLayout.addWidget(tgtLineTemp)
        VLayout.addLayout(HLayout)

        HLayout = QHBoxLayout()
        tempTol = bodyLabel('Temperature tolerance:')
        tempLineTolerance = bodyLineEdit()
        HLayout.addWidget(tempTol)
        HLayout.addWidget(tempLineTolerance)
        VLayout.addLayout(HLayout)

        currentTemp = bodyLabel('Current temperature --> no reading')
        VLayout.addWidget(currentTemp)
        
        gb.setLayout(VLayout)          
        self.dock.addThisWidget(gb)

        #update widget dictionary with all widgets we created
        tempGroupBox = {'widget':gb,
                        'QLabelTgtTemp':{'widget':tgtTemp},
                        'QLabelTempTol':{'widget':tempTol},
                        'QLabelCurrentTemp':{'widget':currentTemp,'value':'no reading'},
                        'QLineEditTgtTemp':{'widget':tgtLineTemp,'value':None},
                        'QLineEditTempTol':{'widget':tempLineTolerance,'value':None}
                        }
        self.parameters.brewGUI[self.key]['tempGroupBox'] = tempGroupBox
        

    #adding the relay funcitonality
    def addRelay(self):
        gb = groupBox('Relay')
        # VLayout = QVBoxLayout()
        HLayout = QHBoxLayout()
        currentPins = bodyLabel('Relay pins attached --> no relays attached')
        HLayout.addWidget(currentPins)       
        switch = bodyButton()
        switch.setText(self.key+' - Off')
        switch.setCheckable(True)
        switch.clicked.connect(lambda ignore, a=self.key:self.whichbtn(a))
        HLayout.addWidget(switch)
        # VLayout.addLayout(HLayout)

        gb.setLayout(HLayout)          
        self.dock.addThisWidget(gb)

        #update widget dictionary with all widgets we created
        relayGroupBox = {'widget':gb,
                        'QLabelCurrentPins':{'widget':currentPins,'value':'no relays attached'},
                        'QPushButton':{'widget':switch,'value':False}
                        }
        self.parameters.brewGUI[self.key]['relayGroupBox'] = relayGroupBox


    def whichbtn(self,hardware):

        b = self.parameters.brewGUI[hardware]['relayGroupBox']['QPushButton']['widget']
        hw = b.text()[:b.text().find('-')-1]
#        print(hardwareName)
        if b.isChecked():
            b.setText(b.text()[:-6]+' - On')
            switch = True
        else:
            b.setText(b.text()[:-5]+' - Off')
            switch = False
        print('Trying to switch {}{}'.format(hw,b.text()[b.text().find('-')+1:]))

        #check to see if any pins are connected to the hardware
        if self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['value']=='no relays attached':
            print('Warning, no relays connected')
        else:
            #now loop through the pins and switch as necessary
            for pin in self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['value']:
                #check status of pin and switch relay on or off
                self.relay(pin,switch,hw)
            

    def relay(self,pin,switch,hw):
        # GPIO.setmode(GPIO.BCM) 
        # RELAIS_1_GPIO = pin
        # GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
        text=self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['widget'].text()
        print(text)
        if switch and not self.parameters.activePins[pin]:
            #check for other dependencies and only switch on if these are also true
            print('switching on relay connected to pin {}'.format(pin))
            self.parameters.activePins[pin]=True
            text = text.replace(str(pin),'<a style="color:red;"><strong>{}</strong></a>'.format(pin))
            # GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # turn on
        elif not switch and self.parameters.activePins[pin]:
            print('switching off relay connected to pin {}'.format(pin))
            self.parameters.activePins[pin]=False
            text = text.replace('<a style="color:red;"><strong>'+str(pin)+'</strong></a>','{}'.format(pin))
            # GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # turn on
        self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['widget'].setText(text)
        
                
def main():
    
    app = QApplication(sys.argv)
    parameters = Parameters()
    controller = BreweryGUI(parameters)
    controller.show()
#    controller.timer.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()