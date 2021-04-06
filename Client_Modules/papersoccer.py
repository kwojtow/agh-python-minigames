import pygame, sys, random
import time
import pickle


class PaperSoccer:
    def __init__(self, player_nmbr, network):
        self.player_nmbr = player_nmbr
        self.net = network
        # pygame.init()
        self.screen = pygame.display.set_mode((600, 1000))
        # self.screen = pygame.display.get_surface()
        self.height = 8
        self.width = 6
        self.moves = [[[False for i in range(10)] for j in range(self.width + 1)] for k in range(self.height + 3)]
        self.keys = [pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8,
                     pygame.K_KP9]

        for i in range(self.height + 3):
            for j in range(self.width + 1):
                self.moves[i][j][5] = True
                self.moves[i][j][0] = True

        for i in range(self.width + 1):
            for j in range(10):
                self.moves[0][i][j] = True
                self.moves[self.height + 2][i][j] = True

            self.moves[1][i][4] = True
            self.moves[1][i][7] = True
            self.moves[1][i][8] = True
            self.moves[1][i][9] = True
            self.moves[1][i][6] = True

            self.moves[self.height + 1][i][4] = True
            self.moves[self.height + 1][i][1] = True
            self.moves[self.height + 1][i][2] = True
            self.moves[self.height + 1][i][3] = True
            self.moves[self.height + 1][i][6] = True

        for i in range(self.height + 3):
            self.moves[i][0][7] = True
            self.moves[i][0][4] = True
            self.moves[i][0][1] = True
            self.moves[i][0][8] = True
            self.moves[i][0][2] = True
            self.moves[i][self.width][9] = True
            self.moves[i][self.width][6] = True
            self.moves[i][self.width][3] = True
            self.moves[i][self.width][8] = True
            self.moves[i][self.width][2] = True

        self.moves[1][int(self.width / 2 - 1)][9] = False
        self.moves[1][int(self.width / 2 - 1)][6] = False
        self.moves[1][int(self.width / 2)][4] = False
        self.moves[1][int(self.width / 2)][7] = False
        self.moves[1][int(self.width / 2)][8] = False
        self.moves[1][int(self.width / 2)][9] = False
        self.moves[1][int(self.width / 2)][6] = False
        self.moves[1][int(self.width / 2 + 1)][4] = False
        self.moves[1][int(self.width / 2 + 1)][7] = False

        self.moves[self.height + 1][int(self.width / 2 - 1)][3] = False
        self.moves[self.height + 1][int(self.width / 2 - 1)][6] = False
        self.moves[self.height + 1][int(self.width / 2)][4] = False
        self.moves[self.height + 1][int(self.width / 2)][1] = False
        self.moves[self.height + 1][int(self.width / 2)][2] = False
        self.moves[self.height + 1][int(self.width / 2)][3] = False
        self.moves[self.height + 1][int(self.width / 2)][6] = False
        self.moves[self.height + 1][int(self.width / 2 + 1)][4] = False
        self.moves[self.height + 1][int(self.width / 2 + 1)][1] = False

        self.ball_position = (int(100 * self.width / 2), int(100 * (self.height + 2) / 2))

        self.screen.fill((255, 255, 255))

        self.whose_turn = 0
        self.color = pygame.Color(255, 0, 0)
        self.winner = -1

        for i in range(1, self.width):
            pygame.draw.line(self.screen, pygame.Color(222, 222, 222), (100 * i, 0), (100 * i, 100 * (self.height + 2)))

        for i in range(1, self.height + 2):
            pygame.draw.line(self.screen, pygame.Color(222, 222, 222), (0, 100 * i), (100 * self.width, 100 * i))

        self.left_edge = int(100 * (self.width / 2 - 1))
        self.right_edge = int(100 * (self.width / 2 + 1))
        self.half_width = int(100 * (self.width / 2 - 1))

        self.background_color = pygame.Color(255 * ((self.player_nmbr + 1) % 2), 0, 255 * self.player_nmbr)

        pygame.draw.rect(self.screen, self.background_color, (0, 0, self.half_width, 100))
        pygame.draw.rect(self.screen, self.background_color, (self.right_edge, 0, self.half_width, 100))
        pygame.draw.rect(self.screen, self.background_color, (0, 100 * (self.height + 1), self.half_width, 100))
        pygame.draw.rect(self.screen, self.background_color,
                         (int(100 * (self.width / 2 + 1)), 100 * (self.height + 1), self.half_width, 100))
        pygame.draw.polygon(self.screen, pygame.Color(0, 0, 0),
                            [(self.left_edge, 0), (self.right_edge, 0), (self.right_edge, 100), (100 * self.width, 100),
                             (100 * self.width, 100 * (self.height + 1)),
                             (self.right_edge, 100 * (self.height + 1)), (self.right_edge, 100 * (self.height + 2)),
                             (self.left_edge, 100 * (self.height + 2)), (self.left_edge, 100 * (self.height + 1)),
                             (0, 100 * (self.height + 1)),
                             (0, 100), (self.left_edge, 100)
                             ], 3)

    def direction(self, x):
        return {
            1: (-100, 100),
            2: (0, 100),
            3: (100, 100),
            4: (-100, 0),
            6: (100, 0),
            7: (-100, -100),
            8: (0, -100),
            9: (100, -100),
        }[x]

    def move_if_possible(self, dir, ball_pos):
        offset = self.direction(dir)
        if not self.moves[int(ball_pos[1] / 100)][int(ball_pos[0] / 100)][dir]:
            old_position = ball_pos
            ball_pos = (ball_pos[0] + offset[0], ball_pos[1] + offset[1])
            pygame.draw.line(self.screen, self.color, old_position, ball_pos, 3)
            self.moves[int(old_position[1] / 100)][int(old_position[0] / 100)][dir] = True
            self.moves[int(ball_pos[1] / 100)][int(ball_pos[0] / 100)][10 - dir] = True
            if not self.can_still_move(ball_pos) and not self.all_occupied(ball_pos):
                self.whose_turn = (self.whose_turn + 1) % 2
                self.color = pygame.Color(255 * ((self.whose_turn + 1) % 2), 0, 255 * self.whose_turn)

        return ball_pos

    def all_occupied(self, ball_pos):
        all_occupied = True
        for k in self.moves[int(ball_pos[1] / 100)][int(ball_pos[0] / 100)]:
            all_occupied = all_occupied and k
        return all_occupied

    def can_still_move(self, ball_pos):
        all_occupied = self.all_occupied(ball_pos)
        no_occupied = 0
        for k in self.moves[int(ball_pos[1] / 100)][int(ball_pos[0] / 100)]:
            if k:
                no_occupied += 1
        return no_occupied > 3 and not all_occupied

    def key_value(self, key):
        return {
            pygame.K_KP1: 1,
            pygame.K_KP2: 2,
            pygame.K_KP3: 3,
            pygame.K_KP4: 4,
            pygame.K_KP6: 6,
            pygame.K_KP7: 7,
            pygame.K_KP8: 8,
            pygame.K_KP9: 9,
        }[key]

    def run(self):
        while self.net.current_minigame() == 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.whose_turn == self.player_nmbr and event.type == pygame.KEYDOWN:
                    if event.key in self.keys:
                        self.ball_position = self.move_if_possible(self.key_value(event.key), self.ball_position)
                        self.net.send((3,self.key_value(event.key), self.ball_position))

            data = self.net.get_data()
            if(data[0]!=3):
                break
            else:
                data=data[1]
            # print(self.net.get_data())
            if data != None:
                # self.whose_turn = data[2]
                self.color = pygame.Color(255 * ((self.whose_turn + 1) % 2), 0, 255 * self.whose_turn)
                if data[1] != self.ball_position:
                    self.ball_position = self.move_if_possible(data[0], self.ball_position)

            if not self.can_still_move(self.ball_position) and self.all_occupied(self.ball_position) and not (self.ball_position[1] == 0 or self.ball_position[1] == (100 * (self.height + 2))):
                print("Winner: ", (self.whose_turn + 1) % 2)
                self.winner = (self.whose_turn + 1) % 2
            elif self.ball_position[1] == 0 or self.ball_position[1] == (100 * (self.height + 2)):
                print("Winner: ", self.whose_turn)
                self.winner = self.whose_turn



            pygame.draw.circle(self.screen, self.color, self.ball_position, 5)

            pygame.display.update()

            if self.winner > -1:
                time.sleep(1)
                self.net.game_won_by(self.winner)

            pygame.time.Clock().tick(100)