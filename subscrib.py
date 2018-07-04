import sys
import zmq

port = "7772"
if len(sys.argv) > 1:
   port =  sys.argv[1]
   int(port)

   # Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print ("Collecting updates from ...", port)
socket.connect ("tcp://127.0.0.1:%s" % port)
socket.setsockopt(zmq.SUBSCRIBE, '')
while True:
   msg = socket.recv_json()
   print msg
   
