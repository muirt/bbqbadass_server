from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer


clients = []

class SimpleServer(WebSocket):

   def handleMessage(self):
      print self.data

   def handleConnected(self):
      print "connected"
      clients.append(self)
      

   def handleClose(self):
      clients.remove(self)
      


def start_server():
   cls = SimpleServer   
   server = SimpleWebSocketServer("192.168.0.10", 9001, cls)   
   server.serveforever()

def send(message):

   for client in clients:
      client.sendMessage(message)