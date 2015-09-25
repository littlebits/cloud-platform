import json
import logging
from websocket_monitor import WebsocketMonitor


ACCESS_TOKEN = "ENTER_YOUR_ACCESS_TOKEN_HERE"
DEVICE_ID = "ENTER_YOUR_DEVICE_ID_HERE"

def on_message(message):
    obj = json.loads(message)
    print obj

def on_state_change(connected):
    if connected:
        print "Connected to websocket"
        msg = '{"name":"subscribe", "args":{"device_id":"%s"}}' % DEVICE_ID
        mon.ws.send(msg)
    else:
        print "Disconnected from websocket"

logging.basicConfig(level=logging.INFO)
mon = WebsocketMonitor(ACCESS_TOKEN, on_message=on_message,
        on_state_change=on_state_change)
mon.connect()
_ = raw_input("Press enter to quit\n")
mon.disconnect()
