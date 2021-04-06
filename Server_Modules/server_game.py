from random import randint
from Server_Modules.server_battleships import Server_battleships
from Server_Modules.server_pong import Server_pong
import pickle

class Server_game:
    def __init__(self):
        self.gameinfo=[-1,0,0]
        self.game=None

    def newgame(self):
        newgame_id=randint(2,2)
        while newgame_id==self.gameinfo[0]:
            newgame_id=randint(2,2)

        self.gameinfo[0]=newgame_id
        if (newgame_id==1):
            self.game=Server_pong()
        elif (newgame_id==2):
            self.game=Server_battleships()

    def receive(self,data,conn,player_nmbr):
        if self.gameinfo[0]==0:# second player joined, select random minigame
            self.newgame()
        #Diffrent data handling
        if data=="gameinfo":#Returns to user id of current minigame and scores
            conn.sendall(pickle.dumps(self.gameinfo))
        elif data=="p0w":#Who won, may change in the future 
            self.gameinfo[1]+=1
            self.newgame()
        elif data=="p1w":
            self.gameinfo[2]+=1
            self.newgame()
        else:
            self.game.receive(data,conn,player_nmbr)