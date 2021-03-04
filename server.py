import socket
import pickle
from _thread import start_new_thread

def threaded_client(conn, p, gameid):
    conn.send(str.encode(str(p)))
    conn.close()

def main():
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
    games = {}
    idCount = 0

    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)
        idCount += 1
        player_nmbr = 0
        gameId = (idCount - 1)//2
        if idCount % 2 == 1:
            games[gameId] = False
            print("New game created")
        else:
            games[gameId] = True
            player_nmbr = 1

        start_new_thread(threaded_client, (conn, player_nmbr, gameId))

if __name__ == "__main__":
    main()