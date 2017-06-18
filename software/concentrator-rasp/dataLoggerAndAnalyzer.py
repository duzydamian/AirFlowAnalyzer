#!/usr/bin/python
#

import pygatt
import logging
import sys
import time
import base64
from array import array
import datetime
import struct
import os

dirTmp = "/tmp/ss-ta"
dirTmpOdroid = "/tmp/ss-ta/current/"


#---------------------------------------------------------------------------#
# Funkcje
#---------------------------------------------------------------------------#
# funkcja sprawdza czy dana sciezka istenieje i zaklada ja w razie potrzeby
def checkPathAndCreate(path):
    if not os.path.exists(path):
        os.makedirs(path)


# funkcja aktualizuje wskazany plik podana zawartoscia
def updateFile(file, content):
    dataFile = open(dirTmpOdroid + file, 'w')
    dataFile.write(content)
    dataFile.close()

def convert_str_bytearray(s):
	split_string = lambda x, n: [x[i:i+n] for i in range(0, len(x), n)]
	a = split_string(s,2)
	ba = bytearray()
	for z in a:
		ba.append(int(z,16))

	return ba
#quit()

def callback_fun(handle, data):
	global data_to_log
	if ready == True:
		print '-----------------------------------------------------------'
		print 'Notiyfikacja z handle: ', handle, 'dane: ', data		
		print '-----------------------------------------------------------'
		if data[0]==16:
			data_to_log = bytearray()
			data_to_log = data_to_log + data
		else:
			data_to_log = data_to_log + data
			#file_to_log.write(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + '\t')
			file_to_log.write(datetime.datetime.now().strftime("%H:%M:%S>") + ' ')
			file_to_log.write(''.join('{:02x}'.format(x) for x in data_to_log) + ' ')
			file_to_log.write(data_to_log + '\n')

			file_to_log_analized.write(datetime.datetime.now().strftime("%H:%M:%S>") + ' ')
			file_to_log_analized.write(''.join('{:02x}'.format(x) for x in data_to_log[:12]) + ' ')
			file_to_log_analized.write(''.join('{:02x}'.format(x) for x in data_to_log[12:]) + ' ')
			if len(data_to_log) > 12:
				if data_to_log[12]==0x42: #B > BatteryLevel
					file_to_log_analized.write(''.join('{:02x}'.format(x) for x in data_to_log[24:28]) + ' ')
					file_to_log_analized.write(''.join('{:02x}'.format(x) for x in data_to_log[28:]) + ' ')
					file_to_log_analized.write(data_to_log[12:24] + ' ')
					file_to_log_analized.write(str(struct.unpack('f', data_to_log[24:28])[0]) + '\n')
				if data_to_log[12]==0x54: #T > Temperature
					file_to_log_analized.write(''.join('{:02x}'.format(x) for x in data_to_log[23:27]) + ' ')
					file_to_log_analized.write(''.join('{:02x}'.format(x) for x in data_to_log[27:]) + ' ')
					file_to_log_analized.write(data_to_log[12:23] + ' ')
					file_to_log_analized.write(str(struct.unpack('f', data_to_log[23:27])[0]) + '\n')
				if data_to_log[12]==0x56: #V > Velocity
					file_to_log_analized.write(''.join('{:02x}'.format(x) for x in data_to_log[20:24]) + ' ')
					file_to_log_analized.write(''.join('{:02x}'.format(x) for x in data_to_log[24:]) + ' ')
					file_to_log_analized.write(data_to_log[12:20] + ' ')
					file_to_log_analized.write(str(struct.unpack('f', data_to_log[20:24])[0]) + '\n')
			else:
				file_to_log_analized.write(data_to_log[12:] + '\n')

			file_to_log_clean.write(datetime.datetime.now().strftime("%H:%M:%S>") + ' ')
			if len(data_to_log) > 12:
				if data_to_log[12]==0x42: #B > BatteryLevel
					file_to_log_clean.write(data_to_log[12:24] + ' ')
					file_to_log_clean.write(str(struct.unpack('f', data_to_log[24:28])[0]) + '\n')
					updateFile("bat_datetime.data", datetime.datetime.now().strftime("%H:%M:%S"))
					updateFile("bat_value.data", str(struct.unpack('f', data_to_log[24:28])[0]))
				if data_to_log[12]==0x54: #T > Temperature
					file_to_log_clean.write(data_to_log[12:23] + ' ')
					file_to_log_clean.write(str(struct.unpack('f', data_to_log[23:27])[0]) + '\n')
					updateFile("temp_datetime.data", datetime.datetime.now().strftime("%H:%M:%S"))
					updateFile("temp_value.data", str(struct.unpack('f', data_to_log[23:27])[0]))
				if data_to_log[12]==0x56: #V > Velocity
					file_to_log_clean.write(data_to_log[12:20] + ' ')
					file_to_log_clean.write(str(struct.unpack('f', data_to_log[20:24])[0]) + '\n')
					updateFile("velo_datetime.data", datetime.datetime.now().strftime("%H:%M:%S"))
					updateFile("velo_value.data", str(struct.unpack('f', data_to_log[20:24])[0]))
			else:
				file_to_log_clean.write(data_to_log[12:] + '\n')


checkPathAndCreate(dirTmp)
checkPathAndCreate(dirTmpOdroid)

updateFile("status.data", "Startuje")

ready = False
file_to_log = open("data.log", "w")
file_to_log_analized = open("dataAnalized.log", "w")
file_to_log_clean = open("dataClean.log", "w")
data_to_log = bytearray()

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.WARN)

# The BGAPI backend will attemt to auto-discover the serial device name of the
# attached BGAPI-compatible USB adapter.
adapter = pygatt.GATTToolBackend()
print "Uruchomiono z adapterem: ", adapter._hci_device

try:
	devices = []
	uuids=[]
	print "Uruchamianie adaptera"
	updateFile("status.data", "Uruchamianie adaptera")
	adapter.start()
	print "Szukanie urzadzen..."
	updateFile("status.data", "Szukanie urzadzen...")
	devs = adapter.scan(timeout=10, run_as_root=True)
	print "Znaleziono nastepujace urzadzenia:"
	for dev in devs:
		print "\tUrzadzenie ", dev["name"], " o adresie: ", dev["address"]
		print "Proba polaczenia..."
		updateFile("status.data", "Proba polaczenia z "+dev["address"])
		device = adapter.connect(dev["address"], 10.0)
		if device._connected:
			print "Proba polaczenia...OK"
			updateFile("status.data", "Polaczono z "+dev["address"])
			devices.append([dev["name"], dev["address"], device])
			file_to_log.write(dev["name"] + '\n')
			file_to_log_analized.write(dev["name"] + '\n')
			print "Charakterystyka"
			aa = device.discover_characteristics()
#			print dir(device)
			#print type(aa), aa
			for bb in aa:
				print aa[bb].uuid, aa[bb].handle, aa[bb].descriptors,
				try:
					value = device.char_read(bb, 1)
					print value
					#value2 = device.char_read_handle(aa[bb].handle, 1)
					#print aa[bb].handle, 'value2:\t', value2

					#for ch in value:
					#	print ch, '\t', chr(ch),								
				except pygatt.exceptions.NotificationTimeout:
					print "TIMEOUT"
					if aa[bb].handle == 40:
						uuids.append(bb)
						print bb
						device.subscribe(bb, callback=callback_fun)
						time.sleep(1)
				except:
					print "Error:", sys.exc_info()

			device.char_write_handle(37, convert_str_bytearray('5600030000000c69023e81'), True, 5)
			device.char_write_handle(37, convert_str_bytearray('200000000000077b'), True, 5)
			device.char_write_handle(37, convert_str_bytearray('04001500000005930f0000004669726d77617265'), True, 5)
			device.char_write_handle(37, convert_str_bytearray('56657273696f6e304f'), True, 5)
			device.char_write_handle(37, convert_str_bytearray('04001500000005930f0000004669726d77617265'), True, 5)
			device.char_write_handle(37, convert_str_bytearray('56657273696f6e304f'), True, 5)
			device.char_write_handle(37, convert_str_bytearray('04001600000005d7100000004d6561737572656d'), True, 5)
			device.char_write_handle(37, convert_str_bytearray('656e744379636c656161'), True, 5)
			device.char_write_handle(37, convert_str_bytearray('110000000000035a'), True, 5)
#	5600030000000c69023e81
#	200000000000077b
#	04001500000005930f0000004669726d77617265
#	56657273696f6e304f
#	04001500000005930f0000004669726d77617265
#	56657273696f6e304f
#	04001600000005d7100000004d6561737572656d
#	656e744379636c656161
#	110000000000035a
		else:
			print "Proba polaczenia...BLAD"

	ready = True
	for i in range(0,720):
#		print i
#		for id_uuid in uuids:
#			print id_uuid
#			device.subscribe(id_uuid, callback=callback_fun)
		time.sleep(1)
except KeyboardInterrupt:
	print "KONIEC"
finally:
	updateFile("status.data", "Wylaczono")
	adapter.stop()
