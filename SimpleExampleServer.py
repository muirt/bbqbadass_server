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
import data_stream

class BBQClient():
   def __init__(self, websocket, number):
      self.player_number = number
      self.websocket = websocket

clients = []
max_clients = 3



def enumerate_client():
   player_sum = 0
   result = 0 
   clients_found = []
   
   for client in clients:
      clients_found.append(client.player_number)

   for index in range(max_clients):
      if index + 1 not in clients_found:
         result = index + 1  
         break 

   return result



class SimpleEcho(WebSocket):
  
   def handleMessage(self):

      for client in clients:
         if client.websocket == self:            
            result = parser.JsonParse(self.data, client.player_number)
            if result != None:               
               if result['message_type'] == "multiple":                  
                  for index, message in enumerate(result['messages']):                     
                     for outClient in clients:                        
                        if outClient.player_number == index+1:
                           outClient.websocket.sendMessageSemi(str(message))
   
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

      if player_number < 3:
         result = data_stream.get_json('player_token', player_number)
         self.sendMessage(result)

      if player_number == 3:
         result = data_stream.get_json('clear_board', player_number)
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

  

def start_server():
   parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
   parser.add_option("--host", default='', type='string', action="store", dest="host", help="hostname (localhost)")
   parser.add_option("--port", default=9001, type='int', action="store", dest="port", help="port (9001)")
   parser.add_option("--example", default='echo', type='string', action="store", dest="example", help="echo, chat")
   parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
   parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
   parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")

   (options, args) = parser.parse_args()

   data_stream.register_all_streams()

   os.system("rm ./unix_socket")
   cls = SimpleEcho
   if options.example == 'chat':
      cls = SimpleChat

   if options.ssl == 1:
      server = SimpleSSLWebSocketServer(options.host, options.port, cls, options.cert, options.cert, version=options.ver)
   else:
      server = SimpleWebSocketServer(options.host, options.port, cls)

   server.serveforever()
