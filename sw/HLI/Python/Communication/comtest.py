import packetHandler
import packetparser
import Queue
import time

qu = Queue.Queue()
receiver = packetHandler.packetHandler("/dev/ttyUSB0",38400,qu)
receiver.start()
parser = packetparser.packetParser()
bla = True
timeout = 0
p = receiver.constructPacket(0,0,9)
print "Packet:"
print p
receiver.sendPacket(p)
time.sleep(2)
print "message sent"
while bla == True:
	try:
		packet = qu.get(False)
		try:
			print packet
		except:
			print "Oh well"
		parser.parsePacket(packet)
		print "Parsed"
	except Exception as inst:
		if timeout > 5:
			#p = receiver.constructPacket(2000,2,3)
			#receiver.sendPacket(p)
			bla = False
		timeout = timeout + 1
		
print "done"
#receiver.close()
#receiver.join()

quit()
