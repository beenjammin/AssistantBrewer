from probeTypes.DS18B20 import getActors
from Database import DatabaseFunctions

class Probe_Initialise():
    """check for probe types that exist and assign functionality for that probe"""
    def __init__(self, parameters):
        super(Probe_Initialise, self).__init__()
        print('checking for probes attached')
        self.parameters = parameters

        self.atlasProbes()
        self.DS18B20()


        #this goes last
        self.addTestData()
        self.initialiseDatabases()

    def initialiseDatabases(self):
        #initialising databases
        for probe in self.parameters.probes.keys():
            print('initialising database for {}'.format(probe))
            self.parameters.probes[probe]['databaseClass'] = DatabaseFunctions(self.parameters,probe)
            self.parameters.probes[probe]['databaseClass'].createFile()

    def atlasProbes(self):
        #use the atlas scientific I2C protocol
        print("Didn't find any atlas probes using the I2C protocol")
        pass

    def DS18B20(self):
        #use the 1 wire DS18B20 temperature protocol
        DS18B20_Probes = getActors()      
        if DS18B20_Probes:
            self.parameters.probes['temperature']['probes'] += DS18B20_Probes
            print('Found {} temp probes using the DS18B20 protocol'.format(len(DS18B20_Probes)))
            #populate field for hardware
            self.parameters.probes['temperature']['hw'] = [None]*len(DS18B20_Probes)
            #add the protocol to the dict
            self.parameters.probes['temperature']['protocol'] = ['DS18B20']*len(DS18B20_Probes)
            self.parameters.test = False
        else:
            print("Didn't find any temp probes using the DS18B20 protocol")
        
    def addTestData(self):
        #test to see if there are any probes and add some sample data if not
        if not self.parameters.probes['temperature']['probes']:
            print('no temp probes, generating sample data for temp probes')
            self.parameters.probes['temperature']['probes']     = ['T1','T2','T3']
            self.parameters.probes['temperature']['readings']   = [10,25,30]
            self.parameters.probes['temperature']['hw']         = [None,None,None]
            self.parameters.probes['temperature']['protocol']   =  ['test','test','test']

        #test to see if there are any probes and add some sample data if not
        if not self.parameters.probes['ph']['probes']:  
            print('no ph probes, generating sample data for ph probes')                                         
            self.parameters.probes['ph']['probes']     = ['ph1','ph2']
            self.parameters.probes['ph']['readings']   = [5,6,]
            self.parameters.probes['ph']['hw']         = [None,None]
            self.parameters.probes['ph']['protocol']   =  ['test','test']