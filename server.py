import socket
import pickle
from _thread import start_new_thread
from Server_Modules.server_game import Server_game

games = {}
idCount = 0

def threaded_client(conn, player_nmbr, gameid):
    global idCount
    conn.send(str(player_nmbr).encode())

    #Data recv loop
    while True:
        try:
            data = conn.recv(2048)
            if not data: 
                break
            data = pickle.loads(data)#New data from player
            if gameid in games:#In case if one player left and deleted the game
                games[gameid].receive(data, conn, player_nmbr)
            else:
                break
        except Exception as e:
            break

    try:#Clean memory
        if gameid in games:
            if games[gameid].gameinfo[0] == -1:#Player left before second joined
                idCount -= 1
            del games[gameid]
            print("Closing Game", gameid)
    except Exception as e:
        print(e)
    finally:
        conn.close()

def main():
    global idCount
    ### Server settings
    server = socket.gethostbyname(socket.gethostname())
    port = 1234

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
    try:
        sock.bind((server, port))
    except socket.error as e:
        print(e)
    sock.listen()
    print("Server Started")
    ###

    while True:
        conn, addr = sock.accept()
        conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        print("Connected to:", addr)
        idCount += 1
        gameid = (idCount - 1) // 2
        if idCount % 2 == 1:
            games[gameid] = Server_game()
            print("New game created")
            start_new_thread(threaded_client, (conn, 0, gameid))
        else:
            games[gameid].gameinfo[0] = 0
            print("Second player joined")
            start_new_thread(threaded_client, (conn, 1, gameid))

if __name__ == "__main__":
    main()
