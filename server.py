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
		print "connection"

	def onOpen(self):
		self.isOpen = True

	#parse the message, and conditionally send the response
	def onMessage(self, payload, isBinary):
		result = parser.JsonParse(payload)
		if result != None:
			print payload
			self.sendMessage(result,False)

	#clear flag isConnected
	def onClose(self, wasClean, code, reason):
		self.isOpen = False
		self.isConnected = False
		if self.factory.handle:
			self.factory.handle = None;
	


class ServerControl:	
	factory = None
    
	port = 9001

	@staticmethod
	def dispatch(self):
		print "dispatching"
		while True:
			try:
				body = self.queue.get(block=False)
			except Queue.Empty:
				print "queue is empty"
				break
			self.factory.handle.sendMessage(body, False)

	#create the server, assign the protocol, start the server
	def start_server(self):		
		self.queue = None
		self.factory = WebSocketServerFactory("ws://localhost:" + str(self.port), debug = False)
		self.factory.protocol = BBQProtocol
		self.factory.handle = None;

		reactor.listenTCP(self.port, self.factory)
		reactor.run()
	
	def setQueue(self, queue):
		self.queue = queue
	
	def isFirstPass(self):
		return self.factory.firstPass

	def clearFirstPass(self):
		self.factory.firstPass = False	

	def callDispatch(self):
		print "attempting to dispatch"
		reactor.callFromThread(self.dispatch)

