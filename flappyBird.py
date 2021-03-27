import pygame, sys, random
from networking import Network
import pickle


class FlappyBird:
    def __init__(self, player_nmbr, network):
        self.net = network
        self.player_nmbr = player_nmbr
        pygame.init()
        pygame.display.set_caption('FlappyBird')

        self.screen = pygame.display.set_mode((600, 800))

        self.running = True

        self.playerImg = pygame.image.load('/home/krzysztof/Dokumenty/semestr4/testGit/Minigames_pvp-Tchlix/bird.png')
        self.playerImg = pygame.transform.scale(self.playerImg, (50, 50))
        self.playerX = 300
        self.playerY = 400

        self.enemyImg = pygame.image.load('/home/krzysztof/Dokumenty/semestr4/testGit/Minigames_pvp-Tchlix/bird.png')
        self.enemyImg = pygame.transform.scale(self.enemyImg, (50, 50))
        self.enemyX = 300
        self.enemyY = 400

        self.brickImg = pygame.image.load('/home/krzysztof/Dokumenty/semestr4/testGit/Minigames_pvp-Tchlix/brickwall.png')
        self.brickImg = pygame.transform.scale(self.brickImg, (50, 50))
        self.bricksX = [600, 900]
        self.holes = [random.randint(1, 14), random.randint(1, 14)]

        self.downSped = 0
        self.downAcceleration = 0

    def player(self, x, y):
        self.screen.blit(self.playerImg, (x, y))
    def enemy(self, x, y):
        self.screen.blit(self.enemyImg, (x, y))

    def random_bricks_position(self):
        for i in range(len(self.bricksX)):
            if self.bricksX[i] < -50:
                self.holes[i] = random.randint(1, 14)

        for k in range(len(self.bricksX)):
            for j in range(16):
                if j == self.holes[k] or j - 1 == self.holes[k] or j + 1 == self.holes[k]:
                    continue
                self.screen.blit(self.brickImg, (self.bricksX[k], 50 * j))

    def crash(self):
        result = False
        if self.playerY <= 0 or self.playerY >= 750:
            result = True
        for i in range(2):
            if self.playerX + 50 >= self.bricksX[i] and self.playerX <= self.bricksX[i] + 50:
                if self.playerY <= (self.holes[i] - 1) * 50 or self.playerY >= (self.holes[i] + 1) * 50:
                    result = True
        return result

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.downSped = -6
                        self.downAcceleration = 0.3

            self.screen.fill((255, 255, 255))

            self.playerY += self.downSped
            for i in range(len(self.bricksX)):
                self.bricksX[i] -= 1
                if self.bricksX[i] < -51:
                    self.bricksX[i] = 600
            self.downSped += self.downAcceleration
            self.player(self.playerX, self.playerY)
            self.enemy(self.enemyX, self.enemyY)
            self.random_bricks_position()
            if self.crash():
                print("!!!!!!!!!!!!! CRASH !!!!!!!!!!!!!!!")
                self.net.game_won_by((self.player_nmbr + 1) % 2)

            self.net.send((self.playerX, self.playerY, self.holes))

            data = self.net.get_data()

            if data != 0:
                if self.player_nmbr == 1:
                    self.holes = data[2]

                self.enemyX = data[0]
                self.enemyY = data[1]

            pygame.display.update()
            pygame.time.Clock().tick(100)


# game = FlappyBird(1,1)
# game.run()
