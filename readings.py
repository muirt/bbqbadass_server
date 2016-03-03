import socket
import sys
import updateGUI
import configuration
import CurrentIO
import unicodeHelper

import time

class Readings():   

   def __init__(self):
      self.sock = None

   def getReadings(self):        

      self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

      server_address = './unix_socket'
      
      try:
         self.sock.connect(server_address)
      except socket.error, msg:
         sys.exit(1)

      updateString = updateGUI.updateGUI() 
       
      while True:             
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
      hysteresis = str(configuration.Parameters.Hysteresis)
      outputState = CurrentIO.getOutputState('controlOutput')
      stateString = ''
      
      if outputState:
         stateString = 'on'
      else :
         stateString = 'off'     
      
      cookString =  "0h00m" #str(recorder.getCurrentRecordingElapsedTime()) #phant TODO
      
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
                        'control_style': controlStyle,
                        'hysteresis': hysteresis,
                       }
               }
      self.sock.send(str(dataDict))
 