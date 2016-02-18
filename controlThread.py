import configuration
import outputControl
import time
import CurrentIO

class ControlThread:

	def __init__(self):        
		self.ShouldStop = False
			
	def ControlLoop(self):
		self.OutputController = outputControl.OutputControl()
		self.ShouldStop = False
		CurrentIO.ShouldControl = True
		while(self.ShouldStop == False):
			
			if CurrentIO.ShouldControl:				
				self.OutputController.ControlLoopPass(configuration.Parameters.ControlOutput,
					configuration.Parameters.ControlInput,
					configuration.Parameters.SetPoint,
					configuration.Parameters.Hysteresis,
					configuration.Parameters.OnState)
			time.sleep(configuration.Parameters.CollectionPeriod)
			
