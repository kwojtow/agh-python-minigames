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

    def current_minigame(self):
        return self.send("gameinfo")[0]

    def score(self):
        return self.send("gameinfo")[1:]

    def get_data(self):
        return self.send("get")

    def game_won_by(self,player_nmbr):
        if player_nmbr==0:
            self.send("p0w")
        elif player_nmbr==1:
            self.send("p1w")

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048*3))
        except socket.error as e:
            print(e)

