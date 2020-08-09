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

try:
    import RPi.GPIO as GPIO #incase we are in test mode
except: 
    print('could not import RPi.GPIO')

from Widget_Styles import *
from Event_Functions import EventFunctions

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
                self.dock = dockable(key,objectName = 'childTab')
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
        self.hwTemp = ''

    #update the set of hardware with temperature properties
    def __updateTempHardware(self):
        try:
            self.parameters.tempHardware
        except:
            self.parameters.tempHardware = set()
        self.parameters.tempHardware.add(self.name)

    #get the temperature of the hardware
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

    #update the status (on/off) for the TempTgt widget
    def updateTempTgtStatus(self):
        try:
            tgtTemp = float(self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTemp']['widget'].text())
            tempTol = float(self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTempTol']['widget'].text())
            currentTemp = float(self.hwTemp)
            pinStatus = all([self.parameters.activePins[a[0]] for a in self.pinList])
            if currentTemp < tgtTemp - tempTol:
                self.hwStatus['TempTgt']=True
            elif currentTemp < tgtTemp and pinStatus:
                self.hwStatus['TempTgt']=True
            else:
                self.hwStatus['TempTgt']=False
        except ValueError: pass
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise 





    # add a target temperature widget to the GUI
    def addTempTgt(self,dock):
        self.__updateTempHardware()
        self.hwStatus['TempTgt']=False
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

class Relay(EventFunctions):
    def __init__(self, parameters):
        EventFunctions.__init__(self,parameters)
        self.parameters = parameters

    def __updateRelayHardware(self):
        try:
            self.parameters.relayHardware
        except:
            self.parameters.relayHardware = set()
        self.parameters.relayHardware.add(self.name)

    #adds basic relay to the GUI
    def addRelay(self,dock):
        self.__updateRelayHardware()
        self.hwStatus['relay']=False
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
        hw = b.text()[:b.text().find('-')-1]
        if b.isChecked():
            b.setText(b.text()[:-6]+' - On')
            switch = True
        else:
            b.setText(b.text()[:-5]+' - Off')
            switch = False
        #updating the status dictionary
        self.parameters.brewGUI[hw]['object'].hwStatus['relay']=switch
        print('Trying to switch {}{}'.format(hw,b.text()[b.text().find('-')+1:]))
        #check to see if any pins are connected to the hardware
        pins = self.parameters.brewGUI[hw]['object'].pinList
        print(pins)
        if not pins:
            print('Warning, no relays connected')
        else:
            self.checkPinStatus(pins)



#a super class that will inherit all properties of probes and relays    
class Hardware(Temperature,Relay):
    def __init__(self,parameters,name):
        Temperature.__init__(self,parameters)
        Relay.__init__(self,parameters)
        self.name = name
        #list of actors connected to hw
        self.actorList = []
        #list of pins connected to hw
        self.pinList = []
        #staus of hw controls (boolean)
        self.hwStatus={}
        self.status = False

    #function to update the temp label associated with the hardware class
    def updateTempLabel(self):
        self.getTemp()
        if self.hwTemp:
            text = self.parameters.brewGUI[self.name]['tempGroupBox']['QLabelCurrentTemp']['widget'].text()
            text = text[:text.find('-->')+4]+'{}'.format(round(self.hwTemp,1))
            self.parameters.brewGUI[self.name]['tempGroupBox']['QLabelCurrentTemp']['widget'].setText(text)
        else:
            text = 'Current temperature --> no reading'
            self.parameters.brewGUI[self.name]['tempGroupBox']['QLabelCurrentTemp']['widget'].setText(text)

    #function to determine if relay connected to HW should be switched on - it will always be switched off if an off signal is recieved.
    def updateStatus(self):
        if 'TempTgt' in self.hwStatus:
            self.updateTempTgtStatus()
        self.status=all(list(self.hwStatus.values()))
        self.setPinStatus()

    #function to set status of pins
    def setPinStatus(self):
        for pin in self.pinList:
            self.parameters.activePins[pin][0] = self.status




def main():   
    app = QApplication(sys.argv)
    parameters = Parameters()
    controller = BreweryGUI(parameters)
    controller.show()
#    controller.timer.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()