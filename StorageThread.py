import configuration
import time
import filesystem
import CurrentIO
import datetime

class StorageThread():

	def __init__(self):
		self.ShouldStop = False

	def get_state_in_csv_row(self):
		row = [CurrentIO.getInputState("Grill"), CurrentIO.getInputState("Meat"), str(datetime.datetime.now())]
		return row

	def StorageLoop(self):		
		storagePeriod = configuration.Parameters.StoragePeriod		
		fs = filesystem.filesystem()

		while(self.ShouldStop == False):

			if configuration.Parameters.CurrentlyRecording == True:
				current_recording_name = configuration.Parameters.CurrentRecordingName
				row = self.get_state_in_csv_row()
				fs.write_to_file(current_recording_name, row)
			time.sleep(storagePeriod)