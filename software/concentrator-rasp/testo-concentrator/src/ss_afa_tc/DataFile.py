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
import csv
import sys
import os

class DataFile(object):
    ##################################################################################################################
    # variables
    ##################################################################################################################
    dataPath = '/tmp/ss-afa'
    
    ##################################################################################################################
    # FUNCTIONS DEFINITION
    ##################################################################################################################
    # constructor        
    #def __init__(self, logger, path = '/opt/ss/testo/config.cfg'):
    def __init__(self, deviceName, fileName):
        print deviceName.split(":")
        self.deviceName = deviceName.split(":")[1]
        self.fileName = fileName
        try:
            print "Check path and create"
            self.checkPathAndCreate(self.dataPath)
            self.checkPathAndCreate(self.dataPath + '/' + self.deviceName)
            self.csvfile = open(self.dataPath + '/' + self.deviceName + '/' + self.fileName + '.csv', 'w')
            self.fieldnames = ['Czas próbki', 'Wartość próbki']
            self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)
        
            self.writer.writeheader()
            print "Created data file"
        except:
            #self.logger.logWarning("Can't parse config file: " + self.configPath, self)
            print "DataFile init exception", self.dataPath + '/' + self.deviceName + '/' + self.fileName + '.csv'
            print "Unexpected error:", sys.exc_info()[0]
    
    #function check if dir exists
    def checkPathAndCreate(self, path):
        print "Checking path", path

        if not os.path.exists(path):
            print "Creating", path
            os.makedirs(path)
            
    # function add row to data file
    def addRow(self, timestamp, value):
        self.writer.writerow({self.fieldnames[0]: timestamp, self.fieldnames[1]: value})