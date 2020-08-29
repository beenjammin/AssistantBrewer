#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 09:35:18 2020

@author: pi
"""
import sys

class Functions():
    def __init__(self):pass
#        self.parameters = parameters
    def getHWTemp(self, hw):
        try:
            self.parameters.brewGUI[hw]['object'].getTemp()
            return self.parameters.brewGUI[hw]['object'].temp
        except KeyError:
            print('cannot adjust for temperature without ph probe being assigned to hardware that also has a temperature probe attached ("connections tab")')        
            return 25
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
            
    def adjustPH(self, temp, ph):
        ph = float(ph)
        temp = float(temp)
        return str(ph + abs(ph-7.0)*.03*abs(temp-25)/10)