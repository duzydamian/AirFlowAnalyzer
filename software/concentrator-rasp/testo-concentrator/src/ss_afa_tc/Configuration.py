#!/usr/bin/python
#
#
# Author : Damian Karbowiak
# Company: Silesian Softing
#
# Date   : 26.06.2017
#

##################################################################################################################
# IMPORT LIBRARIES
##################################################################################################################
import ConfigParser

class Configuration(object):
    ##################################################################################################################
    # variables
    ##################################################################################################################
    configPath = '/opt/ss/testo/config.cfg'
    config = None
    #logger = None
    # parameters from config file
    # System    
    debug = False
    filterDevices = False
    simulationMode = False
    maxDevicesCount = 5
    
    # Local database
    localIP = "127.0.0.1"
    localPort = 502
    localUser = 'posgtres'
    localPass = 'postgres'
    
    # Remote database
    remoteEnable = False
    remoteIP = "192.168.1.100"
    remotePort = 502
    remoteUser = 'posgtres'
    remotePass = 'postgres'
    
    ##################################################################################################################
    # FUNCTIONS DEFINITION
    ##################################################################################################################
    # constructor        
    #def __init__(self, logger, path = '/opt/ss/testo/config.cfg'):
    def __init__(self, path = '/opt/ss/testo/config.cfg'):
        self.configPath = path
        #self.logger = logger
        self.config = ConfigParser.ConfigParser()
        try:
            ret = self.config.read(self.configPath)
            if (len(ret)==0):
                #self.logger.logWarning("Can't read config file: " + self.configPath, self)
                print "Can't read config file: " , self.configPath
                self.setDeafultConfig()
                self.parseConfig()
            else:
                #self.logger.logWarning("Loaded config file: " + self.configPath, self)
                print "Loaded config file: ", self.configPath
                self.parseConfig()
        except ConfigParser.NoOptionError:
            #self.logger.logWarning("Can't parse config file: " + self.configPath, self)
            print "Can't parse config file: ", self.configPath
            self.setDeafultConfig()
            self.parseConfig()
    
    # function reads configuration from file if exists
    def parseConfig(self):
        self.config.read(self.configPath)
        
        self.debug = self.config.getboolean('System', "debug")
        self.filterDevices = self.config.getboolean('System', "filterDevices")
        self.simulationMode = self.config.getboolean('System', "simulationMode")
        self.maxDevicesCount = self.config.getint('System', "maxDevicesCount")
        
        self.localIP = self.config.get('LocalDatabase', "localIP")
        self.localPort = self.config.getint('LocalDatabase', "localPort")
        self.localUser = self.config.get('LocalDatabase', "localUser")
        self.localPass = self.config.get('LocalDatabase', "localPass")

        self.remoteEnable = self.config.getboolean('RemoteDatabase', "remoteEnable")
        self.remoteIP = self.config.get('RemoteDatabase', "remoteIP")
        self.remotePort = self.config.getint('RemoteDatabase', "remotePort")
        self.remoteUser = self.config.get('RemoteDatabase', "remoteUser")
        self.remotePass = self.config.get('RemoteDatabase', "remotePass")
                
    # function create default values to parameters if file doesn't exist
    def setDeafultConfig(self):
        #self.logger.logText('Created default config file'+self.configPath, self)
        print 'Created default config file', self.configPath
        self.config = ConfigParser.ConfigParser()
        
        self.config.add_section('System')
        self.config.set('System', "debug", self.debug)
        self.config.set('System', "filterDevices", self.filterDevices)
        self.config.set('System', "simulationMode", self.simulationMode)
        self.config.set('System', "maxDevicesCount", self.maxDevicesCount)
        
        self.config.add_section('LocalDatabase')
        self.config.set('LocalDatabase', "localIP", self.localIP)
        self.config.set('LocalDatabase', "localPort", self.localPort)
        self.config.set('LocalDatabase', "localUser", self.localUser)
        self.config.set('LocalDatabase', "localPass", self.localPass)

        
        self.config.add_section('RemoteDatabase')
        self.config.set('RemoteDatabase', "remoteEnable", self.remoteEnable)
        self.config.set('RemoteDatabase', "remoteIP", self.remoteIP)
        self.config.set('RemoteDatabase', "remotePort", self.remotePort)
        self.config.set('RemoteDatabase', "remoteUser", self.remoteUser)
        self.config.set('RemoteDatabase', "remotePass", self.remotePass)

        
        f = open(self.configPath,'w')
        self.config.write(f)            