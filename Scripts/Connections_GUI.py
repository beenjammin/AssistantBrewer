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

class ConnectionsGUI(QMainWindow,EventFunctions):
    def __init__(self,parameters):
        print('initiating connections GUI')
        super().__init__()
        self.parameters = parameters
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

        self.parameters.connectionsGUI['relayDict'] = {}
        for label, pins in self.parameters.pins.items():
            lab = bodyLabel(re.sub(r'(?<!^)(?=[A-Z])', ' ', label).lower())
            VLayout.addWidget(lab)
            for pin in pins:
                HLayout = QHBoxLayout()
                pinLabel = bodyLabel()
                pinLabel.setText('Select control for pin {}'.format(pin))
                cb = bodyComboBox(ls=[label,pin])
                cb.addItems(['None']+list(self.parameters.relayHardware))
                self.parameters.connectionsGUI ['relayDict'][pin]={  'QLabelRelay':{'widget':pinLabel},
                                                                    'QCBRelay':{'widget':cb,'value':None}}         
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
                HLayout = QHBoxLayout()
                hwLabel = bodyLabel()
                hwLabel.setText('Select hardware for the {} actor'.format(label))
                rawReading = bodyLabel()
                rawReading.setText('none')
                cb = bodyComboBox(ls=[actor,probe])
                cb.addItems(['None']+list(self.parameters.tempHardware))
                cb.new_signal.connect(self.updateActors)
                HLayout.addWidget(hwLabel)
                HLayout.addWidget(cb)
                HLayout.addWidget(rawReading)
                VLayout.addLayout(HLayout)
                self.parameters.connectionsGUI['actorDict'][actor]={    'QLabelActor':{'widget':hwLabel},
                                                                        'QCBActor':{'widget':cb,'value':None},
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


        #Could change this to just update based on combobox targeted, currently updates all for each focus event
        #reset pins
        # for key, value in self.parameters.brewGUI.items():
        #     # print('key is {}'.format(key))
        #     # print('value is {}'.format(value))
        #     try:
        #         value['relayGroupBox']
        #         text = 'Relay pins attached --> no relays attached'
        #         self.parameters.brewGUI[key]['object'].pinList=[]
        #         self.parameters.brewGUI[key]['relayGroupBox']['QLabelCurrentPins']['widget'].setText(text)
        #         self.parameters.brewGUI[key]['relayGroupBox']['QLabelCurrentPins']['value']='no relays attached'
        #     #This hardware has no relay attached so we ignore it
        #     except KeyError:
        #         print('{} has no relay'.format(key))        
        #     except:
        #         print("Unexpected error:", sys.exc_info()[0])
        #         raise
        #updating the brewGUI dictionary
        if newitem != 'None':
            self.parameters.brewGUI[newitem]['object'].pinList[pinHW].append(pin)
            if pinHW == 'relay':
                    #update hardware entry in pin dictionary
                    self.parameters.relayPins[pin][1] = newitem
                    lbl = ', '.join(map(str,self.parameters.brewGUI[newitem]['object'].pinList[pinHW]))
                    self.parameters.brewGUI[newitem]['relayGroupBox']['QLabelCurrentPins']['widget'].setText('Relay pins attached --> {}'.format(lbl))
            #need to add something here so that float switch control is added to the hardware
            if pinHW == 'floatSwitch':
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


            # print('remove {} from {} and list is now {}'.format(actor, lastitem, self.parameters.brewGUI[lastitem]['object'].actorList[probe]))

        # for key, value in self.parameters.connectionsGUI['relayDict'].items():
        #     #set the relay pin
        #     pin = key
        #     #set the combobox in the GUI associated with the pin
        #     cb = value['QCBRelay']['widget']
        #     #get the combox value
        #     hw = cb.currentText()
        #     #update the dictionary, adding the selected combobox value for the pin
        #     value['QCBRelay']['value'] = hw
        #     #going to try and add the associate the pin with the hardware
        #     self.parameters.relayPins[pin][1] = hw
        #     try:
        #         #check if hw is in the list, if not, display default text
        #         if hw in list(self.parameters.hardware):
        #             self.parameters.brewGUI[hw]['object'].pinList['relay'].append(pin)
        #             if self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['value'] == 'no relays attached':
        #                 self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['widget'].setText('Relay pins attached --> no relays attached')
        #             #add the pin to the dictionary
        #             text = self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['widget'].text()
        #             #updating the GUI with hardware connected pins
        #             text +=' {}'.format(pin)
        #             self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['widget'].setText(text)                       
        #     except:
        #         print("Unexpected error:", sys.exc_info()[0])
        #         raise
        

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


        
def main():
    app = QApplication(sys.argv)
    parameters = Parameters()
    controller = SettingsGUI(parameters)
    controller.show()
#    controller.timer.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()