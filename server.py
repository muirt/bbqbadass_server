from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                       WebSocketServerFactory
import sys

from twisted.python import log
from twisted.internet import reactor
import parser
import threading
import time

import recorder

import json
import configuration
import Queue
import CurrentIO
import debugger
import unicodeHelper


class BBQProtocol(WebSocketServerProtocol):

	
	#set two flags, isConnected, and firstPass
	def onConnect(self, request):		
		self.isConnected = True
		self.factory.handle = self;
		self.factory.firstPass = True

	def onOpen(self):
		self.isOpen = True

	#parse the message, and conditionally send the response
	def onMessage(self, payload, isBinary):
		result = parser.JsonParse(payload)
		if result != None:
			self.sendMessage(result,False)

	#clear flag isConnected
	def onClose(self, wasClean, code, reason):
		self.isOpen = False
		self.isConnected = False
		if self.factory.handle:
			self.factory.handle = None;
	


class ServerControl:	
	factory = None
	sendQueue = Queue.Queue()
	configuration.Load()
	port = 9001

	def dispatch(self):
		while True:
			try:
				body = self.sendQueue.get(block=False)
			except Queue.Empty:				
				break
			self.factory.handle.sendMessage(body, False)

	#create the server, assign the protocol, start the server
	def start_server(self):		
		
		self.factory = WebSocketServerFactory("ws://localhost:" + str(self.port), debug = False)
		self.factory.protocol = BBQProtocol
		self.factory.handle = None;

		reactor.listenTCP(self.port, self.factory)
		reactor.run()
	
	def getReadings(self):
		
		while True:		
			if self.factory != None:	
				if self.factory.handle != None:
					if self.factory.firstPass:
						updateString = self.updateGUI()
						self.sendQueue.put(updateString)
						reactor.callFromThread(self.dispatch)
						                   
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
		#simpleServer.send(dataDict)
		self.sendQueue.put(str(dataDict))
		reactor.callFromThread(self.dispatch)
		
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
		



