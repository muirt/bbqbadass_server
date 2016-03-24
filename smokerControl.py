import collectThread
import controlThread
import StorageThread
import threading
import time
import configuration
import SimpleExampleServer
import readings_stream as readings
import os

if __name__ == "__main__":

	configuration.Load()
	
	collectObject = collectThread.CollectThread()
	controlObject = controlThread.ControlThread()
	storageObject = StorageThread.StorageThread()
	readingsObject = readings.Readings()

	collThread = threading.Thread(target=collectObject.PeriodicCollect)
	collThread.daemon = True
	collThread.start()

	serverThread = threading.Thread(target=SimpleExampleServer.start_server)
	serverThread.daemon = True
	serverThread.start()

	#wait for collection and server to start before 
	#trying to store, act upon, or send sensor readings
	time.sleep(3)

	contThread = threading.Thread(target=controlObject.ControlLoop)
	contThread.daemon = True
	contThread.start()

	storageThread = threading.Thread(target=storageObject.StorageLoop)
	storageThread.daemon = True
	storageThread.start()

	readingsThread = threading.Thread(target=readingsObject.getReadings)
	readingsThread.daemon = True
	readingsThread.start()

	while True:
		pass

