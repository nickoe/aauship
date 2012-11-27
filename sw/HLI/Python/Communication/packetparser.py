import struct
import csv
class packetParser():
	def __init__(self,file):
		self.GPS = {0: 'Latitude', 1: 'Longtitude', 2: 'Velocity'}
		self.IMU = {0: 'Acceleration X', 1: 'Acceleration Y', 2: 'Acceleration Z', 3: 'Gyroscope X', 4: 'Gyroscope Y', 5: 'GyroscopeZ', 6: 'MagnetometerX', 7: 'MagnetometerY', 8: 'MagnetometerZ', 9: 'Temperature'}
		self.MsgID = {0: self.GPS, 1: self.IMU}
		self.DevID = {0: 'GPS', 1: 'IMU'}
		self.accelburst = [0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.log = file
		self.writer = csv.writer(self.log)
		#print "Stdsqewarted!"
		pass
			
	def parsePacket(self,packet):
		#print packet
		#print "started parsing"
		#print "Parsing: "
		#print "What"
		#print "----------"
		#print "parsing:"
		'''
		List of DevIDS:
		GPS: 0
		IMU: 1
		
		'''
		value = ""
		packetinfo = ""
		if (ord(packet['DevID']) == 0):		#GPS
			print "General"
		
			'''
			List of MsgIDs:
			Latitude: 0
			Longtitude: 1
			Velocity: 2
			'''
			if(ord(packet['MsgID']) == 0): 		#Latitude
				value = self.Ascii(packet['Data'])
			elif(ord(packet['MsgID']) == 1): 	#Longtitude
				value = self.Ascii(packet['Data'])
			elif(ord(packet['MsgID']) == 9): 	#Velocity
				print "".join(packet['Data'])
			else:
				print "fejl"
				print "MsgID [" + str(ord(packet['MsgId'])) + "] not recognized"
		elif(ord(packet['DevID']) == 1): 		#IMU
			'''
			List of MsgIDs:
			AccelX 	: 0
			AccelY 	: 1
			AccelZ	: 2
			GyroX 	: 3
			GyroY 	: 4
			GyroZ 	: 5
			MagX  	: 6
			MagY	: 7
			MagZ	: 8
			Temp	: 9
			'''
			if(packet['MsgID'] == 0):		#AccelX
				value = self.binary(packet['Data'])
			elif(packet['MsgID'] == 1):	#AccelY
				value = self.binary(packet['Data'])
			elif(packet['MsgID'] == 2):	#AccelZ
				value = self.binary(packet['Data'])
			elif(packet['MsgID'] == 3):	#GyroX
				value = self.binary(packet['Data'])
			elif(packet['MsgID'] == 4):	#GyroY
				value = self.binary(packet['Data'])
			elif(packet['MsgID'] == 5):	#GyroZ
				value = self.binary(packet['Data'])
			elif(packet['MsgID'] == 6):	#MagX
				value = self.binary(packet['Data'])
			elif(packet['MsgID'] == 7):	#MagY
				value = self.binary(packet['Data'])
			elif(packet['MsgID'] == 8):	#MagZ
				value = self.binary(packet['Data'])
			elif(packet['MsgID'] == 9):	#Temp
				value = self.binary(packet['Data'])
			else:
				print "MsgID [" + ord(packet['MsgID']) + "] not recognized"
		elif(ord(packet['DevID']) == 20):
			#print "------------------------IMU!-----------------------"
			if(ord(packet['MsgID']) == 13):
				accelnr = 0
				#print "Recognized msg"
				#print packet['Data']
				isInt = False
				
			
				for i in range(len(packet['Data'])):
					#print packet['Data'][i] +"\t (" + str(ord(packet['Data'][i])) + ")\t [" + hex(ord(packet['Data'][i])) + "]"

					#print str(packet['Data'][i-1:i+1])
					if ((i & 1) == 1):
						tempval = packet['Data'][i-1:i+1]
						tempval.reverse()
						#print str("".join(tempval))
						val = 0
						try:
							val = struct.unpack('h', "".join(tempval))
						except:
							pass
						#val = struct.unpack('h', "".join(packet['Data'][i-1:i+1]))
						self.accelburst[accelnr] = val[0]
						accelnr = accelnr + 1
						#print str(val[0])
				self.accelburst[accelnr] = packet['Time']
				if(self.accelburst[accelnr-1] == 256):
					print packet
					print self.accelburst
				#print self.accelburst
				else:
					self.writer.writerow(self.accelburst)
				#print "successfull write"
				#print str(packet['Data'])
			#print str(ord(packet['MsgID']))
		else:
			print "DevID [" + (packet['DevID']) + "] not recognized"
		#print packet
		#print self.DevID[packet['DevID']] + "\t" + self.MsgID[packet['DevID']][packet['MsgID']] + "\t" + str(value)
				
	def binary(self,data):
		value = 0
		for i in range(len(data)):
			value = value + data[i]*pow(2,8*(len(data)-1-i))
		return value
	
	def Ascii(self,data):
		value = "".join(map(chr,data))
		return value
		
