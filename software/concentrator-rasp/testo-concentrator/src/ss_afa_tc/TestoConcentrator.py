#!/usr/bin/python
#
#
# Author : Damian Karbowiak
# Company: Silesian Softing
#
# Date   : 26.06.2017
#

from Configuration import Configuration
import pygatt
import logging

class TestoConcentrator:
    ##################################################################################################################
    # variables
    ##################################################################################################################
    #logger = FileLogger()                   # initialisation of logger
    configuration = None
    
    ##################################################################################################################
    # FUNCTIONS DEFINITION
    ##################################################################################################################
    # contructor
    def __init__(self):
        self.configuration = Configuration()

    ##################################################################################################################
    # MAIN CODE
    ##################################################################################################################
    def main(self):
        print "---Software configuration---"
        print "\t ---System---"
        print "\t\t debug:\t\t\t", self.configuration.debug
        print "\t\t filterDevices:\t\t", self.configuration.filterDevices
        print "\t\t simulationMode:\t", self.configuration.simulationMode
        print "\t\t maxDevicesCount:\t", self.configuration.maxDevicesCount
        print "\t ---Local database---"
        print "\t\t localIP:\t\t", self.configuration.localIP
        print "\t\t localPort:\t\t", self.configuration.localPort
        print "\t\t localUser:\t\t", self.configuration.localUser
        print "\t\t localPass:\t\t", self.configuration.localPass
        print "\t ---Remote database---"
        print "\t\t remoteEnable:\t\t", self.configuration.remoteEnable
        print "\t\t remoteIP:\t\t", self.configuration.remoteIP
        print "\t\t remotePort:\t\t", self.configuration.remotePort
        print "\t\t remoteUser:\t\t", self.configuration.remoteUser
        print "\t\t remotePass:\t\t", self.configuration.remotePass
        
        #logger configuration
        logging.basicConfig()
        logging.getLogger('pygatt').setLevel(logging.WARN)
        
        try:
            adapter = pygatt.GATTToolBackend()
            print "Avaible adapter: ", adapter._hci_device\
            
            print "Starting bluetooth adapter"
            adapter.start()
            
            connectedList = dict()
            print "Enter main loop"
            
            try:
                while 1:
                    print "Searching devices [5s}..."
                    devs = adapter.scan(timeout=5, run_as_root=True)
                    for dev in devs:                    
                        print "\tUrzadzenie ", dev["name"], " o adresie: ", dev["address"]
                        if not (dev['name'] in connectedList):
                            connectedList[dev["name"]] = dev["address"]
                            
                    
                    adapter.reset()
                    print connectedList
            except KeyboardInterrupt:
                print "Halt from keyboard"
        finally:
            print "Stopping bluetooth adapter"
            adapter.stop()
