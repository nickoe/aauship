import struct
import csv
from pynmea import nmea
class packetParser():
	def __init__(self,accelfile,gpsfile):
		self.GPS = {0: 'Latitude', 1: 'Longtitude', 2: 'Velocity'}
		self.IMU = {0: 'Acceleration X', 1: 'Acceleration Y', 2: 'Acceleration Z', 3: 'Gyroscope X', 4: 'Gyroscope Y', 5: 'GyroscopeZ', 6: 'MagnetometerX', 7: 'MagnetometerY', 8: 'MagnetometerZ', 9: 'Temperature'}
		self.MsgID = {0: self.GPS, 1: self.IMU}
		self.DevID = {0: 'GPS', 1: 'IMU'}
		self.accelburst = [0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.accellog = accelfile
		self.accelwriter = csv.writer(self.accellog)
		self.prevtime = 0
		self.excount = 0
		#self.accelburst = 0
		self.gpspacket = 0
		
		self.gpsdata = [0,0,0,0,0,0,0,0]
		#Time of fix, Latitude, Longitude, Speed over ground, Course Made Good True, Date of Fix, Magnetic Variation, local timestamp
		self.gpslog = gpsfile
		self.writer = csv.writer(self.accellog)
		#self.gpswriter = csv.writer(self.gpslog)
		#print "Stdsqewarted!"
		pass
			
	def parse(self,packet):
		print packet
		try:
			if(ord(packet['DevID']) == 20):
				if(ord(packet['MsgID']) == 13):
					#self.accelburst = self.accelburst + 1
					#print "IMU: " + str(self.accelburst)
					
					
					accelnr = 0
					try:
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
						if(abs(self.accelburst[accelnr-2]) > 1000):
							print packet
							print self.accelburst
						#print self.accelburst
						else:
							self.writer.writerow(self.accelburst)
					except Exception as e:
						print e
					
					
					#print "IMU BURST!"
					pass
		
			elif (ord(packet['DevID']) == 30):
				if(ord(packet['MsgID']) == 6):
					self.gpspacket += 1
					#print "GPS: " + str(self.gpspacket)
					#print "".join(packet['Data']),
					self.gpslog.write("".join(packet['Data']))
					#self.gpswriter.writerow("".join(packet['Data']))
					#print "Logged"
					if("".join(packet['Data'][1:6]) == "GPGGA"):
						gpgga = nmea.GPGGA()
						tempstr = "".join(packet['Data'])
						gpgga.parse(tempstr)
						#print "Timestamp:" + gpgga.timestamp
						'''try:
							deltat = int(float(gpgga.timestamp))-self.prevtime
							print deltat
							self.prevtime = int(float(gpgga.timestamp))
						except Exception as e:
							print e'''
						gpsd = [gpgga.timestamp, gpgga.latitude, gpgga.longitude, packet['Time']]
						#self.gpswriter.writerow(gpsd)
					
					elif("".join(packet['Data'][1:6]) == "GPRMC"):
						
						gprmc = nmea.GPRMC()
						tempstr = "".join(packet['Data'])
						gprmc.parse(tempstr)
						
						self.gpsdata[0] = gprmc.timestamp
						self.gpsdata[1] = gprmc.lat
						self.gpsdata[2] = gprmc.lon
						self.gpsdata[3] = gprmc.spd_over_grnd
						#self.gpsdata[4] = gprmc.true_course
						#self.gpsdata[5] = gprmc.datestamp
						#self.gpsdata[6] = gprmc.mag_variation
						self.gpsdata[7] = packet['Time']
					#	print self.gpsdata
						#print self.gpsdata
						#self.gpswriter.writerow(self.gpsdata)
			else:
				print "unknown packet"	
		except Exception as e:
			self.excount += 1
			print " "+ str(self.excount)
			print e,
					
						
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
				
				#print "Recognized msg"
				#print packet['Data']
				isInt = False
				accelnr = 0
			
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
				if(abs(self.accelburst[accelnr-2]) > 1000):
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
		
	
		'''
		
	

 ('Timestamp', 'timestamp'),
            ('Latitude', 'latitude'),
            ('Latitude Direction', 'lat_direction'),
            ('Longitude', 'longitude'),
            ('Longitude Direction', 'lon_direction'),
            ('GPS Quality Indicator', 'gps_qual'),
            ('Number of Satellites in use', 'num_sats'),
            ('Horizontal Dilution of Precision', 'horizontal_dil'),
            ('Antenna Alt above sea level (mean)', 'antenna_altitude'),
            ('Units of altitude (meters)', 'altitude_units'),
            ('Geoidal Separation', 'geo_sep'),
            ('Units of Geoidal Separation (meters)', 'geo_sep_units'),
            ('Age of Differential GPS Data (secs)', 'age_gps_data'),
            ('Differential Reference Station ID', 'ref_station_id'))
            #('Checksum', 'checksum'))

'''