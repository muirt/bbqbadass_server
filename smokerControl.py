import collectThread
import controlThread
import StorageThread
import threading
import time

import configuration
import Queue


import SimpleExampleServer

import readings_stream as readings
import os

mode = "run"
serverControl = None


def update():
	return serverControl.updateGUI()

if __name__ == "__main__":

	
	collectQueue = Queue.Queue()
	readingsQueue = Queue.Queue()

	configuration.Load()
	collectObject = collectThread.CollectThread()
	controlObject = controlThread.ControlThread()
	storageObject = StorageThread.StorageThread()
	collThread = threading.Thread(target=collectObject.PeriodicCollect)
	collThread.daemon = True
	collThread.start()

	time.sleep(3)

	contThread = threading.Thread(target=controlObject.ControlLoop)
	contThread.daemon = True
	contThread.start()

	storageThread = threading.Thread(target=storageObject.StorageLoop)
	storageThread.daemon = True
	storageThread.start()


	# serverControl = server.ServerControl()
	#serverControl = server.ServerControl()

	#serverSingleton.setServerControl(serverControl)
	

	#readings = getReadings.ReadingsThread()
	#readingsThread = threading.Thread(target=pyws.getReadings)
	

	
	simplerThread = threading.Thread(target=SimpleExampleServer.start_server)
	simplerThread.daemon = True
	simplerThread.start()

	time.sleep(3)

	readingsObject = readings.Readings()

	readingsThread = threading.Thread(target=readingsObject.getReadings)
	readingsThread.daemon = True
	readingsThread.start()

	#SimpleExampleServer.start_server()

	while True:
		pass

