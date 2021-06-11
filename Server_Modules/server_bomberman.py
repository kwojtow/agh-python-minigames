import pickle
from Client_Modules.bomberman import Bomb

class Server_bomberman:
    def __init__(self):
        self.game_data=[([50, 50],[]),#First palyer starting position,Bombs
                        ([850, 850],[])]#Second player starting position,Bombs

    def receive(self,data,conn,player_nmbr):
        if data == "get":
            conn.sendall(pickle.dumps((6, self.game_data[(player_nmbr+1)%2])))#Send back data from another player
        elif data[0] == 6:#Check if player sends current game data
            self.game_data[player_nmbr]=data[1:]
        else:
            conn.sendall(pickle.dumps(None))#We must return something, or client could be stuck on send_recv function
