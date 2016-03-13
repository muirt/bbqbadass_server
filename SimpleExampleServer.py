'''
The MIT License (MIT)
Copyright (c) 2013 Dave P.
'''

import signal, sys, ssl, socket
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
from optparse import OptionParser
import threading
import os

import parser
import readings

import json
import configuration
import Queue
import CurrentIO
import grapher
import jCmd
import unicodeHelper
import updateGUI


class SimpleEcho(WebSocket):
  
   def handleMessage(self):
      result = parser.JsonParse(self.data)      
      if result != None:
         self.sendMessage(result)    

   def handleConnected(self):      
      updateString = updateGUI.updateGUI() 
      self.sendMessage(updateString)
      
      logs = grapher.get_all_files()
      log_dict_list = []      
      for log in logs:
         log_dict = {}
         log_dict["name"] = log
         log_dict["duration"] = "1h32m"
         log_dict_list.append(log_dict)

      result = jCmd.placeResponseInMessage("logs", str(log_dict_list), 'saved_logs')
      self.sendMessage(result)

   def handleClose(self):
      pass

clients = []
class SimpleChat(WebSocket):

   def handleMessage(self):
      for client in clients:
         if client != self:
            client.sendMessage(self.address[0] + u' - ' + self.data)

   def handleConnected(self):
      print (self.address, 'connected')
      for client in clients:
         client.sendMessage(self.address[0] + u' - connected')
      clients.append(self)

   def handleClose(self):
      clients.remove(self)
      print (self.address, 'closed')
      for client in clients:
         client.sendMessage(self.address[0] + u' - disconnected')



   

def start_server():
   parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
   parser.add_option("--host", default='', type='string', action="store", dest="host", help="hostname (localhost)")
   parser.add_option("--port", default=9001, type='int', action="store", dest="port", help="port (9001)")
   parser.add_option("--example", default='echo', type='string', action="store", dest="example", help="echo, chat")
   parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
   parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
   parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")

   (options, args) = parser.parse_args()

   os.system("rm ./unix_socket")
   cls = SimpleEcho
   if options.example == 'chat':
      cls = SimpleChat

   if options.ssl == 1:
      server = SimpleSSLWebSocketServer(options.host, options.port, cls, options.cert, options.cert, version=options.ver)
   else:
      server = SimpleWebSocketServer(options.host, options.port, cls)

   # def close_sig_handler(signal, frame):
   #    server.close()
   #    sys.exit()

   # serverThread = threading.Thread(target=other_thread)
   # serverThread.daemon = True
   # serverThread.start()

   #signal.signal(signal.SIGINT, close_sig_handler)

   server.serveforever()
