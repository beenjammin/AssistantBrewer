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

from BreweryParameters import Parameters
from Widget_Styles import *

class BreweryGUI(QMainWindow):
    def __init__(self,parameters):
        super().__init__()
        self.parameters=parameters
        self.parameters.colour = 'grey'
        # self.setDockOptions(self.parameters._DOCK_OPTS)
        VLayoutP = QVBoxLayout()       
        for tempHardware in self.parameters.hardware['tempHardware']:
            self.parameters.hardwareDict[tempHardware]=[]
            
            dock = dockable(tempHardware)  
            gb = groupBox('Temperature')
            VLayout = QVBoxLayout()
            HLayout = QHBoxLayout()
            label = bodyLabel('Target temperature:')
            label2 = bodyLabel('Temperature tolerance:')
            VLayout.addWidget(label)
            VLayout.addWidget(label2)
            HLayout.addLayout(VLayout)

            tgtMashTemp = bodyLineEdit()
            tempMashTolerance = bodyLineEdit()
            self.parameters.hardwareDict[tempHardware].append(tgtMashTemp)
            self.parameters.hardwareDict[tempHardware].append(tempMashTolerance)
            VLayout = QVBoxLayout()
            VLayout.addWidget(tgtMashTemp)
            VLayout.addWidget(tempMashTolerance)
            HLayout.addLayout(VLayout)
            
            VLayout = QVBoxLayout()
            VLayout.addLayout(HLayout)
            HLayout = QHBoxLayout()
            currentTemp = bodyLabel('Current temperature --> no reading')
            currentPins = bodyLabel('Relay pins attached --> no relays attached')
            self.parameters.hardwareDict[tempHardware].append(currentTemp)
            HLayout.addWidget(currentTemp)        
            switch = bodyButton()
            switch.setText(tempHardware+' - Off')
            switch.setCheckable(True)
            switch.clicked.connect(lambda ignore, a=tempHardware:self.whichbtn(a))
            self.parameters.hardwareDict[tempHardware].append(switch)
            HLayout.addWidget(self.parameters.hardwareDict[tempHardware][3])
            VLayout.addLayout(HLayout)

            gb.setLayout(VLayout)          
            dock.setThisWidget(gb)
            self.addDockWidget(Qt.RightDockWidgetArea,dock)
      
        #Add other hardware
        HLayout = QHBoxLayout()
        pumps = groupBox("Pumps")
        for otherHardware in self.parameters.hardware['otherHardware']:
            self.parameters.hardwareDict[otherHardware]=[False,False,False]
            button = bodyButton()
            button.setText(otherHardware+' - Off')
            button.setCheckable(True)
            button.clicked.connect(lambda ignore, a=otherHardware:self.whichbtn(a))
            self.parameters.hardwareDict[otherHardware].append(button)
            HLayout.addWidget(button)

        pumps.setLayout(HLayout)
        dock = dockable('Other Hardware')            
        dock.setThisWidget(pumps)
        self.addDockWidget(Qt.RightDockWidgetArea,dock)
        
    def whichbtn(self,hardware):
        b = self.parameters.hardwareDict[hardware][3]
        hardwareName = b.text()[:b.text().find('-')-1]
#        print(hardwareName)
        if b.isChecked():
            b.setText(b.text()[:-6]+' - On')
            switch = True
        else:
            b.setText(b.text()[:-5]+' - Off')
            switch = False
        print('Trying to switch {}{}'.format(hardwareName,b.text()[b.text().find('-')+1:]))
        self.updatePins()
        if not self.parameters.allHardware[hardwareName]:
            print('Warning, no relays connected')
        for pin in self.parameters.allHardware[hardwareName]:
            #check status of pin and switch relay on or off
            self.relay(pin,switch)
            
#        if switch and not self.allHardware[hardwareName][0]:pass
#            #hardware is off an we need to switch it on
#        elif not switch and self.allHardware[hardwareName][0]:pass
            #hardware is on an we need to switch it off
    def relay(self,pin,switch):
        # GPIO.setmode(GPIO.BCM) 
        # RELAIS_1_GPIO = pin
        # GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
        if switch and not self.parameters.activePins[pin]:
            print('switching on {}'.format(pin))
            self.parameters.activePins[pin]=True
            # GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # turn on
        elif not switch and self.parameters.activePins[pin]:
            print('switching off {}'.format(pin))
            self.parameters.activePins[pin]=False
            # GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # turn on        
        
        
    def updatePins(self):
        #reset pins
        for hw in self.parameters.allHardware:
            self.parameters.allHardware[hw]=[]
        
        for count, pin in enumerate(self.parameters.activePins):
            a=self.parameters.relayComboBoxes[count].currentText()
            try:
                # print (pin)
                # print(self.relayComboBoxes[count].currentText())
                self.parameters.allHardware[self.parameters.relayComboBoxes[count].currentText()].append(pin)
            except: pass
                
def main():
    
    app = QApplication(sys.argv)
    parameters = Parameters()
    controller = BreweryGUI(parameters)
    controller.show()
#    controller.timer.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()