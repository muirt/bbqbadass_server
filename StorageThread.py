import configuration
import time

class StorageThread():

	def __init__(self):
		self.ShouldStop = False

	def StorageLoop(self):		
		storagePeriod = configuration.Parameters.StoragePeriod		
		
		while(self.ShouldStop == False):
			time.sleep(storagePeriod)