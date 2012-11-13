import serial
import threading
import time
import crc16pure as crc
import struct

running = True;

class Serialdummy:

	class Serial:
		def __init__(self,serialport,speed):
			''' START, BYTE_LEN, myID, devID, Data, CKH, CKL '''
			self.array = [0x24,3,3,3,3,3,3,4,5,0x24,2,2,2,2,2,2,3,0x24,2,2,2,1,2,4,5,4,5,4,5,2,3,0x24,1,2,0x24,6,3,4,1,2,1,2,1,2,4,5,0,4,3]
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
	
	def __init__(self,serialport,speed):
		self.connection = Serialdummy.Serial(serialport,speed)
		self.newdata = []
		
	def run(self):
		while self.connection.isOpen():
			checkchar = self.connection.Read(1)
			if checkchar == 0x24:
				length=self.connection.Read(1)
				res = self.parser(length)
				if(res[0]):
					self.parsePacket(res[1])
			'''
				length = self.connection.read(1)
				DevID = self.connection.read(1)
				MsgID = self.connection.read(1)
				data=[]
				for i in range(length):
					Data.append(self.connection.read(1))
				CKH = self.connection.read(1)
				CKL = self.connection.read(1)
				packet = {'Length': length, 'DevID': DevID, 'MsgID': MsgID, 'Data': Data,'CKH':CKH,'CKL':CKL }
				if(self.checksum(packet)):
					self.parsePacket(packet)
					
					newdata.append([devID,MsgID,Data]);
					
				else:
				
					
		print ''	
		print '--------'
		print 'Final Result:'
		print self.newdata
		print '--------'
		'''
		running = False
		print 'done'
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
	
	def DataCRC16(self, data):
		
		abc = struct.pack('>I', data)
		print(str(abc))
		chksum = crc.crc16xmodem(abc)
		CKL = chksum & 255
		CKH = (chksum >> 8) & 255
		chkrestored = CKL + (CKH << 8)
		
		print(chksum, CKH,CKL, chkrestored)
		
		return(numpy.array([CKH, CKL]))
		
	def freshdata(self):
		try:
			return len(self.newdata)
		except:
			return 0	
			
	def getdata(self):
		try:
			return self.newdata.pop(0)
		except:
			return 0
			
	def parsePacket(self,packet):
		#print 'Parsing:'
		#print packet
		length = packet[0]
		DevID = packet[1]
		MsgID = packet[2]
		Data = []
		for i in range(length):
			Data.append(packet[3+i])
		self.newdata.append({'DevID':DevID, 'MsgID': MsgID,'Data': Data})
		#print 'success'
		print self.newdata[len(self.newdata)-1]
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

print '/---------------------------------------\\'
receiver = packetHandler(1,2)
receiver.run()
receiver.checksum('abc')

receiver.DataCRC16(123)
	