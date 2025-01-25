#! /usr/bin/python
import json
import sys
import time
import mpd
import threading
import socket
import queue


lock = threading.Lock()
event_listener_lock = threading.Lock()

server = None
current_state = "idle"

events = queue.Queue()


def write(text):
    output = {"text": text,
              "class": "custom-island",
              "alt": ""}

    sys.stdout.write(json.dumps(output) + "\n")
    sys.stdout.flush()

class MPDThread():
    
    def __init__(self):
        self.run_thread = threading.Thread(target=self.mpd_run, name="mpd", daemon=True)
        self.run_thread.start()

        self.event_thread = threading.Thread(target=self.mpd_event, name="mpd event listener", daemon=True)
        self.event_thread.start()

    @staticmethod
    def mpd_run():
        client = mpd.MPDClient()
        client.connect("127.0.0.1", 6600)
        
        while True:
            MPDThread.mpd_refresh_state(client)
            time.sleep(0.5)
            
    @staticmethod
    def mpd_refresh_state(client):
        global current_state
        try:
            client.ping()
        except mpd.ConnectionError:
            client.connect("127.0.0.1", 6600)
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
        
    @staticmethod
    def mpd_event():
        client = mpd.MPDClient()
        client.connect("127.0.0.1", 6600)
        while True:
            if not event_listener_lock.locked() and current_state == "mpd": # 低优先级
                try:
                    event = events.get_nowait()
                    event: str
                    match event:
                        case "rmbc":
                            if client.status()["state"] != "play":
                                client.play()
                            else:
                                client.pause()
                    MPDThread.mpd_refresh_state(client)
                except queue.Empty:
                    pass
                time.sleep(0.1)
class NotificationThread:     
    def __init__(self):
        self.run_thread = threading.Thread(target=self.noti_run, name="mpd", daemon=True)
        self.run_thread.start()

        self.event_thread = threading.Thread(target=self.noti_event, name="mpd event listener", daemon=True)
        self.event_thread.start()
    
    @staticmethod
    def noti_run():
        pass

    @staticmethod
    def noti_event():
        pass

                            
def client_handler(client: socket.socket):
    data = client.recv(4)
    try:
        events.put_nowait(data.decode())
    except queue.Full:
        pass

def idle_daemon():
    while True:
        if current_state == "idle":
            write(" " *3)
            try:
                events.get_nowait()
            except queue.Empty:
                pass
        time.sleep(1)



if __name__ == "__main__":
    server = socket.create_server(("127.0.0.1", 11451)) 
    server.listen(5)
    threading.Thread(target=idle_daemon, daemon=True).start()
    mpd_thread = MPDThread()
    noti_thread = NotificationThread()
    while True:
        client, addr = server.accept()
        threading.Thread(target=client_handler, args=(client, ), daemon=True).start()
        
    
