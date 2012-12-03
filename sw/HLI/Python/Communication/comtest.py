import packetHandler
import packetparser
import Queue
import time
import csv
accf = open("accdata00141.csv", 'w')
gpsf = open("gpsdata00141.txt", 'a')
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
time.sleep(2)
stopping = False
print "message sent"
while bla == True:
	try:
		#time.sleep(0.1)
		packet = qu.get(False)
		try:
			pass
		#	print packet
		except:
			print "Oh well"
		parser.parse(packet)
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
