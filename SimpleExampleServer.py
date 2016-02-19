'''
The MIT License (MIT)
Copyright (c) 2013 Dave P.
'''

import signal, sys, ssl
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
import parser

class SimpleEcho(WebSocket):

   def handleMessage(self):
      print "handling" + self.data
      result = parser.JsonParse(self.data)
      if result != None:
         print result
         self.sendMessage(result)

   def handleConnected(self):
      pass

   def handleClose(self):
      pass

clients = []
class SimpleChat(WebSocket):

   def handleMessage(self):
      print "handling" + client.data
      for client in clients:
         if client != self:
            
            result = parser.JsonParse(client.data)
            if result != None:
               print result
               client.sendMessage(result)
            #client.sendMessage(self.address[0] + u' - ' + self.data)

   def handleConnected(self):
      print (self.address, 'connected')
      clients.append(self)

   def handleClose(self):
      clients.remove(self)
      print (self.address, 'closed')
      



def start_server():
   cls = SimpleEcho
   server = SimpleWebSocketServer("192.168.0.10", 9001, cls)
   server.serveforever()

