# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:25:59 2020

@author: BTHRO
"""

import sys, re
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json, ast

from Widget_Styles import *
# from Actor_Classes import *
from Event_Functions import EventFunctions
from Save_Load_Config import Config

class ConnectionsGUI(QMainWindow,EventFunctions,Config):
    def __init__(self,parameters):
        print('initiating connections GUI')     
        self.parameters = parameters
        super().__init__()
        # eF = EventFunctions(self.parameters)
        #Settings
        #Give user the option to set connections for relays
        VLayoutP = QVBoxLayout()  
        VLayout = QVBoxLayout()       
        relays = groupBox("Relays")
        self.headerFont = QFont()
        self.headerFont.setPointSize(11) 
        self.bodyFont = QFont()
        self.bodyFont.setPointSize(10)

        #set the pin connections
        self.parameters.connectionsGUI['relayDict'] = {}
        dall = {}
        dall.update(self.parameters.relayPins)
        dall.update(self.parameters.floatPins)
        print('relay pins in connections are {}'.format(self.parameters.relayPins))
        for label, pins in self.parameters.pins.items():
            lab = bodyLabel(re.sub(r'(?<!^)(?=[A-Z])', ' ', label).lower())
            VLayout.addWidget(lab)
            for pin in pins:
                HLayout = QHBoxLayout()
                pinLabel = bodyLabel()
                pinLabel.setText('Select control for pin {}'.format(pin))
                cb = bodyComboBox(ls=[label,pin])
                cb.addItems(['None']+list(self.parameters.relayHardware))
                if dall[pin][1]:
                    text = dall[pin][1]
                    index = cb.findText(text)
                    cb.setCurrentIndex(index)
                else:
                    text = None
                
                self.parameters.connectionsGUI ['relayDict'][pin]={  'QLabelRelay':{'widget':pinLabel},
                                                                    'QCBRelay':{'widget':cb,'value':text}}         
                cb.new_signal.connect(self.updatePins)
                HLayout.addWidget(pinLabel)
                HLayout.addWidget(cb)
                VLayout.addLayout(HLayout)
        relays.setLayout(VLayout)
        VLayoutP.addWidget(relays)
        

        #setting up connections to actors
#load the actors
        VLayout = QVBoxLayout()
        Actors = groupBox("Actors")
        HLayout = QHBoxLayout()    
        actorHeader = bodyLabel()
        actorHeader.setText('Actor')   
        actorHeader.setFont(self.headerFont)
        cbHeader = bodyLabel()
        cbHeader.setText('Connected hardware')   
        cbHeader.setFont(self.headerFont)
        rawOutput = bodyLabel()
        rawOutput.setText('Raw Reading')   
        rawOutput.setFont(self.headerFont)
        HLayout.addWidget(actorHeader)
        HLayout.addWidget(cbHeader)
        HLayout.addWidget(rawOutput)
        VLayout.addLayout(HLayout)
        
        self.parameters.connectionsGUI['actorDict'] = {}
        for probe in self.parameters.probes.keys():
            for count, actor in enumerate(self.parameters.probes[probe]['actors']):
                label = self.parameters.probes[probe]['dispName'][count]
                hw = self.parameters.probes[probe]['hw'][count]
                HLayout = QHBoxLayout()
                hwLabel = bodyLabel()
                hwLabel.setText('Select hardware for the {} actor'.format(label))
                rawReading = bodyLabel()
                rawReading.setText('none')
                cb = bodyComboBox(ls=[actor,probe])
                cb.addItems(['None']+list(self.parameters.tempHardware))
                cb.new_signal.connect(self.updateActors)
                if hw:
                    text = hw
                    index = cb.findText(text)
                    cb.setCurrentIndex(index)
                else:
                    text = None
                HLayout.addWidget(hwLabel)
                HLayout.addWidget(cb)
                HLayout.addWidget(rawReading)
                VLayout.addLayout(HLayout)
                self.parameters.connectionsGUI['actorDict'][actor]={    'QLabelActor':{'widget':hwLabel},
                                                                        'QCBActor':{'widget':cb,'value':text},
                                                                        'QLabelReading':{'widget':rawReading,'value':'none'}}

        self.assignProbeReadings()
           
        Actors.setLayout(VLayout)
        VLayoutP.addWidget(Actors)

        connections = groupBox("Connections") 
        connections.setLayout(VLayoutP)
        dock = dockable('Connections')            
        dock.addThisWidget(connections)
        dock.setCentralWidget()
        self.addDockWidget(Qt.RightDockWidgetArea,dock)
    

    def updatePins(self,lastitem, newitem, ls):
        #unpack list
        pinHW = ls[0] #the hardware that is connected to the Rpi pin
        pin = ls[1] #the pin that it is connected to on the Rpi

        if newitem != 'None':
            self.parameters.brewGUI[newitem]['object'].pinList[pinHW].append(pin)
            if pinHW == 'relay':
                    #update hardware entry in pin dictionary
                    self.parameters.relayPins[pin][1] = newitem
                    lbl = ', '.join(map(str,self.parameters.brewGUI[newitem]['object'].pinList[pinHW]))
                    self.parameters.brewGUI[newitem]['relayGroupBox']['QLabelCurrentPins']['widget'].setText('Relay pins attached --> {}'.format(lbl))
            #need to add something here so that float switch control is added to the hardware
            if pinHW == 'floatSwitch':
                #update hardware entry in float dictionary
                self.parameters.floatPins[pin][1] = newitem
                self.parameters.brewGUI[newitem]['object'].hwStatus['floatSwitch']=False
            # print(self.parameters.relayPins)
            print('added {} pin {} to {} and connected pins are now {}'.format(pinHW, pin, newitem, self.parameters.brewGUI[newitem]['object'].pinList[pinHW]))
        if lastitem != 'None':
            self.parameters.brewGUI[lastitem]['object'].pinList[pinHW].remove(pin)
            #now we check to see if it was a relay and update the widget with the relay text if required
            if pinHW == 'relay':
                if self.parameters.brewGUI[lastitem]['object'].pinList[pinHW]:
                    lbl = ', '.join(map(str,self.parameters.brewGUI[lastitem]['object'].pinList[pinHW]))
                    self.parameters.brewGUI[lastitem]['relayGroupBox']['QLabelCurrentPins']['widget'].setText('Relay pins attached --> {}'.format(lbl))
                else:
                    self.parameters.brewGUI[lastitem]['relayGroupBox']['QLabelCurrentPins']['widget'].setText('Relay pins attached --> no relays attached')
            #remove float switch control from hardware status dict
            if pinHW == 'floatSwitch':             
                self.parameters.brewGUI[newitem]['object'].hwStatus.pop('floatSwitch', None)

        #save the new configuration
        self.saveConnectionConfig()
       

    def updateActors(self,lastitem, newitem, ls):
        #runs on actor combobox change event - update associated actors, think this can be rewritten to only update relevent info
        # print('last item is {} and this item is {} and name is {}'.format(lastitem, newitem, actor))
        #unpack list
        actor = ls[0]
        probe = ls[1]
        #update plotGUI widgets
        if self.parameters.plotGUI['checkBoxes'][actor]['widget']: self.parameters.plotGUI['checkBoxes'][actor]['widget'].setText(newitem) 
        self.parameters.plotGUI['checkBoxes'][actor]['hw']=newitem

        #update brewGUI widgets NEED TO MODIFY THE updateTempLabel
        # print('newitem is {} and last item is {} and actor is {} and probe is {}'.format(newitem, lastitem, actor, probe))
        if newitem != 'None':
            self.parameters.brewGUI[newitem]['object'].probes[probe]['actors'].append(actor)
            self.parameters.brewGUI[newitem]['object'].updateTempLabel()
            print('added {} to {} and list is now {}'.format(actor, newitem, self.parameters.brewGUI[newitem]['object'].probes[probe]['actors']))
        if lastitem != 'None':
            self.parameters.brewGUI[lastitem]['object'].probes[probe]['actors'].remove(actor)
            self.parameters.brewGUI[lastitem]['object'].updateTempLabel()
            print('removed {} from {} and list is now {}'.format(actor, lastitem, self.parameters.brewGUI[lastitem]['object'].probes[probe]['actors']))
        
        self.parameters.probes[probe]['hw'][self.parameters.probes[probe]['actors'].index(actor)] = newitem

        #save the new configuration
        self.saveConnectionConfig()


        
def main():
    app = QApplication(sys.argv)
    parameters = Parameters()
    controller = SettingsGUI(parameters)
    controller.show()
#    controller.timer.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()