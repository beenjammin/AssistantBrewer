from probeTypes.DS18B20 import getActors, actor_read_raw
from probeTypes.Atlas import atlas_i2c
from Database import DatabaseFunctions

class Probe_Initialise():
    """check for probe types that exist and assign functionality for that probe"""
    def __init__(self, parameters):
        super(Probe_Initialise, self).__init__()
        print('checking for probes attached')
        self.parameters = parameters

        
        self.DS18B20()
        self.atlasProbes()


        #this goes last
        self.addTestData()
        self.finaliseProbes()
        self.initialiseDatabases()
        self.parameters.allActors = []
        for key in self.parameters.probes.keys():
            self.parameters.allActors += self.parameters.probes[key]['actors']
        #set the dictionary for checkboxes and initialise
        self.parameters.plotGUI['checkBoxes']={}
        for actor in self.parameters.allActors:
            self.parameters.plotGUI['checkBoxes'][actor]={'hw':None,'widget':None,'state':True}

    def initialiseDatabases(self):
        #initialising databases
        for probe in self.parameters.probes.keys():
            print('initialising database for {}'.format(probe))
            self.parameters.probes[probe]['databaseClass'] = DatabaseFunctions(self.parameters,probe)
            self.parameters.probes[probe]['databaseClass'].createFile()

    def atlasProbes(self):
        #use the atlas scientific I2C protocol
        for probe, address in self.parameters.I2C.items():
            try:
                actor = atlas_i2c(address=int(address))
#                print(actor.query("R"))
                self.parameters.probes[probe]['actors'] += [address]
                #populate field for hardware
                self.parameters.probes[probe]['hw'] += [None]
                self.parameters.probes[probe]['readings'] += [actor.query("R").rstrip('\x00')]
                #add the protocol to the dict
                self.parameters.probes[probe]['protocol'] += ['Atlas_I2C']
                self.parameters.probes[probe]['probeClass'] += [actor]
                print('found a {} probe using the Atlas I2C protocol on I2C address {}'.format(probe, address))
                self.parameters.test = False
            except: pass
        if self.parameters.test: print("Didn't find any atlas probes using the I2C protocol")

    def DS18B20(self):
        #use the 1 wire DS18B20 temperature protocol
        DS18B20_Probes = getActors()      
        if DS18B20_Probes:
            self.parameters.probes['temperature']['actors'] += DS18B20_Probes
            print('Found {} temp probes using the DS18B20 protocol'.format(len(DS18B20_Probes)))
            #populate field for hardware
            self.parameters.probes['temperature']['hw'] += [None]*len(DS18B20_Probes)
            self.parameters.probes['temperature']['readings'] += [actor_read_raw(probe+'/w1_slave') for probe in DS18B20_Probes]
            #add the protocol to the dict
            self.parameters.probes['temperature']['protocol'] += ['DS18B20']*len(DS18B20_Probes)
            self.parameters.probes['temperature']['probeClass'] += [None]*len(DS18B20_Probes)
            self.parameters.test = False
        else:
            print("Didn't find any temp probes using the DS18B20 protocol")
        
    def addTestData(self):
        #test to see if there are any probes and add some sample data if not
        if not self.parameters.probes['temperature']['actors']:
            print('no temp probes, generating sample data for temp probes')
            self.parameters.probes['temperature']['actors']     = ['T1','T2','T3']
            self.parameters.probes['temperature']['readings']   = [10,25,30]
            self.parameters.probes['temperature']['hw']         = [None,None,None]
            self.parameters.probes['temperature']['protocol']   =  ['test','test','test']

        #test to see if there are any probes and add some sample data if not
        if not self.parameters.probes['ph']['actors']:  
            print('no ph probes, generating sample data for ph probes')                                         
            self.parameters.probes['ph']['actors']     = ['ph1','ph2']
            self.parameters.probes['ph']['readings']   = [5,6,]
            self.parameters.probes['ph']['hw']         = [None,None]
            self.parameters.probes['ph']['protocol']   =  ['test','test']
            
    def finaliseProbes(self):
        for probe in self.parameters.probes.keys():
            self.parameters.probes[probe]['dispName']   = [probe[:4] + a for a in self.parameters.probes[probe]['protocol']]
                