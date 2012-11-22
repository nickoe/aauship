class packetParser():
	def __init__(self):
		self.GPS = {0: 'Latitude', 1: 'Longtitude', 2: 'Velocity'}
		self.IMU = {0: 'Acceleration X', 1: 'Acceleration Y', 2: 'Acceleration Z', 3: 'Gyroscope X', 4: 'Gyroscope Y', 5: 'GyroscopeZ', 6: 'MagnetometerX', 7: 'MagnetometerY', 8: 'MagnetometerZ', 9: 'Temperature'}
		self.MsgID = {0: self.GPS, 1: self.IMU}
		self.DevID = {0: 'GPS', 1: 'IMU'}
		
		#print "Stdsqewarted!"
		pass
			
	def parsePacket(self,packet):
		print packet
		print "started parsing"
		print "Parsing: "
		print "What"
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
		elif(packet['DevID'] == 1): 		#IMU
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
				print "MsgID [" + packet['MsgID'] + "] not recognized"
		
		else:
			print "DevID [" + packet['DevID'] + "] not recognized"
		print packet
		print self.DevID[packet['DevID']] + "\t" + self.MsgID[packet['DevID']][packet['MsgID']] + "\t" + str(value)
				
	def binary(self,data):
		value = 0
		for i in range(len(data)):
			value = value + data[i]*pow(2,8*(len(data)-1-i))
		return value
	
	def Ascii(self,data):
		value = "".join(map(chr,data))
		return value
		
