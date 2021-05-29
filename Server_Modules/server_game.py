from random import randint
import pickle

from Server_Modules.server_battleships import Server_battleships
from Server_Modules.server_pong import Server_pong
from Server_Modules.server_papersoccer import Server_papersoccer
from Server_Modules.server_flappybird import Server_flappybird
from Server_Modules.server_race import Server_race
from Server_Modules.server_snakes import Server_snakes
from Server_Modules.server_bomberman import Server_bomberman
from Server_Modules.server_volleyball import Server_volleyball


class Server_game:
    def __init__(self):
        self.gameinfo=[-1,0,0]
        self.game=None
        self.games = [Server_pong,Server_battleships,Server_papersoccer,Server_flappybird,Server_snakes,Server_bomberman,Server_volleyball,Server_race]
    def newgame(self):
        newgame_id=3
        while newgame_id==self.gameinfo[0]:
            newgame_id=1

        self.gameinfo[0]=newgame_id
        self.game = self.games[newgame_id-1]()

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