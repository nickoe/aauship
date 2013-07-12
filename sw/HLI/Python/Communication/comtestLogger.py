import packetHandler
import packetparser
import Queue
import time
import csv
import numpy
import os
from math import pi
import serial

#import Ship_nofilter as Shipnf
#import Ship
#import ObjectLibrary as OL

'''LOGGING FOR BOTH'''
receivinglog = open("meas/received.txt",'w')
acclog = open("meas/acc.txt",'w')
gpslog = open("meas/gps.txt",'w')
plog = open("meas/plog.txt",'w')
inclog = open("meas/inclog.txt",'w')
echolog = open("meas/echolog.txt",'w')
gps2log = open("meas/gps2log.txt",'wb')

Y = numpy.array([0,2.5574,0.5683,-16.3120,-40.7704]) #Easting
X = numpy.array([0,-18.3388,-36.7722,-53.9444,-54.2330]) #Northing

WPC = numpy.array([X,Y])

qu = Queue.Queue()
kalqueue = Queue.Queue()
to = 0.1665
#receiver = packetHandler.packetHandler("/dev/tty.SLAB_USBtoUART",38400,0.02,qu,inclog)
# Using the udev rules file 42-aauship.rules 
receiver = packetHandler.packetHandler("/dev/lli",115200,0.02,qu,inclog)
echorcv = serial.Serial("/dev/echosounder",4800,timeout=0.04)
gps2rcv = serial.Serial("/dev/gps2",115200,timeout=0.04)

receiver.start()

measuredstates = numpy.zeros((9,2))
tempm = measuredstates
parser = packetparser.packetParser(acclog,gpslog,measuredstates,receivinglog,plog)
bla = True
timeout = 1000
p = receiver.constructPacket("",0,9)
print "Packet:" ,
print p
#time.sleep(2)
stopping = False
count = 0
print "message sent"
motor = numpy.matrix([[0],[0]])
motor2 = numpy.matrix([[0],[0]])
sendControl = 0
running = True
sign = 1
p = {'DevID': chr(255) , 'MsgID': 0,'Data': 0, 'Time': time.time()}
p2 = {'DevID': chr(255) , 'MsgID': 0,'Data': 0, 'Time': time.time()}
GPSFIX = False
print p
try:
	
	while running == True:
			if(receiver.isOpen()):
				try:
					p = qu.get(False)
					#receivinglog.write(str(p['DevID']) + "," + str(p['MsgID']) + "," + str("".join(p['Data'])) + "\r\n")
					if ord(p['DevID']) != 255:
						#print "\r" + str(p),
						#print p
						pass
					if ord(p['DevID']) == 30 and ord(p2['DevID']) == 255:
						
						GPSFIX = True
					#	print "Handling GPS Data!1"
						p2 = p
						n = 0
						while n < 3:
							try:
								p = qu.get(False)
							except Queue.Empty:
								time.sleep(0.0001)
								pass
							n += 1
						parser.parse(p2)
						parser.parse(p)
						tempm = measuredstates
						sendControl += 1
					#	print measuredstates
					
					elif ord(p2['DevID']) == 20 and ord(p['DevID']) == 30:
						GPSFIX = True
					#	print "blaH"
					##	print "Handling GPS Data!2"
					#	print p
					#	print p2
						parser.parse(p)
						parser.parse(p2)
						tempm = measuredstates
						#print measuredstates[0]
						sendControl += 1
						#print measuredstates
						#tempm = measuredstates
						
					elif ord(p2['DevID']) == 20 and ord(p['DevID']) == 20:
						parser.parse(p2)
						#print measuredstates[0]
						sendControl += 1
						
					elif ord(p2['DevID']) == 20 and ord(p['DevID']) == 255:
						parser.parse(p2)
						sendControl += 1
						
					if ord(p2['DevID']) == 255 and ord(p['DevID']) == 255 and sendControl > 0:
						#print chr(27) + "[2J"
						#print measuredstates[0][1]
						if measuredstates[0][1] == 1:
							print measuredstates
						
						#if measuredstates[0][1] == 1:
						#	print "blaH"
						print time.time()
						if GPSFIX == True:
							print "GPS FIX!"
							#AAUSHIP2.ReadStates(tempm,motor)
						GPSFIX = False
						#print sendControl
						sendControl = 0
						#print sendControl
						#print str(count)
						count += 1
						
					p2 = p
					
#					elif ord(p['DevID']) == 20 and ord(p2['DevID']) == 30:
#						parser.parse(p2)
#						parser.parse(p)
#					elif ord(p2['DevID']) == 20:
#						parse(p2)
				except Queue.Empty:
					pass

				# Grabbing the echosounder data
				try:
					echosounder = echorcv.readline()
					echosounder = echosounder.rstrip()
					if echosounder != "":
						#print echosounder
						echolog.write(echosounder + ',' + str(time.time()) + "\r\n")
				except Exception:
					pass
				
				# Grabbing the GPS2 data
				try:
					gps2 = gps2rcv.readline()
					if gps2 != "":
						gps2 = gps2.rstrip()
						gps2log.write(gps2 + ',' + str(time.time()) + "\r\n")
						#print gps2
#						if gps[0:3]=='$GP':
#							print "nullermand" + gps2
#							gps2 = gps2.rstrip()
#							gps2log.write(gps2 + ',' + str(time.time()) + "\r\n")
#						else:
#							gps2log.write(gps2)
				except Exception:
					pass

except KeyboardInterrupt:
	print "Interrupted by keyboard"
	receiver.close()
	receiver.join()
				
'''
try:
	while bla == True:
		try:
			if(receiver.isOpen()):
				#time.sleep(0.1)
				packet = qu.get(False)
				if packet == "End":
					if sendControl > 2:
					
						print str(count)
						p = receiver.constructPacket(str(count)+"\r\n",10,19)
						count += 1
						receiver.sendPacket(p)
						print  str(time.time())
						sendControl = 0
				else:
					sendControl += 1
					parser.parse(packet)
			else:
				print "Closing loop"
				bla = False
			#print "Parsed"
		except KeyboardInterrupt:
			print "keyboardinterrupted main loop"
			receiver.close()
			if stopping:
				break
			stopping = True
		except Queue.Empty:
			pass
		
		except Exception as inst:
			print type(inst)
			try:
				if stopping:
					break
				else:
					#print "Get Exception"
					#time.sleep(0.000001)
					pass
					
					#if timeout > 50:
						#p = receiver.constructPacket(2000,2,3)
						#receiver.sendPacket(p)
						#bla = False
					#timeout = timeout + 1
			except KeyboardInterrupt:
				print "Interrupt 1"
				p = receiver.constructPacket("",0,9)
				receiver.sendPacket(p)
				time.sleep(2)
				receiver.close()
				if stopping:
					break
				stopping = True
except KeyboardInterrupt:
	print "outer interrupt"
	receiver.close()
		
	
#receiver.close()
#receiver.join()
''
n = 0
while True:
	if (n % 5) == 0:
		print ""
	try:
		t = kalqueue.get(False)
		print t
	except:
		break
'''

receivinglog.close()
echorcv.close()

acclog.close()
gpslog.close()
echolog.close()
gps2log.close()


plog.close()
inclog.close()

print "done"

quit()	
