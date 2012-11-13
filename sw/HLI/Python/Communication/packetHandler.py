#import serial
import threading
import time
import datetime
import Queue
from math import pow

running = True;

class Serialdummy:

	class Serial:
		def __init__(self,serialport,speed):
			self.array = [0x24,3,0,1,49,50,51,4,5,0x24,2,1,1,2,2,2,3,0x24,2,1,1,1,2,4,5,4,5,4,5,2,3,0x24,1,2,0x24,6,0,2	,48,49,50,51,52,53,4,5,0,4,3]
			self.open = True;
		def Read(self,numbers):
			'''print self.array[0]'''
			return self.array.pop(0)
			
		def isOpen(self):
			if len(self.array) > 0:		
				return open
			return False
		
		def close(self):
			self.open = False;

class packetHandler(threading.Thread):
	
	def __init__(self,serialport,speed,queue):
		self.connection = Serialdummy.Serial(serialport,speed)
		self.myNewdata = []
		self.q = queue
		threading.Thread.__init__(self)
		
	def run(self):
		while self.connection.isOpen():
			checkchar = self.connection.Read(1)
			if checkchar == 0x24:
				length=self.connection.Read(1)
				res = self.parser(length)
				if(res[0]):
					self.preparePacket(res[1])
		running = False
		#print '\\------------------------------------------------------/'
		
	def close(self):
		self.connection.close()
				
	def sendData(self,data,DevID,MsgID):
		packet = [len(data),DevID,MsgID]
		for i in range(data):
			packet.append(data[i])
		Checksum = self.generateCheckSum(packet)
		packet.append(Checksum(0))
		packet.append(Checksum(1))
		
	def isOpen(self):
		return self.connection.isOpen()
		
	def checksum(self,packet):
	
		CKL = packet[len(packet)-1]
		CKH = packet[len(packet)-2]
		
		'''
			Calculate Checksum
		'''
		if CKL == 5:
			if CKH == 4:
				if len(packet) - 5 == packet[0]:
					return True
		return False
	
	def newdata(self):
		try:
			return len(self.myNewdata)
		except:
			return 0	
			
	def getdata(self):
		try:
			return self.newdata.pop(0)
		except:
			return 0
			
	def preparePacket(self,packet):
		#print 'Parsing:'
		#print packet
		length = packet[0]
		DevID = packet[1]
		MsgID = packet[2]
		Data = []
		for i in range(length):
			Data.append(packet[3+i])
		newpacket = {'DevID':DevID, 'MsgID': MsgID,'Data': Data}
		self.myNewdata.append(newpacket)
		self.q.put(newpacket)
		#print 'success'
		#print self.myNewdata[len(self.myNewdata)-1]
		#print '-------------'
		
		
	def parser(self,array):
		#print 'input: ' + repr(array)
		success = False
		packet = []
		length=1
		try:
			length = len(array)
			for j in range(length):
				packet.append(array[j])
		except:
			packet.append(array)
			extrabits = 4
		for i in range((packet[0]-length+5)):
			packet.append(self.connection.Read(1))
		check = self.checksum(packet)
		#print 'after reading:' + repr(packet)
		if(check):
		#	print 'True'
			return [True, packet]
		else:
		#	print 'False'
		#	print '-------------'
			try:
				index = packet.index(0x24)
				if index == len(packet)-1:
					packet.append(self.connection.Read(1))
				del packet[0:index+1]
				return self.parser(packet)
			except:
				return [False,0]
	
class packetParser():
	def __init__(self):
		pass
			
	def parsePacket(self,packet):
		print "----------"
		print "parsing:"
		'''
		List of DevIDS:
		GPS: 0
		IMU: 1
		
		'''
		print packet
		if (packet['DevID'] == 0):		#GPS
			print "GPS!"
			'''
			List of MsgIDs:
			Latitude: 0
			Longtitude: 1
			Velocity: 2
			'''
			if(packet['MsgID'] == 0): 	#Latitude
				print "Latitude!"
				value = []
				for i in range(len(packet['Data'])):
					value.append(chr(packet['Data'][i]))
				print value
				print "done"
			elif(packet['MsgID'] == 1): 	#Longtitude
				print "Longtitude!"
				value = []
				for i in range(len(packet['Data'])):
					value.append(chr(packet['Data'][i]))
				print value
				print "done"
			elif(packet['MsgID'] == 2): 	#Velocity
				
				print "Velocity!"
				value = []
				for i in range(len(packet['Data'])):
					value.append(chr(packet['Data'][i]))
				print value
				print "done"
		elif(packet['DevID'] == 1): 		#IMU
			print "IMU!"
			'''
			List of MsgIDs:
			AccelX : 0
			AccelY : 1
			AccelZ : 2
			GyroX  : 3
			GyroY  : 4
			GyroZ  : 5
			'''
			if(packet['MsgID'] == 0):		#AccelX
				pass
			elif(packet['MsgID'] == 1):	#AccelY
				print "AccelY!"
				value = 0
				for i in range(len(packet['Data'])):
					value = value + packet['Data'][i]*pow(2,8*(len(packet['Data'])-1-i))
				print value
			elif(packet['MsgID'] == 2):	#AccelZ
				pass
			elif(packet['MsgID'] == 3):	#GyroX
				pass
			elif(packet['MsgID'] == 4):	#GyroY
				pass
			elif(packet['MsgID'] == 5):	#GyroZ
				pass

	