# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:25:59 2020

@author: BTHRO
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json, ast

from BreweryParameters import Parameters

class SettingsGUI(QMainWindow):
    def __init__(self,parameters):
        super().__init__()
        self.parameters=parameters
        #Settings
        #Give user the option to set connections for relays
        VLayoutP = QVBoxLayout()  
        VLayout = QVBoxLayout()       
        relays = QGroupBox("Relays")
        
        for relay in self.parameters.activePins:
            HLayout = QHBoxLayout()
            relayLabel = QLabel()
            relayLabel.setText('Select control for pin {}'.format(relay))
            cb = QComboBox()
            cb.addItems(['None']+self.parameters.hardware['tempHardware']+self.parameters.hardware['otherHardware'])
            self.parameters.relayComboBoxes.append(cb)
            HLayout.addWidget(relayLabel)
            HLayout.addWidget(cb)
            VLayout.addLayout(HLayout)
        relays.setLayout(VLayout)
        VLayoutP.addWidget(relays)
        
        
        VLayout = QVBoxLayout()
        Actors = QGroupBox("Actors")
        
        for probe in self.parameters.hardware['tempHardware']:
            HLayout = QHBoxLayout()
            probeLabel = QLabel()
            probeLabel.setText('Select actor for the {}'.format(probe))
            cb = QComboBox()
            cb.addItems(['None']+(self.parameters.actors))
            self.parameters.actorComboBoxes.append(cb)
            HLayout.addWidget(probeLabel)
            HLayout.addWidget(cb)
            VLayout.addLayout(HLayout)
        
        #load the actors
        HLayout = QHBoxLayout()    
        actorHeader = QLabel()
        actorHeader.setText('Actor')   
        actorHeader.setFont(self.parameters.headerFont)
        rawOutput = QLabel()
        rawOutput.setText('Raw Reading')   
        rawOutput.setFont(self.parameters.headerFont)
        HLayout.addWidget(actorHeader)
        HLayout.addWidget(rawOutput)
        VLayout.addLayout(HLayout)
        
        #load the raw output of each actor
        self.rawOutput_list = []   
        for count, actor in enumerate(self.parameters.actors):
            HLayout = QHBoxLayout()  
            actorLabel = QLabel()
            actorLabel.setText(actor)   
            rawReading = QLabel()
            rawReading.setText('none')   
            self.rawOutput_list.append(rawReading)
            HLayout.addWidget(actorLabel)
            HLayout.addWidget(rawReading)
            VLayout.addLayout(HLayout)
        self.clickedUpdateReadings()
        
        updateReadings = QPushButton('Update Readings')
        updateReadings.clicked.connect(self.clickedUpdateReadings)
        VLayout.addWidget(updateReadings,alignment=Qt.AlignRight)   
        Actors.setLayout(VLayout)
        VLayoutP.addWidget(Actors)

        connections = QGroupBox("Connections") 
        connections.setLayout(VLayoutP)
        dockSetting = QDockWidget('Settings')            
        dockSetting.setWidget(connections)
        self.addDockWidget(Qt.RightDockWidgetArea,dockSetting)
        
    def clickedUpdateReadings(self):
        rawReadings = [10,25,30]#[actor_read_raw(a+'/w1_slave') for a in self.actors]
        for count, a in enumerate(self.parameters.actors):
            self.parameters.actorTemps[a]=rawReadings[count]
        print (rawReadings)
        for count, label in enumerate(self.rawOutput_list):
            label.setText(str(rawReadings[count]))        
        
        
def main():
    
    app = QApplication(sys.argv)
    parameters = Parameters()
    controller = SettingsGUI(parameters)
    controller.show()
#    controller.timer.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()