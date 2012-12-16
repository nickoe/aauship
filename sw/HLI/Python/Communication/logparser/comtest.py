import Queue
import time
import csv
import numpy
import os, sys
from math import pi


import packetHandler
import packetparser

sys.path.append("..")
#import Ship_nofilter as Ship
import Ship
import ObjectLibrary as OL

Kalmanfile = open("kalmandata00206.txt",'w')
swp = open("swp00206.txt",'w')
controllog = open("controllog00206",'w')
Startpos = OL.O_PosData(0, 0, 0, 1)
AAUSHIP = Ship.O_Ship(Startpos,swp,Kalmanfile)

'''
EMBEDDED OPTIONAL STEP 2/B
Waypoint ADDING
'''

#X = numpy.array([0,1,2,3,4,5,6,7])
#Y = numpy.array([10,11,12,13,14,15,16,17])
#Y = numpy.array([0,35.0543,35.5730,58.8078])
#X = numpy.array([0,-0.5753,26.0082,25.5482])

Y = numpy.array([33.866070951884211, 35.298945836124972]) #Easting
X = numpy.array([-28.917917253103049,42.596021647672877]) #Northing

WPC = numpy.array([X,Y])
AAUSHIP.SetWaypoints(WPC)

'''
EMBEDDED STEP 3
Set first target WP (should be 0 or 1)
'''
AAUSHIP.FlushPath(-1)

'''
EMBEDDED STEP 5
Control loop
'''
#while 1:
    
#   '''Force ant torque control'''
#    motor = AAUSHIP.Control_Step()
#    AAUSHIP.ReadStates(measurement_matrix, motor)
#    tosend = AAUSHIP.FtoM(motor)


accf = open("accdata00206.csv", 'w')
gpsf = open("gpsdata00206.txt", 'a')

qu = Queue.Queue()
receiver = packetHandler.packetHandler("/dev/tty.SLAB_USBtoUART",38400,qu)
receiver.start()
parser = packetparser.packetParser(accf,gpsf)
bla = True
timeout = 0
p = receiver.constructPacket(0,0,9)
print "Packet:"
print p
receiver.sendPacket(p)
#time.sleep(2)
stopping = False
print "message sent"
while bla == True:
	try:
		if(receiver.isOpen()):
			#time.sleep(0.1)
			packet = qu.get(False)
			try:
				pass
			#	print packet
			except:
				print "Oh well"
			parser.parse(packet)
		else:
			print "Closing loop"
			bla = False
		#print "Parsed"
	except Exception as inst:
		try:
			if stopping:
				break
			else:
				#print "Get Exception"
				time.sleep(0.001)
				#if timeout > 50:
					#p = receiver.constructPacket(2000,2,3)
					#receiver.sendPacket(p)
					#bla = False
				#timeout = timeout + 1
		except KeyboardInterrupt:
				receiver.close()
				if stopping:
					break
				stopping = True
	except KeyboardInterrupt:
		
		receiver.close()
		if stopping:
			break
		stopping = True

	
#receiver.close()
#receiver.join()
accf.close()
gpsf.close()
print "done"
quit()	
