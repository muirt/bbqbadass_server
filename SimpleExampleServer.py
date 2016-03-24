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
import datetime
import filesystem
import timeHelper
import responseWrapper

class BBQClient():
   def __init__(self, websocket, number):
      self.player_number = number
      self.websocket = websocket

clients = []

def enumerate_client():
   player_sum = 0
   result = 1 # assume no clients
   for client in clients:
      player_sum += client.player_number

   # if there is either a 1 or a 2, return the other
   # if both, dont allow more clients
   # if none, default value is 1
   if player_sum:
      result = 3 - player_sum

   return result



class SimpleEcho(WebSocket):
  
   def handleMessage(self):

      for client in clients:
         if client.websocket == self:
            
            result = parser.JsonParse(self.data)
            if result != None:
               self.sendMessageSemi(result)
      
      # result = parser.JsonParse(self.data)      
      # if result != None:
      #    self.sendMessageSemi(result)       

   def sendMessageSemi(self, message):
      self.sendMessage(message + ";")

   def handleConnected(self):      
      
      player_number = enumerate_client()
      
      if player_number:
         client = BBQClient(self, player_number)
         clients.append(client)
      else:
         self.close()
         return

      
      updateString = updateGUI.updateGUI() 
      self.sendMessage(updateString)

      log_dict_list = grapher.get_log_file_details()

      result = self.placeResponseInMessage("logs", str(log_dict_list), 'saved_logs')
      self.sendMessage(result)

      log_dict_list = grapher.get_current_log_file_details()
      result = self.placeResponseInMessage("log", str(log_dict_list), 'current_log')
      
      self.sendMessage(result)

   def handleClose(self):
      for client in clients:
         if client.websocket == self:
            clients.remove(client)

   
   def placeResponseInMessage(self, string, val, key):

      messageDict = {
            'secret':'badass', 
            'target':key, 
            'value': { 
                     string: val
                    }
            }
      return  str(messageDict).replace('"', ' ')

# clients = []
# class SimpleChat(WebSocket):

#    def handleMessage(self):
#       for client in clients:
#          if client != self:
#             client.sendMessage(self.address[0] + u' - ' + self.data)

#    def handleConnected(self):
#       print (self.address, 'connected')
#       for client in clients:
#          client.sendMessage(self.address[0] + u' - connected')
#       clients.append(self)

#    def handleClose(self):
#       clients.remove(self)
#       print (self.address, 'closed')
#       for client in clients:
#          client.sendMessage(self.address[0] + u' - disconnected')



   

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
