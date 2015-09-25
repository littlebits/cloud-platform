import websocket
import thread
import threading
from time import sleep
from random import random
import logging


logger = logging.getLogger(__name__)
class WebsocketMonitor(threading.Thread):

    def on_message(self, message):
        logger.debug(message)
        if self.msg_callback is not None and hasattr(self.msg_callback, '__call__'):
            self.msg_callback(message)

    def on_error(self, error):
        logger.error(error)

    def on_close(self):
        if self.state_callback is not None and hasattr(self.state_callback, '__call__'):
            self.state_callback(False)
        logger.info("websocket closed")
        if self.autoconnect and self.running:
            sleep(0.5+random())
            self.connect()

    def on_open(self):
        if self.state_callback is not None and hasattr(self.state_callback, '__call__'):
            self.state_callback(True)
        logger.info("websocket Opened")

    def connect(self):
        if self.ws is not None:
            self.disconnect()
        self.running = True
        self.abort.clear()
        self.ws = websocket.WebSocketApp(
            "wss://api-stream.littlebitscloud.cc/primus/?access_token=%s" % self.access_token,
            on_message = lambda ws,msg: self.on_message(msg),
            on_error = lambda ws, err: self.on_error(err),
            on_close = lambda ws: self.on_close(),
            on_open = lambda ws: self.on_open())
        thread.start_new_thread(self.ws.run_forever, ())
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def disconnect(self):
        if self.ws is not None:
            self.ws.close()
        self.running = False
        self.abort.set()
        logger.debug("Waiting for pingthread to quit")
        self.join()
        logger.debug("Quit")

    def run(self):
        while(self.running):
            self.abort.wait(self.keepalive)
            if not self.abort.is_set():
                logger.debug("Ping")
                self.ws.send("Hi")

    def __init__(self, access_token, autoconnect=True,
            on_message=None, on_state_change=None, keepalive=10.0):
        self.ws = None
        self.msg_callback = on_message
        self.state_callback = on_state_change
        self.autoconnect = autoconnect
        self.access_token = access_token
        self.keepalive = keepalive
        self.abort = threading.Event()
        self.abort.clear()

#websocket.enableTrace(True)
#self.SUBSCRIBEMSG = '{"name":"subscribe", "args":{"device_id":"%s"}}' % self.device_id
