from Vertical_Tabs import mainGUI
from Brewery_Parameters import Parameters
from probeTypes.DS18B20 import actor_read_raw
from probeTypes.Probes_Init import Probe_Initialise
from Database import DatabaseFunctions
from time import sleep
import random
from threading import Thread



class intialiseBrewery():
    def __init__(self,parameters):
        print('initialising brewery')
        self.parameters = parameters
        a = Probe_Initialise(self.parameters)
        # self.dataWrite = DatabaseFunctions(self.parameters)
        # self.dataWrite.createFile()

        print('starting another process')
        if not self.parameters.test:
            p1 = Thread(target=self.outputData)
        else: 
            p1 = Thread(target=self.outputDataTest)
        try:
            p1.start()
        except:
            print('starting process failed')
        print('loading GUI')
        b = mainGUI(self.parameters)
        print('done')
        p1.join()   

    def outputData(self):
        while True:
            #split this out into I2C readings and DS18B20 and test
            for probe in self.parameters.probes.keys():
                readings = []
                for count, protocol in enumerate(self.parameters.probes[probe]['protocol']):
                    if probe == 'temperature':
                        if protocol == 'test':
                            readings += [random.randint(30,55)]
                        elif protocol == 'DS18B20':
                            readings += [actor_read_raw(self.parameters.probes[probe]['probes'][count]+'/w1_slave')]
                        elif protocol == 'I2C':
                            print("don't have I2C functionality yet")
                        else:
                            print('unidentified protocol for temp probe in probe dictionary')
                            raise
                    elif probe == 'ph':
                        if protocol == 'I2C':
                            print("don't have I2C functionality yet")
                        elif protocol == 'test':
                            readings += [random.randint(5,7)]
                        else:
                            print('unidentified protocol for ph probe in probe dictionary')
                # print('writing data --> {}'.format(readings))
                self.parameters.probes[probe]['databaseClass'].appendRow(readings)
    
    def outputDataTest(self):
        print('writing data')
        while True:
            for probe in self.parameters.probes.keys():
                readings = []
                for protocol in self.parameters.probes[probe]['protocol']:
                    if protocol == 'test':
                        if probe == 'temperature':
                            readings += [random.randint(30,55)]  
                        elif probe == 'ph':
                            readings += [random.randint(5,7)]                     
                # print('writing data --> {}'.format(readings))
                self.parameters.probes[probe]['databaseClass'].appendRow(readings)
            sleep(5)

#    def initialiseGUI(self):        
#        b = mainGUI(self.parameters)
    
if __name__ == '__main__':
    parameters = Parameters()
    parameters.initialise()
    a = intialiseBrewery(parameters)
    
#    b = mainGUI(parameters)
    
