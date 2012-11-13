import packetHandler
import packetparser
import Queue

qu = Queue.Queue()
receiver = packetHandler.packetHandler(1,2,qu)
receiver.start()
parser = packetparser.packetParser()
bla = True
timeout = 0
while bla == True:
	try:
		packet = qu.get(False)
		#print packet
		parser.parsePacket(packet)
	except Exception as inst:
		if timeout > 5:
			print "Quitting"
			bla = False
		timeout = timeout + 1
		
