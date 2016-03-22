import socket
import sys
import updateGUI
import configuration
import data_stream
import time

class Readings():   

    def __init__(self):
        self.sock = None
        data_stream.register_all_streams()

    def getReadings(self):

        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_address = './unix_socket'

        try:
           self.sock.connect(server_address)
        except socket.error, msg:
           sys.exit(1)

        updateString = updateGUI.updateGUI()
        self.sock.send(updateString)

        while True:
            self.buildAndQueueReadingsMessage()
            time.sleep(configuration.Parameters.CollectionPeriod)
         

    def buildAndQueueReadingsMessage(self):
      
        stream_update_list = data_stream.update_all_streams()
        dataDict = {
               'secret':'badass',
               'target':'magic',
               'value': stream_update_list
               }

        self.sock.send(str(dataDict))