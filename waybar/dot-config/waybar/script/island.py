#! /usr/bin/python
import json
import sys
import time
import mpd
import threading
import socket
import queue


lock = threading.Lock()

server = None
current_state = "idle"

events = queue.Queue()

write_index = 0
prev_text = ""
def write(text):
    # if len(text) > 5:
    #     if text == prev_text:
    #         write_index += 1
    #     else:
    #         prev_text = text
    #     if len(text) < write_index:
    #         write_index = 0
    #     text = "".join(text[write_index:])    
    # bug
    output = {"text": text,
              "class": "custom-island",
              "alt": ""}

    sys.stdout.write(json.dumps(output) + "\n")
    sys.stdout.flush()

def try_connect_mpd(client):
    try:
        client.ping()
    except mpd.ConnectionError:
        while True:
            try:
                client.connect("127.0.0.1", 6600)
            except mpd.ConnectionError:
                time.sleep(10)
                continue
            else:
                break

class MPDThread():
    
    def __init__(self):
        self.run_thread = threading.Thread(target=self.mpd_run, name="mpd", daemon=True)
        self.run_thread.start()




    @staticmethod
    def mpd_run():
        client = mpd.MPDClient()
        try_connect_mpd(client)
        
        while True:
            MPDThread.mpd_refresh_state(client)
            time.sleep(0.5)
            if current_state == "idle":
                write(" "*3)
                time.sleep(0.5)
            
    @staticmethod
    def mpd_refresh_state(client):
        global current_state
        try_connect_mpd(client)
        try:
            info = client.currentsong()["file"].split(".")[0]
        except KeyError:
            if current_state == "mpd" and not lock.locked():
                current_state = "idle"
            return
        if client.status()["state"] == "play":
            info = "" + " "*3 + info
        else: 
            info = "" + " "*3 + info 
        if not lock.locked():
            current_state = "mpd"
            write(info)
class MPDEventHandler:
    def __init__(self):
        self.client = mpd.MPDClient()
        self.client.connect("127.0.0.1", 6600)
        
    def handle(self, event):
        try_connect_mpd(self.client)
        match event:
            case "rmbc":
                if self.client.status()["state"] != "play":
                    self.client.play()
                else:
                    self.client.pause()
        MPDThread.mpd_refresh_state(self.client)

class NotificationThread:     
    def __init__(self):
        self.run_thread = threading.Thread(target=self.noti_run, name="mpd", daemon=True)
        self.run_thread.start()
    
    @staticmethod
    def noti_run():
        pass

                            
mpd_handler = MPDEventHandler()
mpd_lock = threading.Lock()
def client_handler(client: socket.socket):
    data = client.recv(4)
    event = data.decode()
    match current_state:
        case "idle":
            pass
        case "mpd":
            mpd_lock.acquire()
            mpd_handler.handle(event)
            mpd_lock.release()



if __name__ == "__main__":
    server = socket.create_server(("127.0.0.1", 11451)) 
    server.listen(5)
    mpd_thread = MPDThread()
    noti_thread = NotificationThread()
    while True:
        client, addr = server.accept()
        threading.Thread(target=client_handler, args=(client, ), daemon=True).start()
        
    
