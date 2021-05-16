import pickle


class Server_race:
    def __init__(self):
        self.game_data = [((0, 0,), 0), ((0, 0,), 0), []]  # player0 speed,score, player1 speed,score, obstacles list

    def receive(self, data, conn, player_nmbr):
        if data == "get":
            conn.sendall(pickle.dumps((7, self.game_data[(player_nmbr + 1) % 2], self.game_data[2])))
        elif data[0] == 7:  # Check if player sends current game data
            self.game_data[player_nmbr] = data[1]
            if player_nmbr == 0:
                self.game_data[2] = data[2]
        else:
            conn.sendall(pickle.dumps(None))  # We must return something, or client could be stuck on send_recv function
