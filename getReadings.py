
import Queue
import configuration
import time
import CurrentIO
import unicodeHelper
import recorder
import json
import simpleServer
import server

class ReadingsThread:

	def __init__(self):		
		self.sendQueue = Queue.Queue()

	def getReadings(self):
		
		while True:			
			'''if serverSingleton.firstPass():
				serverSingleton.clearFirstPass()
				updateString = self.updateGUI()
				self.sendQueue.put(updateString)
				server.ServerControl.dispatch()'''
						                   
			self.buildAndQueueReadingsMessage()
			time.sleep(configuration.Parameters.CollectionPeriod)
	
	def buildAndQueueReadingsMessage(self):
	
		data_string = ""
		
		temp_reading_num = 1
		inputList = []
		for inputNumber in configuration.Parameters.CurrentTempList:
			inputDict = {}
			
			name = configuration.InputList[inputNumber].Name
			value = 0
			value = CurrentIO.getInputState(name)			
						
			if value != None:
				inputDict = {
								'name': unicodeHelper.getAscii(name), 
								'value': value
							} 
	
			inputList.append(inputDict)
			temp_reading_num += 1                    	                       
									
		setPoint = str(configuration.Parameters.SetPoint)
	                      
		outputState = CurrentIO.getOutputState('controlOutput')
		stateString = ''
		
		if outputState:
			stateString = 'on'
		else :
			stateString = 'off'		
		
		cookString =  str(recorder.getCurrentRecordingElapsedTime())
		
		if CurrentIO.ShouldControl:
			controlStyle = 'Auto'
		else:
			controlStyle = 'Manual'
			
				
		dataDict = {
					'secret':'badass', 
					'target':'periodic_update', 
					'value': { 
								'input':inputList, 
								'set_point': setPoint, 								
								'cook_time': cookString, 
								'output_state': stateString,
								'control_style': controlStyle
							  }
					}
		simpleServer.send(dataDict)
		#self.sendQueue.put(str(dataDict))
		#server.ServerControl.dispatch()
		
	def updateGUI(self):
		setPoint = configuration.Parameters.SetPoint
		controlInput = configuration.Parameters.ControlInput
		controlInputName = configuration.InputList[controlInput].Name
		currentTempList = configuration.Parameters.CurrentTempList
		currentTempName1 = str(configuration.InputList[currentTempList[0]].Name)
		currentTempName2 = str(configuration.InputList[currentTempList[1]].Name)
		dataListDict = {	
							'secret': 'badass', 
							'target': 'initial_update', 
							'value': {
								'set_point_input_name':str(controlInputName),
								'set_point_value':setPoint,
								'current_temp_1_name':currentTempName1,
								'current_temp_2_name':currentTempName2
								}
						}
		
		return str(dataListDict)
		

