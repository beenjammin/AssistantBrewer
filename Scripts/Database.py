import os, csv
import glob
import time
from datetime import date
import pandas as pd


class databaseManager():       
    def refreshDatabase(self):
        self.data = pd.read_csv(self.fp)
        # print ('datafdrame is {}'.format(self.data.loc[:,['1','2']]))
        self.parameters.database['temperature'] = self.data
        self.headers = list(self.data)
        self.lastRow = self.data.iloc[[-1]]




class csvFunctions():
    def __init__(self,parameters):
        today = date.today()
        self.parameters = parameters
        self.name = 'brew_'+str(today).replace('-','_')
        self.header = ['Time']+self.parameters.actors['actors']
        self.startTime = time.time()
       
        
    def createFile(self):
        i = 0
        while os.path.exists(self.parameters.cwd+self.name+'%s.csv' % i):
            i += 1
        self.csv_fp = self.parameters.cwd+'/'+self.name+'_%s.csv' % i
        self.parameters.tempDatabaseFP = self.csv_fp
#        print (self.csv_fp)
        f = open(self.csv_fp, "w")
        with f:
            writer = csv.writer(f)
            writer.writerow(self.header)
        f.close()
        print('created new file --> {}'.format(self.csv_fp))
        self.appendRow(self.parameters.actors['readings'])
        self.appendRow(self.parameters.actors['readings'])

    
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
    

    def readLastRow(self):
#        f = open(self.parameters.tempDatabaseFP, "a")
        data = self.import_csv(self.parameters.tempDatabaseFP,)
        last_row = data[-1]
        self.parameters.actors['readings'] = last_row[1:]
        print('the last row is {}'.format(last_row[1:]))
#        f.close()    
        
        
    def appendRow(self,write_data):
        f = open(self.parameters.tempDatabaseFP, "a",newline='')
#        self.parameters.actors['readings'] = write_data
        timeElapsed = time.time()-self.startTime
        write_data = [timeElapsed]+write_data
        with f:
            writer = csv.writer(f)
            writer.writerow(write_data)
        f.close()
