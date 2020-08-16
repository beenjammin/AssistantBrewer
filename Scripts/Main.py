from Vertical_Tabs import mainGUI
from Brewery_Parameters import Parameters
from Actor_Classes import actor_read_raw
from Database import csvFunctions
from time import sleep
import random
from threading import Thread



class intialiseBrewery():
    def __init__(self,parameters):
        print('initialising brewery')
        self.parameters = parameters
        print('starting another process')
        self.dataWrite = csvFunctions(self.parameters)
        self.dataWrite.createFile()
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
            print('writing data')
            readings = [actor_read_raw(a+'/w1_slave') for a in self.parameters.actors['actors']]
            self.dataWrite.appendRow(readings)
    
    def outputDataTest(self):
        print('writing data')
        while True:
            readings = [random.randint(30,55) for a in self.parameters.actors['actors']]
            print('writing data --> {}'.format(readings))
            self.dataWrite.appendRow(readings)
            sleep(5)

#    def initialiseGUI(self):        
#        b = mainGUI(self.parameters)
    
if __name__ == '__main__':
    parameters = Parameters()
    parameters.initialise()
    a = intialiseBrewery(parameters)
    
#    b = mainGUI(parameters)
    
