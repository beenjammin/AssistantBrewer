#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 20:57:29 2020

@author: pi
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Actor_Classes import *

class MyTimer():
    def __init__(self,parameters,plot,tempDatabase):
        self.parameters = parameters
        self.plot = plot
        self.tempDatabase = tempDatabase
        
    def startTimer(self):   
        self.timer = QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.runFunctions)
        self.timer.start()
    
    def runFunctions(self):
        #this whole function can in a process
        if not self.parameters.test:
            self.parameters.actors['readings'] = [actor_read_raw(a+'/w1_slave') for a in self.parameters.actors['actors']]
        self.plot.updatePlot()
        
        