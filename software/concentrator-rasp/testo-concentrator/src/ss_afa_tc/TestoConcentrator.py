#!/usr/bin/python
#
#
# Author : Damian Karbowiak
# Company: Silesian Softing
#
# Date   : 26.06.2017
#

from Configuration import Configuration
from TestoDevice import TestoDevice
import pygatt
import logging
import sys


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
            self.adapters = []
            for i in range(0, self.configuration.maxDevicesCount):
                self.adapters.append(pygatt.GATTToolBackend())
            print "Created adapters count: ", len(self.adapters), self.adapters[0]._hci_device
            
            print "Starting bluetooth adapters"
            for adapter in self.adapters:
                adapter.start()
            
            connectedList = dict()
            print "Enter main loop"
            
            try:
                while 1:
                    print "Searching devices [5s}..."
                    devs = self.adapters[0].scan(timeout=5, run_as_root=True)
                    for dev in devs:                    
                        #print "\tUrzadzenie ", dev["name"], " o adresie: ", dev["address"]
                        if not (dev['name'] in connectedList):
                            newDevice = TestoDevice(dev["name"], dev["address"], self.adapters[len(connectedList)+1])
                            print newDevice
                            connectedList[dev["name"]] = newDevice
                    
                    #print connectedList, type(connectedList)
                    #if len(connectedList) <> 0:
                    #    for device in connectedList:
                    #        print "Device:\t", device#, device.battery, device.temperature, device.velocity
            except KeyboardInterrupt:
                print "Halt from keyboard"
        finally:
            print "Unexpected error:", sys.exc_info()[0]
            print "Stopping bluetooth adapters"
            for adapter in self.adapters:
                adapter.stop()
