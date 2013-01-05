import packetHandler
import packetparser
import Queue
import time
import csv
import numpy
import os
from math import pi

import Ship_nofilter as Shipnf
import Ship
import ObjectLibrary as OL

'''LOGGING FOR BOTH'''
receivinglog = open("meas/received.txt",'w')
acclog = open("meas/acc.txt",'w')
gpslog = open("meas/gps.txt",'w')
plog = open("meas/plog.txt",'w')

'''LOGGING FOR THE SHIP WITH KALMAN FILTER'''

Kswp = open("meas/Kalman/swp.txt",'w')
Kcontrol = open("meas/Kalman/control.txt",'w')
Kstate = open("meas/Kalman/state.txt",'w')


'''LOGGING FOR THE SHIP WITHOUT KALMAN FILTER'''
Nswp = open("meas/NoFilter/swp.txt",'w')
Ncontrol = open("meas/NoFilter/control.txt",'w')
Nstate = open("meas/NoFilter/state.txt",'w')





#Kalmanfile = open("measurements/Kalmandata141212.txt",'w')
#swp = open("measurements/swp141212.txt",'w')
#controllog = open("measurements/controllog141212.txt",'w')
#swpnf = open("measurements/swpnf141212.txt",'w')
#outputnf = open("measurements/outputnf.txt",'w')
Startpos = OL.O_PosData(0, 0, 0, 1)
AAUSHIP = Ship.O_Ship(Startpos,Kstate,Kswp)
AAUSHIP2 = Shipnf.O_Ship(Startpos,Nstate,Nswp)

'''
EMBEDDED OPTIONAL STEP 2/B
Waypoint ADDING
'''

#X = numpy.array([0,1,2,3,4,5,6,7])
#Y = numpy.array([10,11,12,13,14,15,16,17])
#Y = numpy.array([0,35.0543,35.5730,58.8078])
#X = numpy.array([0,-0.5753,26.0082,25.5482])

#Y = numpy.array([33.866070951884211, 35.298945836124972]) #Easting
#X = numpy.array([-28.917917253103049,42.596021647672877]) #Northing

Y = numpy.array([0,2.5574,0.5683,-16.3120,-40.7704]) #Easting
X = numpy.array([0,-18.3388,-36.7722,-53.9444,-54.2330]) #Northing

WPC = numpy.array([X,Y])
AAUSHIP.SetWaypoints(WPC)
AAUSHIP2.SetWaypoints(WPC)

'''
EMBEDDED STEP 3
Set first target WP (should be 0 or 1)
'''
AAUSHIP.FlushPath(-1)
AAUSHIP2.FlushPath(-1)

'''
EMBEDDED STEP 5
Control loop
'''
#while 1:
    
#   '''Force ant torque control'''
#    motor = AAUSHIP.Control_Step()
#    AAUSHIP.ReadStates(measurement_matrix, motor)
#    tosend = AAUSHIP.FtoM(motor)





#accf = open("measurements/accdata141212.csv", 'w')
#gpsf = open("measurements/gpsdata141212.txt", 'w')
#statelog = open("measurements/statelog141212.txt",'w')

qu = Queue.Queue()
kalqueue = Queue.Queue()
to = 0.1665
receiver = packetHandler.packetHandler("/dev/tty.SLAB_USBtoUART",38400,0.02,qu)
receiver.start()

measuredstates = numpy.zeros((9,2))
tempm = measuredstates
parser = packetparser.packetParser(acclog,gpslog,measuredstates,receivinglog,plog)
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
						motor2 = AAUSHIP2.Control_Step()
						motor = AAUSHIP.Control_Step()
						AAUSHIP2.ReadStates(measuredstates,motor)
						AAUSHIP.ReadStates(measuredstates, motor)
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
						motor2 = AAUSHIP.Control_Step()
						motor = AAUSHIP.Control_Step()
						
						AAUSHIP2.ReadStates(measuredstates,motor)
						AAUSHIP.ReadStates(measuredstates, motor)
						sendControl += 1
						#print measuredstates
						#tempm = measuredstates
						
					elif ord(p2['DevID']) == 20 and ord(p['DevID']) == 20:
						parser.parse(p2)
						#print measuredstates[0]
						motor2 = AAUSHIP2.Control_Step()
						motor = AAUSHIP.Control_Step()
						AAUSHIP2.ReadStates(measuredstates,motor)
						AAUSHIP.ReadStates(measuredstates, motor)
						sendControl += 1
						
					elif ord(p2['DevID']) == 20 and ord(p['DevID']) == 255:
						parser.parse(p2)
						motor2 = AAUSHIP2.Control_Step()
						motor = AAUSHIP.Control_Step()
						AAUSHIP2.ReadStates(measuredstates,motor)
						AAUSHIP.ReadStates(measuredstates, motor)
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
						#motor2 = AAUSHIP2.Control_Step()
						#AAUSHIP2.ReadStates(measuredstates,motor)
						
						sp = receiver.constructPacket(str(count)+"\r\n",10,19)
						receiver.sendPacket(sp)
						tosend = AAUSHIP.FtoM(motor)
						tosend2 = AAUSHIP2.FtoM(motor2)
						#print sendControl
						#print "Sent data"
						
						#print motor
						#print motor2
						#print "LastWP: \t" +  str(AAUSHIP.LastWP)
						#print "Theta_r: \t" + str(AAUSHIP.get_Thera_r()*180/pi)
						#print "Theta: \t\t" + str(AAUSHIP.Theta*180/pi)
						#print "NextWP (N,E): \t" + str(AAUSHIP.NextSWP.get_Pos())
						#print "Pos (N,E): \t" + str(AAUSHIP.Pos.get_Pos())
						#print "NFPos (N,E): \t" + str(AAUSHIP2.Pos.get_Pos())
						#print "MeasPos: \t" + str(AAUSHIP.get_mp())
						#print "Vel: \t" + str(AAUSHIP.get_vel())
						
						
						#print tempm
						#sign = -sign
						#print tosend
						
						#print motor[1,0]
						Kcontrol.write(str(tosend[0][0]) + ", " + str(tosend[1][0]) + ", " + str(motor[0,0]) + ", " + str(motor[1,0]) + ", " + str(time.time()) +"\r\n")
						Ncontrol.write(str(tosend2[0][0]) + ", " + str(tosend2[1][0]) + ", " + str(motor2[0,0]) + ", " + str(motor2[1,0]) + ", " + str(time.time()) +"\r\n")
						
						#print tosend
						#receiver.setMotor(int(round(tosend[0][0]*4)),int(round(tosend[1][0]*4)))
						#print measuredstates
						#print ""
						
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
#accf.close()
#gpsf.close()
#Kalmanfile.close()
#swp.close()
#controllog.close()
#swpnf.close()

receivinglog.close()
acclog.close()
gpslog.close()

Kswp.close()
Kcontrol.close()
Kstate.close()

Nswp.close()
Ncontrol.close()
Nstate.close()
plog.close()

print "done"

quit()	
