import pickle


class Server_volleyball:
    def __init__(self):
        self.width = 1200
        self.height = 800
        self.playerRadius = 50
        self.enemyRadius = 50
        self.ballRadius = 25
        self.game_data = [(self.width * 3 / 4 - self.playerRadius, self.height * 3 / 4 - self.playerRadius, 0, 0),  # first player position x,y speed x,y
                          (self.width / 4 - self.enemyRadius, self.height * 3 / 4 - self.enemyRadius, 0, 0),  # second player position x,y, speed x,y
                          (self.width / 2 - self.ballRadius, self.height / 10 - self.ballRadius)]  # ball position x,y, speed x,y

    def receive(self, data, conn, player_nmbr):
        if data == "get":
            conn.sendall(pickle.dumps((6, (self.game_data[(player_nmbr + 1) % 2], self.game_data[2]))))  # Send back data from another player
        elif data[0] == 6:  # Check if player sends current game data
            if data[1] == "player":
                self.game_data[player_nmbr] = data[2]
            if data[1] == "both":
                self.game_data[player_nmbr] = data[2]
                self.game_data[2] = data[3]
        else:
            conn.sendall(pickle.dumps(None))  # We must return something, or client could be stuck on send_recv function
