import json
import logging
import thread
import websocket
from time import sleep


ACCESS_TOKEN = "ENTER_YOUR_ACCESS_TOKEN_HERE"
DEVICE_ID = "ENTER_YOUR_DEVICE_ID_HERE"

connected = False

def on_message(ws, message):
    obj = json.loads(message)
    print obj

def on_error(ws, error):
    print "Error: "+str(error)

def on_close(ws):
    print "Disconnected from websocket!"
    connected = False

def on_open(ws):
    print "Connected to websocket"
    msg = '{"name":"subscribe", "args":{"device_id":"%s"}}' % DEVICE_ID
    ws.send(msg)
    connected = True

ws = websocket.WebSocketApp(
    "wss://api-stream.littlebitscloud.cc/primus/?access_token=%s" % ACCESS_TOKEN,
    on_message = on_message, on_error = on_error,
    on_close = on_close, on_open = on_open)
thread.start_new_thread(ws.run_forever, ())
print "Listening: Press Control-C to exit"
while(True):
    if connected:
        ws.send("Hi")
    sleep(10.0)
