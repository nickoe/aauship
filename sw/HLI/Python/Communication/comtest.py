import packetHandler
import packetparser
import Queue
import time
import csv
import numpy
import os

import Ship
import ObjectLibrary as OL

Startpos = OL.O_PosData(0, 0, 0, 1)
AAUSHIP = Ship.O_Ship(Startpos)

'''
EMBEDDED OPTIONAL STEP 2/B
Waypoint ADDING
'''

X = numpy.array([0,1,2,3,4,5,6,7])
Y = numpy.array([10,11,12,13,14,15,16,17])
WPC = numpy.array([X,Y])
AAUSHIP.SetWaypoints(WPC)

'''
EMBEDDED STEP 3
Set first target WP (should be 0 or 1)
'''
AAUSHIP.FlushPath(1)

'''
EMBEDDED STEP 5
Control loop
'''
#while 1:
    
#   '''Force ant torque control'''
#    motor = AAUSHIP.Control_Step()
#    AAUSHIP.ReadStates(measurement_matrix, motor)
#    tosend = AAUSHIP.FtoM(motor)





accf = open("accdata121212.csv", 'w')
gpsf = open("gpsdata121212.txt", 'a')
qu = Queue.Queue()
kalqueue = Queue.Queue()
to = 0.1665
receiver = packetHandler.packetHandler("/dev/tty.SLAB_USBtoUART",38400,0.02,qu)
receiver.start()

measuredstates = numpy.zeros((9,2))
parser = packetparser.packetParser(accf,gpsf,measuredstates)
bla = True
timeout = 1000
p = receiver.constructPacket("",0,9)
print "Packet:" ,
print p
#receiver.sendPacket(p)
#time.sleep(2)
stopping = False
count = 0
print "message sent"
motor = numpy.matrix([[0],[0]])
sendControl = 0
running = True
p = {'DevID': chr(255) , 'MsgID': 0,'Data': 0, 'Time': time.time()}
p2 = {'DevID': chr(255) , 'MsgID': 0,'Data': 0, 'Time': time.time()}
print p
try:
	
	while running == True:
			if(receiver.isOpen()):
				
				try:
					
					
					p = qu.get(False)
					if ord(p['DevID']) != 255:
						#print p
						pass
					if ord(p['DevID']) == 30 and ord(p2['DevID']) == 255:
						print "Handling GPS Data!"
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
						
						motor = AAUSHIP.Control_Step()
						AAUSHIP.ReadStates(measuredstates, motor)
						sendControl += 1
					
					elif ord(p2['DevID']) == 20 and ord(p['DevID']) == 30:
						print "Handling GPS Data!"
						parser.parse(p)
						parser.parse(p2)
						motor = AAUSHIP.Control_Step()
						AAUSHIP.ReadStates(measuredstates, motor)
						sendControl += 1
						
					elif ord(p2['DevID']) == 20 and ord(p['DevID']) == 20:
						parser.parse(p2)
						motor = AAUSHIP.Control_Step()
						AAUSHIP.ReadStates(measuredstates, motor)
						sendControl += 1
						
					elif ord(p2['DevID']) == 20 and ord(p['DevID']) == 255:
						parser.parse(p2)
						motor = AAUSHIP.Control_Step()
						AAUSHIP.ReadStates(measuredstates, motor)
						sendControl += 1
						
					if ord(p2['DevID']) == 255 and ord(p['DevID']) == 255 and sendControl > 2:
						sendControl = 0
						#print str(count)
						count += 1
						sp = receiver.constructPacket(str(count)+"\r\n",10,19)
						receiver.sendPacket(sp)
    					tosend = AAUSHIP.FtoM(motor)
    					#print chr(27) + "[2J"
    					print motor
    					print tosend
    					print measuredstates
    					print ""
						
					p2 = p
					
#					elif ord(p['DevID']) == 20 and ord(p2['DevID']) == 30:
#						parser.parse(p2)
#						parser.parse(p)
#					elif ord(p2['DevID']) == 20:
#						parse(p2)
				except Queue.Empty:
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
accf.close()
gpsf.close()
print "done"

quit()	
