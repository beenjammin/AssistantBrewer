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
            self.parameters.brewGUI[key] = {}
            self.parameters.brewGUI[key]['object'] = Hardware(self.parameters,key)

            #create a dockable widget which will contain child widgets only if at least one vlau
            if any(value):
                self.dock = dockable(key)
                self.parameters.brewGUI[key]['dockwidget']=[self.dock]

            #check if we are adding simple temperature functionality to the hardware
            if value['widgets'][0]:
                self.parameters.brewGUI[key]['object'].addSimpleTemp(self.dock)

            #check if we are adding targer temperature functionality to the hardware
            if value['widgets'][1]:
                self.parameters.brewGUI[key]['object'].addTempTgt(self.dock)

            #check if we are adding temperature timer functionality to the hardware
            if value['widgets'][2]:pass

            #check if we are adding relay functionality to the hardware
            if value['widgets'][3]:
                self.parameters.brewGUI[key]['object'].addRelay(self.dock)

            self.dock.setCentralWidget()
            self.addDockWidget(Qt.RightDockWidgetArea,self.dock)
        # print (self.parameters.brewGUI)


    #adding the temperature funcitonality
    #multiple probes connected to one hardware item - use min, max or average of readings
class Temperature():
    def __init__(self, parameters):
        self.parameters = parameters
        #Heat, cool, do nothing
        self.status = 'do nothing'
        self.hwTemp = ''


    def __updateTempHardware(self):
        try:
            self.parameters.tempHardware
        except:
            self.parameters.tempHardware = set()
        self.parameters.tempHardware.add(self.name)


    def getTemp(self):
        if self.actorList:
            indices = [self.parameters.actors['actors'].index(b) for b in self.actorList]
            temps = [float(self.parameters.actors['readings'][b]) for b in indices]
            print('temps for {} is {}'.format(self.name,temps))
            self.tempCalc = 'max'
            if self.tempCalc == 'max':
                self.hwTemp = max(temps)
                print(self.hwTemp)
            elif self.tempCalc == 'min':
                self.hwTemp = min(temps)
            else:
                self.hwTemp = average(temps)
        else:
            self.hwTemp = ''


    # add a simple temp widget to the GUI            
    def addSimpleTemp(self,dock):
        self.__updateTempHardware()
        gb = groupBox('Temperature')
        HLayout = QHBoxLayout()
        currentTemp = bodyLabel('Current temperature --> no reading')
        HLayout.addWidget(currentTemp)
        gb.setLayout(HLayout)          
        dock.addThisWidget(gb)

        tempGroupBox = {'widget':gb,
                        'QLabelCurrentTemp':{'widget':currentTemp,'value':'no reading'},
                        }
        self.parameters.brewGUI[self.name]['tempGroupBox'] = tempGroupBox

    # add a target temperature widget to the GUI
    def addTempTgt(self,dock):
        self.__updateTempHardware()
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
        dock.addThisWidget(gb)

        #update widget dictionary with all widgets we created
        tempGroupBox = {'widget':gb,
                        'QLabelTgtTemp':{'widget':tgtTemp},
                        'QLabelTempTol':{'widget':tempTol},
                        'QLabelCurrentTemp':{'widget':currentTemp,'value':'no reading'},
                        'QLineEditTgtTemp':{'widget':tgtLineTemp,'value':None},
                        'QLineEditTempTol':{'widget':tempLineTolerance,'value':None}
                        }
        self.parameters.brewGUI[self.name]['tempGroupBox'] = tempGroupBox
    
     # add a temperature timer widget to the GUI    
    def addTempTimer(self):pass

class Relay():
    def __init__(self, parameters):
        self.parameters = parameters
        #Relay can be on or off
        self.status = False

    def __updateRelayHardware(self):
        try:
            self.parameters.relayHardware
        except:
            self.parameters.relayHardware = set()
        self.parameters.relayHardware.add(self.name)



    def addRelay(self,dock):
        self.__updateRelayHardware()
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


    def whichbtn(self,hardware):
        b = self.parameters.brewGUI[hardware]['relayGroupBox']['QPushButton']['widget']
        hw = b.text()[:b.text().find('-')-1]
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

#A super class that will inherit all properties of probes and relays    
class Hardware(Temperature,Relay):
    def __init__(self,parameters,name):
        Temperature.__init__(self,parameters)
        Relay.__init__(self,parameters)
        self.name = name
        self.actorList = []
        self.pins = []

    def updateTempLabel(self):
        self.getTemp()
        if self.hwTemp:
            text = self.parameters.brewGUI[self.name]['tempGroupBox']['QLabelCurrentTemp']['widget'].text()
            text = text[:text.find('-->')+4]+'{}'.format(round(self.hwTemp,1))
            self.parameters.brewGUI[self.name]['tempGroupBox']['QLabelCurrentTemp']['widget'].setText(text)
        else:
            text = 'Current temperature --> no reading'
            self.parameters.brewGUI[self.name]['tempGroupBox']['QLabelCurrentTemp']['widget'].setText(text)




def main():   
    app = QApplication(sys.argv)
    parameters = Parameters()
    controller = BreweryGUI(parameters)
    controller.show()
#    controller.timer.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()