#GPSParser

from pynmea.streamer import NMEAStream
import time
from pynmea import nmea

#f = open('gpsSDlog291112.log','w')
f = open('speedlog.log','w')
lines = 0
gga = 0
data=[]
try:
	fr = open('LOG00139.txt','r')
	while 1:
		line = fr.readline()
		#print line
		if not line:
			break
		lines = lines + 1
		if (line.split(',')[0].lstrip('$') == "GPRMC"):
			#print "GPRMC!"
			print line
			gga = gga + 1
			d = line.split(',')
			print d[7]
			f.write(d[7] + "\n")
			#f.write(d[2] + "," + d[4] + "\n")
			
		#print line
except:	
	pass
print gga
print lines
f.close()
quit()	
time.sleep(5)

with open('gpslog291112.txt','r') as data_file:
	streamer = NMEAStream(data_file)
	next_data = streamer.get_objects()
	data = []
	i = 0
	samples = 0
	while next_data:
	
		try:
			datapack = []
			data += next_data
			next_data = streamer.get_objects()
			#print type(next_data)
			try:
				#print data[i].latitude
				#print data[i].lat_direction
				#print data[i].longitude
				#print data[i].lon_direction
				#print data[i]
				try:
					#print type(data[i])
					#time.sleep(0.5)
					if(type(data[i]) is nmea.GPGGA):
						print "GPGGA Packet!"
						print data[i].timestamp
					print data[i]
					datapack.append(data[i].latitude)
					datapack.append(data[i].lat_direction)
					datapack.append(data[i].longitude)
					datapack.append(data[i].lon_direction)
					datapack.append(data[i].timestamp)
					#print data[i]
					print datapack
					#f.write(datapack[0]+",\""+datapack[1]+"\","+datapack[2]+",\""+datapack[3]+"\"\n")
					f.write(datapack[0] + "," + datapack[2] + "," + datapack[4] + "\n")
					print "written"
					print 
					
				except KeyboardInterrupt:
					print "KEYBOARDINTERUPT"
					break
				except Exception as e:
					#print e
					pass
			except KeyboardInterrupt:
				break
			except:
				pass
			i = i + 1
		except KeyboardInterrupt:
			break
		
	#print data
f.close()