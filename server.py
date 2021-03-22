import socket
import pickle
from _thread import start_new_thread
from random import randint

games = {}#games[gameid]=[current_minigame,player0wins,player1wins]
games_data = {}
idCount = 0

def starting_data(gameid):
    if(games[gameid][0]==1):
        games_data[gameid]=[(960/2 - 50,1280/2,960/2),960/2 - 50]#Middle of board, player0 also takes care of ball logic/location
    if(games[gameid][0]==2):
        games_data[gameid]=[[None,None],[None,None]]#(X,Y,Did enemy shot hit)



def threaded_client(conn, player_nmbr, gameid):
    global idCount,games

    def newgame():
        newgame_id=randint(1,2)
        while newgame_id==games[gameid][0]:
            newgame_id=randint(1,2)

        games[gameid][0]=newgame_id
        starting_data(gameid)

    conn.send(str.encode(str(player_nmbr)))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))#New data from player
            if not data:
                break
            if gameid in games:#In case if one player left

                if games[gameid][0]==0:# second player joined, select random minigame
                    newgame()
                #Diffrent data handling
                if data=="gameinfo":#Returns to user id of current minigame and scores
                    conn.sendall(pickle.dumps(games[gameid]))
                elif data=="p0w":#Who won, may change in the future 
                    games[gameid][1]+=1
                    newgame()
                elif data=="p1w":
                    games[gameid][2]+=1
                    newgame()
                #region Pong 
                elif games[gameid][0]==1:
                    if data != "get":
                        games_data[gameid][player_nmbr]=data
                    if data=="get":
                        conn.sendall(pickle.dumps(games_data[gameid][(player_nmbr+1)%2]))#Send back data from another player
                #endregion
                #region Battleships 
                elif games[gameid][0]==2:
                    if data[0] == "matrix":
                        games_data[gameid][player_nmbr][0]=data[1]
                        if player_nmbr==1:
                            games_data[gameid][1][1]=(-1,-1)
                    elif data[0] == "shot":
                        games_data[gameid][(player_nmbr+1)%2][1]=None
                        games_data[gameid][player_nmbr][1]=data[1]
                        conn.sendall(pickle.dumps(games_data[gameid][(player_nmbr+1)%2][0][data[1][0]][data[1][1]]))#Send back data from another player
                    elif data=="get":
                        conn.sendall(pickle.dumps(games_data[gameid][(player_nmbr+1)%2][1]))#Send back data from another player
                #endregion

            else:
                break
        except:
            break

    try:#Clean memory
        if games[gameid][0]==-1:#Player left before second joined
            idCount-=1
        del games[gameid]
        del games_data[gameid]
        print("Closing Game", gameid)
    except:
        pass
    conn.close()

def main():
    global idCount
    ### Server settings
    server = socket.gethostbyname(socket.gethostname())
    port = 1234

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)
    s.listen()
    print("Server Started")
    ###

    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)
        idCount += 1
        gameid = (idCount - 1)//2
        if idCount % 2 == 1:
            games[gameid] = [-1,0,0]
            games_data[gameid] = [0,0]
            print("New game created")
            start_new_thread(threaded_client, (conn, 0, gameid))
        else:
            games[gameid][0]= 0
            print("Second player joined")
            start_new_thread(threaded_client, (conn, 1, gameid))

if __name__ == "__main__":
    main()