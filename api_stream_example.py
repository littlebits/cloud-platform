import json
import thread
import websocket
from time import sleep
from HTMLParser import HTMLParser


ACCESS_TOKEN = "ENTER_YOUR_ACCESS_TOKEN_HERE"
DEVICE_ID = "ENTER_YOUR_DEVICE_ID_HERE"

connected = False
last_message = None

def on_message(ws, message):
    # Data returned is a JSON string wrapped in a string literal
    obj = json.loads(json.loads(message))
    if obj['type'] == 'connection_change':
        if obj['state'] == 0:
            print "Device %s is offline" % obj['from']['device']['id']
        elif obj['state'] == 1:
            print "Device %s connection is unsteady" % obj['from']['device']['id']
        elif obj['state'] == 2:
            print "Device %s is online" % obj['from']['device']['id']
    elif obj['type'] == 'output':
        print "Device %s: output %s %s" % (obj['from']['device']['id'],
            obj['name'], obj['payload'])
    elif obj['type'] == 'input':
        print "Device %s: input %s %s" % (obj['from']['device']['id'],
            obj['name'], obj['payload'])

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
