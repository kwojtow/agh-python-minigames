import pickle
from random import randint
class Server_snakes:
    def __init__(self):
        self.game_data=[([(0,0)],[0,0]),#First palyer starting position
                        ([(950,950)],[950,950]),#Second player starting position
                        (randint(1,18)*50,randint(1,18)*50)]#First apple location
    def create_apple(self):
        new_position=(randint(0,19)*50,randint(0,19)*50)
        while new_position in self.game_data[0][0] or new_position in self.game_data[1][0]:#TODO Maybe add counter to prevent infinite loop
            new_position=(randint(0,19)*50,randint(0,19)*50)

        self.game_data[2] = new_position

    def receive(self,data,conn,player_nmbr):
        if data=="get":
            conn.sendall(pickle.dumps((5,self.game_data[(player_nmbr+1)%2],self.game_data[2])))#Send back data from another player
        elif data=="ate":
            self.create_apple()
        elif data[0]==5:#Check if player sends current game data
            self.game_data[player_nmbr]=data[1:]
        else:
            conn.sendall(pickle.dumps(None))#We must return something, or client could be stuck on send_recv function
