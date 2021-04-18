import socket
import pickle


class Network:
    def __init__(self):
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
            return self.client.recv(1024).decode()
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
        print("gettt", self.player_nmbr)
        return self.send_recv("get")

    def game_won_by(self,player_nmbr):
        if player_nmbr==0:
            self.send("p0w")
        elif player_nmbr==1:
            self.send("p1w")

    def send_recv(self, data):
        try:
            print("send_recv", self.player_nmbr)
            self.client.send(pickle.dumps(data))
            print("send_recv2", self.player_nmbr)
            print(data)
            return pickle.loads(self.client.recv(2048*3))
        except socket.error as e:
            print("Enemy left (probably)")
            #print(e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(e)
