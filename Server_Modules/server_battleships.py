import pickle

class Server_battleships:
    def __init__(self):
        self.game_data=[[None,None],[None,None]]#(X,Y,Did enemy shot hit)

    def receive(self,data,conn,player_nmbr):
        if data=="get":
            conn.sendall(pickle.dumps((2,self.game_data[(player_nmbr+1)%2][1])))#Send back data from another player
        elif data[0]==2:#Check if player sends current game data
            if data[1] == "matrix":
                self.game_data[player_nmbr][0]=data[2]
                if player_nmbr==1:
                    self.game_data[1][1]=(-1,-1)
            elif data[1] == "shot":
                self.game_data[(player_nmbr+1)%2][1]=None #Overwrite old shot data
                self.game_data[player_nmbr][1]=data[2] #Save data for second player
                conn.sendall(pickle.dumps((2,self.game_data[(player_nmbr+1)%2][0][data[2][0]][data[2][1]])))#Send result of shot
        else:
            conn.sendall(pickle.dumps(None))#We must return something, or client could be stuck on send_recv function
