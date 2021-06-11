import pickle

class Server_flappybird:
    def __init__(self):
        self.game_data = [0, 0]

    def receive(self,data,conn,player_nmbr):
        if data == "get":
            conn.sendall(pickle.dumps((4,self.game_data[(player_nmbr + 1) % 2])))#Send back data from another player
        elif data[0] == 4:#Check if player sends current game data
            self.game_data[player_nmbr] = data[1:]
        else:
            conn.sendall(pickle.dumps(None))#We must return something, or client could be stuck on send_recv function
