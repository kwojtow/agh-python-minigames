import pickle

class Server_pong:
    def __init__(self):
        self.game_data=[(960/2 - 50,1280/2,960/2),960/2 - 50]#Middle of board, player0 also takes care of ball logic/location

    def receive(self,data,conn,player_nmbr):
        if data=="get":
            conn.sendall(pickle.dumps((1,self.game_data[(player_nmbr+1)%2])))#Send back data from another player
        elif data[0]==1:#Check if player sends current game data
            self.game_data[player_nmbr]=data[1]
        else:
            conn.sendall(pickle.dumps(None))#We must return something, or client could be stuck on send_recv function
