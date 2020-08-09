import os, csv
import glob
import time
from datetime import date
""" code modified from https://pimylifeup.com/raspberry-pi-temperature-sensor/"""

#function to return actors as a list
def getActors():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    home = '/home/pi/temperature_sensor'
    base_dir = '/sys/bus/w1/devices/'
    #Returns a list of all connected devices
    devices = [f.path for f in os.scandir(base_dir) if f.is_dir()]
    tempDevices = [x for x in devices if not 'master' in x]
    return tempDevices

#function to return the temperature of a given actor
def actor_read_raw(device_file):
    # we aer going to do something smart here to guess the device
    def read_raw(device_file):
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
    lines = read_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

    
#takes a device as 
class ReadDevice():
    def __init__(self,device_file):
        self.device_file = device_file
    def read_raw(self):
        f = open(self.device_file, 'r')
        self.lines = f.readlines()
        f.close()
    def read_temp(self):
        self.read_raw()
        while self.lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            self.lines = read_raw()
        equals_pos = self.lines[1].find('t=')
        if equals_pos != -1:
            temp_string = self.lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c



class csvFunctions():
    def __init__(self,parameters):
        today = date.today()
        self.parameters = parameters
        self.name = 'brew_'+str(today).replace('-','_')
        self.header = ['Time']+self.parameters.actors['actors']
        self.home = self.parameters.cwd
        self.startTime = time.time()

#        self.createFile()
        
        
    def createFile(self):
        i = 0
        while os.path.exists(self.home+self.name+'%s.csv' % i):
            i += 1
        self.csv_fp = self.home+'/'+self.name+'_%s.csv' % i
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


#tempDevices = getActors()
#Temperatures = csvFunctions(tempDevices)
#while True:
#    string = ''
#    ls = []
#    for count, device in enumerate(tempDevices):
#        a = ReadDevice(device+'/w1_slave')
#        ls.append(a.read_temp())
#        string += 'T{} = {} '.format(count+1, a.read_temp())
#    print(string)
#    Temperatures.append(ls)
#    time.sleep(1)