# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:34:55 2020

@author: BTHRO
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Parameters():
    def __init__(self):
        #{pin:last state} 
        self.activePins = {17:False,22:False,23:False,27:False}
        #Add hardware to dictionary to populate GUI     
        self.hardware = {'tempHardware':['HLT','Mash','Boil'],
                         'otherHardware':['Pump 1','Pump 2']}

        self.colours = {'black':'#000000','grey1':'#383838','grey2':'#616161','grey3':'#999999','white':'#ffffff'}
        #Dictionaries for GUI
        #user inputs as a dictionary{hardware: Status, Target tempature, Temperature tolerance, Actor}
        self.userInputs={}
        #Actor inputs as a dictionary{HLT: Status, Target tempature, Temperature tolerance, Actor}       
        self.actorTemps = {}
        #pins
        self.allHardware = {}
        
        for key in self.hardware:
            for hw in self.hardware[key]:
                 self.allHardware[hw] = []
        
        self.headerFont = QFont()
        self.headerFont.setPointSize(14)
        
        self.bodyFont = QFont()
        self.bodyFont.setPointSize(10)
        
        self.relayComboBoxes = []
        self.actorComboBoxes = []
        self.actors = ['1','2','3']#getActors()
        
        #Actor inputs as a dictionary{hardware: tgtTemp, tgtTolerance, tempReading, on/off switch,}
        self.hardwareDict={}
        
class groupBox(QGroupBox):
    def __init__(self, *args, **kwargs):
        QGroupBox.__init__(self, *args, **kwargs)
        stylesheet = """ 
                    QGroupBox {border: 1px solid black;
                    border-radius: 9px;
                    margin-top: 0.5em}
                    QGroupBox::title {subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 3px 0 3px;
                    }
                    """
        self.setStyleSheet(stylesheet)
        
        
class bodyLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        stylesheet = """ 
                    QLabel {color : #999999}
                    """
        self.setStyleSheet(stylesheet)
        

class bodyButton(QPushButton):
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        stylesheet = """ 
                    QPushButton {background-color: #616161; border: none; color : #999999}
                    QPushButton:checked {background-color: #33524c; border: none;color: white}
                    """
        self.setStyleSheet(stylesheet)
        
class dockable(QDockWidget):
    def __init__(self, *args, **kwargs):
        QDockWidget.__init__(self, *args, **kwargs)
        stylesheet = """ 
                    QDockWidget::title {background: black; color : white}
                    """
        self.setStyleSheet(stylesheet)


