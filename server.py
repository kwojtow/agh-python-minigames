import socket
import pickle
from _thread import start_new_thread
from random import randint

games = {}
games_data = {}
idCount = 0

def starting_data(gameid):
    if(games[gameid]==1):
        games_data[gameid]=[960/2 - 70,960/2 - 70]

def threaded_client(conn, player_nmbr, gameid):
    global idCount,games
    conn.send(str.encode(str(player_nmbr)))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))#New data from player
            if not data:
                break
            if gameid in games:#In case if one player left

                #Diffrent data handling
                if data=="minigame":#Returns to user id of current minigame
                    conn.sendall(pickle.dumps(games[gameid]))
                elif games[gameid]==0:# second player joined, select random minigame
                    games[gameid]=randint(1,1)
                    starting_data(gameid)
                #region Pong 
                elif games[gameid]==1:
                    if data != "get":
                        games_data[gameid][player_nmbr]=data
                #endregion

                if data!="minigame":
                    conn.sendall(pickle.dumps(games_data[gameid][(player_nmbr+1)%2]))#Send back data from another player
            else:
                break
        except:
            break

    try:#Clean memory
        del games[gameid]
        del games_data[gameid]
        print("Closing Game", gameid)
        idCount -= 1
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
        player_nmbr = 0
        gameid = (idCount - 1)//2
        if idCount % 2 == 1:
            games[gameid] = -1
            games_data[gameid] = [0,0]
            print("New game created")
        else:
            player_nmbr = 1
            games[gameid] = 0
        start_new_thread(threaded_client, (conn, player_nmbr, gameid))

if __name__ == "__main__":
    main()