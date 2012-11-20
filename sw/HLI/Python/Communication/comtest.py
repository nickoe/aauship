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
			p = receiver.constructPacket(2000,2,3)
			receiver.sendPacket(p)
			bla = False
		timeout = timeout + 1
		
