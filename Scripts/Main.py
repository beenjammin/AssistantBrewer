from Vertical_Tabs import mainGUI
from Brewery_Parameters import Parameters
from Actor_Classes import csvFunctions, actor_read_raw
from time import sleep
from multiprocessing import Process



class intialiseBrewery():
    def __init__(self,parameters):
        print('initialising brewery')
        self.parameters = parameters
        print('starting another process')
        self.dataWrite = csvFunctions(self.parameters)
        self.dataWrite.createFile()
        if not self.parameters.test:
            p1 = Process(target=self.outputData)
        # else: 
        #     p1 = Process(target=self.outputDataTest)
        # p1.start()
        print('loading GUI')
        b = mainGUI(self.parameters)

    def outputData(self):
        while True:
            print('writing data')
            readings = [actor_read_raw(a+'/w1_slave') for a in self.parameters.actors['actors']]
            self.dataWrite.appendRow(readings)
    
    def outputDataTest(self):
        while True:
            print('writing data')
            readings = [random.randint(30,55) for a in self.parameters.actors['actors']]
            self.dataWrite.appendRow(readings)
            sleep(5)

#    def initialiseGUI(self):        
#        b = mainGUI(self.parameters)
    
if __name__ == '__main__':
    parameters = Parameters()
    parameters.initialise()
    a = intialiseBrewery(parameters)
    
#    b = mainGUI(parameters)
    
