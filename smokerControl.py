import collectThread
import controlThread
import StorageThread
import threading
import time
import server
import configuration
import Queue
import getReadings

import debugger
import serverSingleton

import simpleServer


mode = "run"
serverControl = None



if __name__ == "__main__":

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

	serverControl = server.ServerControl()
	#serverSingleton.setServerControl(serverControl)
	

	#readings = getReadings.ReadingsThread()
	
	readingsThread = threading.Thread(target=serverControl.getReadings)
	readingsThread.daemon = True
	readingsThread.start()

	
	serverControl.start_server()

