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

import SimpleExampleServer


mode = "run"
serverControl = None



if __name__ == "__main__":


	SimpleExampleServer.start_server()
	'''
	serverThread = threading.Thread(target=SimpleExampleServer.start_server)
	serverThread.daemon = True
	serverThread.start()
'''

