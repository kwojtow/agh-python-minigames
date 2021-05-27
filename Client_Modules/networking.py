import socket
import pickle
import sys
from retry import retry

class Network:
    def __init__(self):
        socket.setdefaulttimeout(0.3)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())#FOR DEBUG ONLY<--------------------
        self.port = 1234
        self.addr = (self.server, self.port)
        self.player_nmbr = self.connect()

    def get_player_nmbr(self):
        return self.player_nmbr

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            print("Connection failed")
            raise

    def close(self):
        try:
            self.client.close()
        except:
            print("Close failed")
            raise

    def current_minigame(self):
        return self.send_recv("gameinfo")[0]

    def score(self):
        return self.send_recv("gameinfo")[1:]

    def get_data(self):
        return self.send_recv("get")

    def game_won_by(self,player_nmbr):
        if player_nmbr==0:
            self.send("p0w")
        elif player_nmbr==1:
            self.send("p1w")

    @retry(tries=3)
    def send_recv(self, data):
        self.client.send(pickle.dumps(data))
        data=self.client.recv(2048)
        return pickle.loads(data)

    def send(self, data):
        self.client.send(pickle.dumps(data))
