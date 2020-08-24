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


class csvFunctions():
    def __init__(self,parameters,probe):
        today = date.today()
        self.parameters = parameters
        self.parameters.brewDayFP
        self.name = probe
        self.header = ['Time']+self.parameters.probes[probe]['probes']
        self.startTime = time.time()

    def createFile(self):      
        i = 0
        while os.path.exists(self.parameters.brewDayFP+'/'+self.name+'%s.csv' % i):
            i += 1
        self.csv_fp = self.parameters.brewDayFP+'/'+self.name+'_%s.csv' % i
        self.parameters.probes[self.name]['fp'] = self.csv_fp
        f = open(self.csv_fp, "w")
        with f:
            writer = csv.writer(f)
            writer.writerow(self.header)
        f.close()
        print('created new file --> {}'.format(self.csv_fp))
        self.appendRow(self.parameters.probes[self.name]['readings'])
        self.appendRow(self.parameters.probes[self.name]['readings'])

    
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
        #add the latest readings to the dictionary
        self.parameters.probes[self.name]['readings'] = write_data
        f = open(self.csv_fp, "a",newline='')
        print('writing data --> {}'.format(write_data))
        timeElapsed = time.time()-self.startTime
        write_data = [timeElapsed]+write_data
        with f:
            writer = csv.writer(f)
            writer.writerow(write_data)
        f.close()
