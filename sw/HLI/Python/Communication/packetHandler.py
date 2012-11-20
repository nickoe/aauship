#import serial
import threading
import time
import datetime
import Queue
from math import pow
import crc16 as crc
import struct

running = True;
STARTCHAR = ord('$')

class Serialdummy:

	class Serial:
		def __init__(self,serialport,speed):
			self.array = [0x24,3,0,1,49,50,51,0x42,0xCE,0x24,2,1,1,2,2,2,3,0x24,2,1,1,1,2,0x5a,0xad,4,5,4,5,2,3,0x24,1,2,0x24,6,0,2	,48,49,50,51,52,53,0x6e,0x5b,0,4,3]
			self.open = True;
		def Read(self,numbers):
			'''print self.array[0]'''
			return self.array.pop(0)
			
		def isOpen(self):
			if len(self.array) > 0:		
				return open
			return False
			
		def write(self,byte):
			print str(byte)  + "\t [" + str(hex(byte)) + "]"
		
		def close(self):
			self.open = False;

class packetHandler(threading.Thread):
	
	def __init__(self,serialport,speed,queue):
		self.connection = Serialdummy.Serial(serialport,speed)	#Serial Connection
		self.myNewdata = []				#Array for storing new packets
		self.q = queue					#Queue to share data between threads
		 
		self.table = [
		0x0000, 0x1189, 0x2312, 0x329B, 0x4624, 0x57AD, 0x6536, 0x74BF,
		0x8C48, 0x9DC1, 0xAF5A, 0xBED3, 0xCA6C, 0xDBE5, 0xE97E, 0xF8F7,
		0x1081, 0x0108, 0x3393, 0x221A, 0x56A5, 0x472C, 0x75B7, 0x643E,
		0x9CC9, 0x8D40, 0xBFDB, 0xAE52, 0xDAED, 0xCB64, 0xF9FF, 0xE876,
		0x2102, 0x308B, 0x0210, 0x1399, 0x6726, 0x76AF, 0x4434, 0x55BD,
		0xAD4A, 0xBCC3, 0x8E58, 0x9FD1, 0xEB6E, 0xFAE7, 0xC87C, 0xD9F5,
		0x3183, 0x200A, 0x1291, 0x0318, 0x77A7, 0x662E, 0x54B5, 0x453C,
		0xBDCB, 0xAC42, 0x9ED9, 0x8F50, 0xFBEF, 0xEA66, 0xD8FD, 0xC974,
		0x4204, 0x538D, 0x6116, 0x709F, 0x0420, 0x15A9, 0x2732, 0x36BB,
		0xCE4C, 0xDFC5, 0xED5E, 0xFCD7, 0x8868, 0x99E1, 0xAB7A, 0xBAF3,
		0x5285, 0x430C, 0x7197, 0x601E, 0x14A1, 0x0528, 0x37B3, 0x263A,
		0xDECD, 0xCF44, 0xFDDF, 0xEC56, 0x98E9, 0x8960, 0xBBFB, 0xAA72,
		0x6306, 0x728F, 0x4014, 0x519D, 0x2522, 0x34AB, 0x0630, 0x17B9,
		0xEF4E, 0xFEC7, 0xCC5C, 0xDDD5, 0xA96A, 0xB8E3, 0x8A78, 0x9BF1,
		0x7387, 0x620E, 0x5095, 0x411C, 0x35A3, 0x242A, 0x16B1, 0x0738,
		0xFFCF, 0xEE46, 0xDCDD, 0xCD54, 0xB9EB, 0xA862, 0x9AF9, 0x8B70,
		0x8408, 0x9581, 0xA71A, 0xB693, 0xC22C, 0xD3A5, 0xE13E, 0xF0B7,
		0x0840, 0x19C9, 0x2B52, 0x3ADB, 0x4E64, 0x5FED, 0x6D76, 0x7CFF,
		0x9489, 0x8500, 0xB79B, 0xA612, 0xD2AD, 0xC324, 0xF1BF, 0xE036,
		0x18C1, 0x0948, 0x3BD3, 0x2A5A, 0x5EE5, 0x4F6C, 0x7DF7, 0x6C7E,
		0xA50A, 0xB483, 0x8618, 0x9791, 0xE32E, 0xF2A7, 0xC03C, 0xD1B5,
		0x2942, 0x38CB, 0x0A50, 0x1BD9, 0x6F66, 0x7EEF, 0x4C74, 0x5DFD,
		0xB58B, 0xA402, 0x9699, 0x8710, 0xF3AF, 0xE226, 0xD0BD, 0xC134,
		0x39C3, 0x284A, 0x1AD1, 0x0B58, 0x7FE7, 0x6E6E, 0x5CF5, 0x4D7C,
		0xC60C, 0xD785, 0xE51E, 0xF497, 0x8028, 0x91A1, 0xA33A, 0xB2B3,
		0x4A44, 0x5BCD, 0x6956, 0x78DF, 0x0C60, 0x1DE9, 0x2F72, 0x3EFB,
		0xD68D, 0xC704, 0xF59F, 0xE416, 0x90A9, 0x8120, 0xB3BB, 0xA232,
		0x5AC5, 0x4B4C, 0x79D7, 0x685E, 0x1CE1, 0x0D68, 0x3FF3, 0x2E7A,
		0xE70E, 0xF687, 0xC41C, 0xD595, 0xA12A, 0xB0A3, 0x8238, 0x93B1,
		0x6B46, 0x7ACF, 0x4854, 0x59DD, 0x2D62, 0x3CEB, 0x0E70, 0x1FF9,
		0xF78F, 0xE606, 0xD49D, 0xC514, 0xB1AB, 0xA022, 0x92B9, 0x8330,
		0x7BC7, 0x6A4E, 0x58D5, 0x495C, 0x3DE3, 0x2C6A, 0x1EF1, 0x0F78]				#CRC16 lookup table
		threading.Thread.__init__(self) #Initialize Thread
		
	def run(self):
		while self.connection.isOpen():	
			checkchar = self.connection.Read(1)	
			if checkchar == 0x24:	#Read char until start char is found
				length=self.connection.Read(1)	#The next char after start byte is the length
				res = self.parser(length)	#Input the length into the parser function
				if(res[0]):	#If the packet is valid, prepare the packet and put it in the queue
					self.preparePacket(res[1])
		running = False
			
	def close(self):
		self.connection.close()	#Close connection
		
	def CheckSum(self,packet):
		crc = 0xFFFF
		
		for i in packet:
			try:
				value = (crc ^ i) & 0xFF		#If the value of 'i' is an int
			except:
				value = (crc ^ ord(i)) & 0xFF	#if the value of 'i' is a chr
			crc = (crc >> 8) ^self.table[value]	
		result = [crc&0xFF,(crc>>8)&0xFF] 		#Format checksum correctly
		
		return result
		
	def constructPacket(self,data,DevID,MsgID):
		try:
			length = len(data)	#If the data is a string, get the length of the string
			dat = data	#if the data is a string, the data needs no formatting
		except TypeError:	#The above will give a typeError if its a number
			length = 0	#Init length
			num = []
			dat = []
			while (data >> 8*length) > 0: #Divide data into bytes
				num.append((data >> (8*length)) & 255) #Append bytewise
				length = length+1	#increment length of data
			#num = reversed(num)
			for i in reversed(num):	#append the data to the dat array in reverse, due to endianness
				dat.append(i)
		
		packet = [length,DevID,MsgID] #The first part of the packet contains the length, the DevID and the MsgID
		
		for i in range(length):
			packet.append(dat[i]) #The data is then appended.
		return packet
		
	def sendPacket(self,packet):
		#Checksum = self.generateCheckSum(packet)
		Checksum = self.CheckSum(packet)	#First, the checksum of the packet is generated
		packet.append(Checksum[0])	#The checksum is appropriately appended
		packet.append(Checksum[1])
		self.connection.write(STARTCHAR) #The startChar is written
		for i in range(len(packet)):	#The byte are then written individually
			self.connection.write(packet[i])
		
		
	def isOpen(self):
		return self.connection.isOpen()
	
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
		#print newpacket
		self.myNewdata.append(newpacket)
		self.q.put(newpacket)
		#print 'success'
		#print self.myNewdata[len(self.myNewdata)-1]
		#print '-------------'
		
	def packetCheck(self,packet):
		p = packet[:] #Copy packet to p
		incCheck=[p.pop(),p.pop()] #remove the two checksum bytes
		check = self.CheckSum(p) #get the checksum of the bit.
		#print "check: " + str(check)
		#print "incCheck: " + str(incCheck)
		if incCheck == check:
			return True
		else:
			return False
		
		
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
		check = self.packetCheck(packet)
		if(check):
			#print "EEEEEEEENS!"
			return [True, packet]
		else:
			try:
				index = packet.index(0x24)
				if index == len(packet)-1:
					packet.append(self.connection.Read(1))
				del packet[0:index+1]
				return self.parser(packet)
			except:
				return [False,0]

				pass

	