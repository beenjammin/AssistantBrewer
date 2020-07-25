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

from Widget_Styles import *
from Event_Functions import *

class SettingsGUI(QMainWindow):
    def __init__(self,parameters):
        super().__init__()
        self.parameters=parameters
        eF = EventFunctions(self.parameters)
        #Settings
        #Give user the option to set connections for relays
        VLayoutP = QVBoxLayout()  
        VLayout = QVBoxLayout()       
        relays = groupBox("Relays")

        self.parameters.settingsGUI['relayDict'] = {}
        for relay in self.parameters.activePins:
            HLayout = QHBoxLayout()
            relayLabel = bodyLabel()
            relayLabel.setText('Select control for pin {}'.format(relay))
            cb = bodyComboBox()
            cb.addItems(['None']+list(self.parameters.hardware))
            self.parameters.relayComboBoxes.append(cb)
            self.parameters.settingsGUI ['relayDict'][relay]={  'QLabelRelay':{'widget':relayLabel},
                                                                'QCBRelay':{'widget':cb,'value':None}}
            
            cb.activated.connect(lambda:eF.updatePins())
            HLayout.addWidget(relayLabel)
            HLayout.addWidget(cb)
            VLayout.addLayout(HLayout)
        relays.setLayout(VLayout)
        VLayoutP.addWidget(relays)
             
        VLayout = QVBoxLayout()
        Actors = groupBox("Actors")
        self.parameters.settingsGUI['actorDict'] = {}
        for key, value in list(self.parameters.hardware.items()):
            if value[0]:
                print(key)
                HLayout = QHBoxLayout()
                hwLabel = bodyLabel()
                hwLabel.setText('Select actor for the {}'.format(key))
                cb = bodyComboBox()
                cb.addItems(['None']+(self.parameters.actors))
                self.parameters.actorComboBoxes.append(cb)
                HLayout.addWidget(hwLabel)
                HLayout.addWidget(cb)
                VLayout.addLayout(HLayout)
                self.parameters.settingsGUI['actorDict'][key]={    'QLabelActor':{'widget':hwLabel},
                                                                    'QCBActor':{'widget':cb,'value':None}}

        # self.parameters.settingsGUI = {'relayDict':relayDict,'actorDict':actorDict}
        
        #load the actors
        HLayout = QHBoxLayout()    
        actorHeader = bodyLabel()
        actorHeader.setText('Actor')   
        actorHeader.setFont(self.parameters.headerFont)
        rawOutput = bodyLabel()
        rawOutput.setText('Raw Reading')   
        rawOutput.setFont(self.parameters.headerFont)
        HLayout.addWidget(actorHeader)
        HLayout.addWidget(rawOutput)
        VLayout.addLayout(HLayout)
        
        #load the raw output of each actor
        self.rawOutput_list = []   
        for count, actor in enumerate(self.parameters.actors):
            HLayout = QHBoxLayout()  
            actorLabel = bodyLabel()
            actorLabel.setText(actor)   
            rawReading = bodyLabel()
            rawReading.setText('none')   
            self.rawOutput_list.append(rawReading)
            HLayout.addWidget(actorLabel)
            HLayout.addWidget(rawReading)
            VLayout.addLayout(HLayout)
        self.clickedUpdateReadings()
        
        updateReadings = bodyButton('Update Readings')
        updateReadings.clicked.connect(self.clickedUpdateReadings)
        VLayout.addWidget(updateReadings,alignment=Qt.AlignRight)   
        Actors.setLayout(VLayout)
        VLayoutP.addWidget(Actors)

        connections = groupBox("Connections") 
        connections.setLayout(VLayoutP)
        dock = dockable('Settings')            
        dock.addThisWidget(connections)
        dock.setCentralWidget()
        self.addDockWidget(Qt.RightDockWidgetArea,dock)
        

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