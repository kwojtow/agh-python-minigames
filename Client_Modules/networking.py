import socket
import pickle
import sys
from retry import retry

class Network:

    def __init__(self):
        socket.setdefaulttimeout(0.1)
        self.server = socket.gethostbyname(socket.gethostname())#Current PC
        self.port = 1234
        self.addr = (self.server, self.port)
        self.player_nmbr = None
        self.connected = False

    def get_player_nmbr(self):
        return self.player_nmbr

    def connect(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            self.client.connect(self.addr)
            self.player_nmbr = self.client.recv(2048).decode()
            self.connected = True
        except:
            print("Connection failed\n")
            raise

    def close(self):
        try:
            self.client.close()
            self.connected = False
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
        if player_nmbr == 0:
            self.send("p0w")
        elif player_nmbr == 1:
            self.send("p1w")

    @retry(tries=10,logger=None)
    def send_recv(self, data):
        self.client.sendall(pickle.dumps(data))
        try:
            data = self.client.recv(2048)
            data = pickle.loads(data)
            if not isinstance(data, (list, tuple)):
                raise socket.timeout
            return data
        except socket.timeout:
            raise

    def send(self, data):
        self.client.sendall(pickle.dumps(data))
