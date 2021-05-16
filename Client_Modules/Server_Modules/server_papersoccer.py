import pickle

class Server_papersoccer:
    def __init__(self):
        self.game_data=None

    def receive(self,data,conn,player_nmbr):
        if data=="get":
            conn.sendall(pickle.dumps((3,self.game_data)))#Send back data from another player
        elif data[0]==3:#Check if player sends current game data
            self.game_data = data[1:]
        else:
            conn.sendall(pickle.dumps(None))#We must return something, or client could be stuck on send_recv function
