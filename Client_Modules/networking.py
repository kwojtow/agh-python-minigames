import socket
import pickle
import sys
from retry import retry

class Network:
    def __init__(self):
        socket.setdefaulttimeout(0.1)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        self.server = socket.gethostbyname(socket.gethostname())#FOR DEBUG ONLY<--------------------
        self.server='192.168.100.99'
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
            print("Connection failed\n")
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

    @retry(tries=10)
    def send_recv(self, data):
        try:
            self.client.sendall(pickle.dumps(data))
            data=self.client.recv(2048)
            data = pickle.loads(data)#Temporary
            print(data)
            return data
        except socket.timeout:
            print("LAG\n")
            raise

    def send(self, data):
        self.client.sendall(pickle.dumps(data))
