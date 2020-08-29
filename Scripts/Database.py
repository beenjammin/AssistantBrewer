import os, csv
import glob
import time
from datetime import date
import pandas as pd
from pathlib import Path

class databaseManager():       
    def updateDatabase(self):
        self.data = pd.read_csv(self.fp)
        # print ('datafdrame is {}'.format(self.data.loc[:,['1','2']]))
        self.parameters.database['temperature'] = self.data
        self.headers = list(self.data)
        self.lastRow = self.data.iloc[[-1]]


class DatabaseFunctions():
    def __init__(self,parameters,probe):
        today = date.today()
        self.parameters = parameters
        self.parameters.brewDayFP
        self.probe = probe
        self.header = ['Time']+self.parameters.probes[probe]['actors']
        self.startTime = time.time()
    
    def updateDatabase(self):
        self.data = pd.read_csv(self.fp)
        # print ('datafdrame is {}'.format(self.data.loc[:,['1','2']]))
        #maybe can get rid of this and access via self.data
        self.parameters.database[self.probe] = self.data
        self.headers = list(self.data)
        self.lastRow = self.data.iloc[[-1]]

    def createFile(self):      
        i = 0
        while os.path.exists(self.parameters.brewDayFP+'/'+self.probe+'%s.csv' % i):
            i += 1
        self.fp = self.parameters.brewDayFP+'/'+self.probe+'_%s.csv' % i
        self.parameters.probes[self.probe]['fp'] = self.fp
        f = open(self.fp, "w")
        with f:
            writer = csv.writer(f)
            writer.writerow(self.header)
        f.close()
        print('created new file --> {}'.format(self.fp))
        self.appendRow(self.parameters.probes[self.probe]['readings'])
        self.appendRow(self.parameters.probes[self.probe]['readings'])
    
    def import_csv(self,csvfilename):
        data = []
        with open(csvfilename, "r", encoding="utf-8", errors="ignore") as scraped:
            reader = csv.reader(scraped, delimiter=',')
            for row in reader:
                if row:  # avoid blank lines
#                    row_index += 1
                    columns = row
                    data.append(columns)
        return data
                
    def appendRow(self,write_data):
        #add the latest readings to the csv file
        self.parameters.probes[self.probe]['readings'] = write_data
        f = open(self.fp, "a",newline='')
        print('writing data --> {}'.format(write_data))
        timeElapsed = (time.time()-self.startTime)/60
        write_data = [timeElapsed]+write_data
        with f:
            writer = csv.writer(f)
            writer.writerow(write_data)
        f.close()
