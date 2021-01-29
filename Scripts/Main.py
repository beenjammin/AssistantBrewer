from Vertical_Tabs import mainGUI
from Brewery_Parameters import Parameters
from probeTypes.DS18B20 import actor_read_raw
from probeTypes.Probes_Init import Probe_Initialise
from probeTypes.Float_Switch import FloatSwitch
from Database import DatabaseFunctions
from Brewery_Functions import Functions
from time import sleep
import random
from threading import Thread
from Save_Load_Config import Config



class intialiseBrewery(Functions,Config):
    def __init__(self,parameters):
        print('initialising brewery')
        self.parameters = parameters
        super().__init__()
        a = Probe_Initialise(self.parameters)
        # self.dataWrite = DatabaseFunctions(self.parameters)
        # self.dataWrite.createFile()
        self.loadConfig()
        print('starting another process')
        if not self.parameters.test:
            p1 = Thread(target=self.outputData)
            #test to see if we have any float pins
#            if self.parameters.floatPins:
#                p2 = Thread(target=self.pollFloatSwitch)
        else: 
            p1 = Thread(target=self.outputDataTest)
        try:
            p1.start()
#            p2.start()
        except:
            print('starting process failed')
        #going too add another process for quick polling, so far only the float switch is in here
        #add thread for float switch and send signal on trigger
        print('loading GUI')
        b = mainGUI(self.parameters)
        print('done')
        p1.join()  
        # p2.join()
    
    def pollFloatSwitch(self):
        lst = [FloatSwitch(pin) for pin in self.parameters.floatPins]
        while True:
            for floatSwitch, pin in zip(lst, self.parameters.floatPins.keys()):
                #check if pin has hw assigned
                hw = self.parameters.floatPins[pin][1]
                if hw:
                    if floatSwitch.switchState():
                        self.parameters.brewGUI[hw]['object'].hwStatus['floatSwitch']=not(floatSwitch.thisState)
                        relayPins = self.parameters.brewGUI[hw]['object'].pinList['relay']
                        if relayPins:
                            self.parameters.brewGUI[hw]['object'].checkRelayPinStatus(relayPins)
            sleep(1)
                
        
    def outputData(self):
        while True:
            #split this out into I2C readings and DS18B20 and test
#            self.pollFloatSwitch()
            for probe in self.parameters.probes.keys():
                readings = []
                for count, protocol in enumerate(self.parameters.probes[probe]['protocol']):
                    if probe == 'temperature':
                        if protocol == 'test':
                            readings += [random.randint(30,55)]
                        elif protocol == 'DS18B20':
                            readings += [actor_read_raw(self.parameters.probes[probe]['actors'][count]+'/w1_slave')]
                        elif protocol == 'Atlas_I2C':
                            print(self.parameters.probes[probe]['probeClass'][count].query("R"))
                            readings += [self.parameters.probes[probe]['probeClass'][count].query("R").rstrip('\x00')]
                        else:
                            print('unidentified protocol for temp probe in probe dictionary')
                            raise
                    elif probe == 'ph':
                        if protocol == 'Atlas_I2C':
                            rawPH = self.parameters.probes[probe]['probeClass'][count].query("R").rstrip('\x00')
                            if self.parameters.phTempAdjust:
                                temp = self.getHWTemp(self.parameters.probes[probe]['hw'][count])
                                rawPH = self.adjustPH(temp,rawPH)
                            readings += [rawPH]
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
    
