import time

import pygame as pygame


class Volleyball:
    def __init__(self, player_nmbr, network):
        if player_nmbr == 0:
            self.images = ['Client_Modules/Volleyball_Assets/pol.png', 'Client_Modules/Volleyball_Assets/rus.png']
        else:
            self.images = ['Client_Modules/Volleyball_Assets/rus.png', 'Client_Modules/Volleyball_Assets/pol.png']
        self.playersX = [0, 0]
        self.playersY = [0, 0]
        self.playersRadius = [0, 0]
        self.playersXSpeed = [0, 0]
        self.playersYSpeed = [0, 0]
        self.playersImg = [None, None]
        self.playersMask = [None, None]

        self.net = network
        self.player_nmbr = player_nmbr
        # pygame.init()
        # pygame.display.set_caption("Volleyball")
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.clock = pygame.time.Clock()

        self.acceleration = 0.2

        self.ballRadius = 25
        self.ballX = self.width / 2 - self.ballRadius
        self.ballY = self.height / 10 - self.ballRadius
        self.ballImg = pygame.image.load('Client_Modules/Volleyball_Assets/ball.png')
        self.ballImg = pygame.transform.scale(self.ballImg, (2 * self.ballRadius, 2 * self.ballRadius))
        self.ballXSpeed = 0
        self.ballYSpeed = 0
        self.ballMask = pygame.mask.from_surface(self.ballImg)

        self.playersRadius[self.player_nmbr] = 50
        self.playersX[self.player_nmbr] = self.width * 3 / 4 - self.playersRadius[self.player_nmbr]
        self.playersY[self.player_nmbr] = self.height * 3 / 4 - self.playersRadius[self.player_nmbr]
        self.playersImg[self.player_nmbr] = pygame.image.load('Client_Modules/Volleyball_Assets/pol.png')
        self.playersImg[self.player_nmbr] = pygame.transform.scale(self.playersImg[self.player_nmbr], (
            2 * self.playersRadius[self.player_nmbr], 2 * self.playersRadius[self.player_nmbr]))
        self.playersXSpeed[self.player_nmbr] = 0
        self.playersYSpeed[self.player_nmbr] = 0
        self.playersMask[self.player_nmbr] = pygame.mask.from_surface(self.playersImg[self.player_nmbr])
        self.playerPoints = 0

        self.playersRadius[(self.player_nmbr + 1) % 2] = 50
        self.playersX[(self.player_nmbr + 1) % 2] = self.width / 4 - self.playersRadius[(self.player_nmbr + 1) % 2]
        self.playersY[(self.player_nmbr + 1) % 2] = self.height * 3 / 4 - self.playersRadius[(self.player_nmbr + 1) % 2]
        self.playersImg[(self.player_nmbr + 1) % 2] = pygame.image.load('Client_Modules/Volleyball_Assets/rus.png')
        self.playersImg[(self.player_nmbr + 1) % 2] = pygame.transform.scale(
            self.playersImg[(self.player_nmbr + 1) % 2],
            (2 * self.playersRadius[(self.player_nmbr + 1) % 2], 2 * self.playersRadius[(self.player_nmbr + 1) % 2]))
        self.playersYSpeed[(self.player_nmbr + 1) % 2] = 0
        self.playersXSpeed[(self.player_nmbr + 1) % 2] = 0
        self.playersMask[(self.player_nmbr + 1) % 2] = pygame.mask.from_surface(
            self.playersImg[(self.player_nmbr + 1) % 2])
        self.enemyPoints = 0

        self.ground = pygame.Rect(0, self.height - 100, self.width, 100)
        self.stick = pygame.Rect(self.width / 2 - 10, self.height * 2 / 5, 20, self.height * 3 / 5 - 100)

        self.initialize_payers()

    def initialize_payers(self):
        self.playersRadius = [50, 50]
        self.playersX = [self.width * 3 / 4 - self.playersRadius[self.player_nmbr],
                         self.width / 4 - self.playersRadius[(self.player_nmbr + 1) % 2]]
        self.playersY = [self.height * 3 / 4 - self.playersRadius[self.player_nmbr],
                         self.height * 3 / 4 - self.playersRadius[(self.player_nmbr + 1) % 2]]
        self.playersXSpeed = [0, 0]
        self.playersYSpeed = [0, 0]
        self.playersImg = [pygame.transform.scale(pygame.image.load(self.images[self.player_nmbr]), (
            2 * self.playersRadius[self.player_nmbr], 2 * self.playersRadius[self.player_nmbr])),
                           pygame.transform.scale(
                               pygame.image.load(self.images[(self.player_nmbr + 1) % 2]),
                               (2 * self.playersRadius[(self.player_nmbr + 1) % 2],
                                2 * self.playersRadius[(self.player_nmbr + 1) % 2]))
                           ]
        self.playersMask = [pygame.mask.from_surface(self.playersImg[self.player_nmbr]),
                            pygame.mask.from_surface(self.playersImg[(self.player_nmbr + 1) % 2])]

    def initialize_ball(self):
        self.ballRadius = 25
        self.ballX = self.width / 2 - self.ballRadius
        self.ballY = self.height / 10 - self.ballRadius
        self.ballXSpeed = 0
        self.ballYSpeed = 0
        self.ballMask = pygame.mask.from_surface(self.ballImg)

    def initialize_player(self):
        self.playersRadius[self.player_nmbr] = 50
        self.playersX[self.player_nmbr] = self.width * 3 / 4 - self.playersRadius[self.player_nmbr]
        self.playersY[self.player_nmbr] = self.height * 3 / 4 - self.playersRadius[self.player_nmbr]
        self.playersXSpeed[self.player_nmbr] = 0
        self.playersYSpeed[self.player_nmbr] = 0
        self.playersMask[self.player_nmbr] = pygame.mask.from_surface(self.playersImg[self.player_nmbr])

    def initialize_enemy(self):
        self.playersRadius[(self.player_nmbr + 1) % 2] = 50
        self.playersX[(self.player_nmbr + 1) % 2] = self.width / 4 - self.playersRadius[(self.player_nmbr + 1) % 2]
        self.playersY[(self.player_nmbr + 1) % 2] = self.height * 3 / 4 - self.playersRadius[(self.player_nmbr + 1) % 2]
        self.playersYSpeed[(self.player_nmbr + 1) % 2] = 0
        self.playersXSpeed[(self.player_nmbr + 1) % 2] = 0
        self.playersMask[(self.player_nmbr + 1) % 2] = pygame.mask.from_surface(
            self.playersImg[(self.player_nmbr + 1) % 2])

    def player(self, x, y):
        self.screen.blit(self.playersImg[self.player_nmbr], (x, y))

    def enemy(self, x, y):
        self.screen.blit(self.playersImg[(self.player_nmbr + 1) % 2], (x, y))

    def ball(self, x, y):
        self.screen.blit(self.ballImg, (x, y))

    def check_collision(self):
        self.ballYSpeed += self.acceleration

        offset = (int(self.ballX - self.playersX[self.player_nmbr]), int(self.ballY - self.playersY[self.player_nmbr]))

        if self.playersMask[self.player_nmbr].overlap(self.ballMask, offset):
            offset_tmp = (
                int(self.ballX - self.playersX[self.player_nmbr]), int(self.ballY - self.playersY[self.player_nmbr]))
            while self.playersMask[self.player_nmbr].overlap(self.ballMask, offset_tmp):
                if self.ballX + self.ballRadius < self.playersX[self.player_nmbr] + self.playersRadius[
                    self.player_nmbr]:
                    self.ballX -= 0.01
                if self.ballX + self.ballRadius > self.playersX[self.player_nmbr] + self.playersRadius[
                    self.player_nmbr]:
                    self.ballX += 0.01
                if self.ballY + self.ballRadius < self.playersY[self.player_nmbr] + self.playersRadius[
                    self.player_nmbr]:
                    self.ballY -= 0.01
                if self.ballY + self.ballRadius > self.playersY[self.player_nmbr] + self.playersRadius[
                    self.player_nmbr]:
                    self.ballY += 0.01
                offset_tmp = (
                    int(self.ballX - self.playersX[self.player_nmbr]),
                    int(self.ballY - self.playersY[self.player_nmbr]))

            self.ballYSpeed = - 0.8 * self.ballYSpeed + self.playersYSpeed[self.player_nmbr]
            self.ballXSpeed = - 0.8 * self.ballXSpeed + self.playersXSpeed[self.player_nmbr]
            # print("kolizja")

        offset_enemy = (int(self.ballX - self.playersX[(self.player_nmbr + 1) % 2]),
                        int(self.ballY - self.playersY[(self.player_nmbr + 1) % 2]))

        if self.playersMask[self.player_nmbr].overlap(self.ballMask, offset_enemy):
            offset_tmp = (int(self.ballX - self.playersX[(self.player_nmbr + 1) % 2]),
                          int(self.ballY - self.playersY[(self.player_nmbr + 1) % 2]))
            while self.playersMask[(self.player_nmbr + 1) % 2].overlap(self.ballMask, offset_tmp):
                if self.ballX + self.ballRadius < self.playersX[(self.player_nmbr + 1) % 2] + self.playersRadius[
                    (self.player_nmbr + 1) % 2]:
                    self.ballX -= 0.01
                if self.ballX + self.ballRadius > self.playersX[(self.player_nmbr + 1) % 2] + self.playersRadius[
                    (self.player_nmbr + 1) % 2]:
                    self.ballX += 0.01
                if self.ballY + self.ballRadius < self.playersY[(self.player_nmbr + 1) % 2] + self.playersRadius[
                    (self.player_nmbr + 1) % 2]:
                    self.ballY -= 0.01
                if self.ballY + self.ballRadius > self.playersY[(self.player_nmbr + 1) % 2] + self.playersRadius[
                    (self.player_nmbr + 1) % 2]:
                    self.ballY += 0.01
                offset_tmp = (int(self.ballX - self.playersX[(self.player_nmbr + 1) % 2]),
                              int(self.ballY - self.playersY[(self.player_nmbr + 1) % 2]))

            self.ballYSpeed = - 0.8 * self.ballYSpeed + self.playersYSpeed[(self.player_nmbr + 1) % 2]
            self.ballXSpeed = - 0.8 * self.ballXSpeed + self.playersXSpeed[(self.player_nmbr + 1) % 2]
            # print("kolizja")

        if self.ballY >= self.height - 100 - 2 * self.ballRadius:
            self.ballYSpeed = - 0.8 * self.ballYSpeed

        if self.ballX <= 0:
            self.ballXSpeed = - self.ballXSpeed
            self.ballX = 0
        if self.ballX >= self.width - 2 * self.ballRadius:
            self.ballXSpeed = - self.ballXSpeed
            self.ballX = self.width - 2 * self.ballRadius

        if (self.width / 2 + 10 >= self.ballX >= self.width / 2 - 10) and \
                self.ballY + self.ballRadius > self.height * 2 / 5:
            self.ballX = self.width / 2 + 10
            self.ballXSpeed = -0.8 * self.ballXSpeed
        if (self.width / 2 + 10 >= self.ballX + 2 * self.ballRadius >= self.width / 2 - 10) and \
                self.ballY + self.ballRadius > self.height * 2 / 5:
            self.ballX = self.width / 2 - 10 - 2 * self.ballRadius
            self.ballXSpeed = -0.8 * self.ballXSpeed

        if self.width / 2 - 10 - 2 * self.ballRadius < self.ballX < self.width / 2 + 10 and \
                self.ballY + 2 * self.ballRadius >= self.height * 2 / 5:
            self.ballY = self.height * 2 / 5 - 2 * self.ballRadius
            self.ballYSpeed = - 0.8 * self.ballYSpeed

        self.ballY += self.ballYSpeed
        self.ballX += self.ballXSpeed

    def run(self):
        while self.net.current_minigame() == 6:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.playersY[self.player_nmbr] >= self.height - 100 - 2 * \
                            self.playersRadius[self.player_nmbr]:
                        self.playersYSpeed[self.player_nmbr] = -12
                    if event.key == pygame.K_LEFT:
                        self.playersXSpeed[self.player_nmbr] = -3
                    if event.key == pygame.K_RIGHT:
                        self.playersXSpeed[self.player_nmbr] = 3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.playersXSpeed[self.player_nmbr] = 0

            self.screen.fill((255, 255, 255))
            pygame.draw.rect(self.screen, (111, 111, 111), pygame.Rect(0, self.height - 100, self.width, 100), 0)
            pygame.draw.rect(self.screen, (111, 111, 111), self.ground, 0)
            pygame.draw.rect(self.screen, (0, 0, 0), self.stick, 0)

            if self.player_nmbr == 0:
                if (self.playersX[self.player_nmbr] <= self.width / 2 + 10 and self.playersXSpeed[
                    self.player_nmbr] < 0) or (
                        self.playersX[self.player_nmbr] + 2 * self.playersRadius[self.player_nmbr] >= self.width and
                        self.playersXSpeed[self.player_nmbr] > 0):
                    self.playersXSpeed[self.player_nmbr] = 0
                self.playersX[self.player_nmbr] += self.playersXSpeed[self.player_nmbr]

                if self.playersX[self.player_nmbr] >= self.width - 2 * self.playersRadius[self.player_nmbr]:
                    self.playersX[self.player_nmbr] = self.width - 2 * self.playersRadius[self.player_nmbr]
            else:
                if (self.playersX[self.player_nmbr] + 2 * self.playersRadius[
                    self.player_nmbr] >= self.width / 2 - 10 and self.playersXSpeed[
                        self.player_nmbr] > 0) or (
                        self.playersX[self.player_nmbr] <= 0 and self.playersXSpeed[self.player_nmbr] < 0):
                    self.playersXSpeed[self.player_nmbr] = 0
                self.playersX[self.player_nmbr] += self.playersXSpeed[self.player_nmbr]

                if self.playersX[self.player_nmbr] <= 0:
                    self.playersX[self.player_nmbr] = 0

            self.playersYSpeed[self.player_nmbr] += self.acceleration
            self.playersY[self.player_nmbr] += self.playersYSpeed[self.player_nmbr]
            if self.playersY[self.player_nmbr] + 2 * self.playersRadius[self.player_nmbr] >= self.height - 100:
                self.playersYSpeed[self.player_nmbr] = 0
                self.playersY[self.player_nmbr] = self.height - 100 - 2 * self.playersRadius[self.player_nmbr]

            if self.player_nmbr == 0:
                self.check_collision()

            # pygame.display.update()
            # if self.player_nmbr == 0:


            if self.player_nmbr == 0:
                self.net.send((6, "both", (
            self.playersX[self.player_nmbr], self.playersY[self.player_nmbr], self.playersXSpeed[self.player_nmbr],
            self.playersYSpeed[self.player_nmbr]), (self.ballX, self.ballY)))
            else:
                self.net.send((6, "player", (
                    self.playersX[self.player_nmbr], self.playersY[self.player_nmbr],
                    self.playersXSpeed[self.player_nmbr],
                    self.playersYSpeed[self.player_nmbr])))
            # else:
            #     self.net.send((6, (self.playersX[(self.player_nmbr + 1) % 2], self.playersY[(self.player_nmbr + 1) % 2], self.playersXSpeed[(self.player_nmbr + 1) % 2], self.playersYSpeed[(self.player_nmbr + 1) % 2]),
            #                    (self.playersX[self.player_nmbr], self.playersY[self.player_nmbr], self.playersXSpeed[self.player_nmbr], self.playersYSpeed[self.player_nmbr]),
            #                    (self.ballX, self.ballY, self.ballXSpeed, self.ballYSpeed)))

            data = self.net.get_data()
            if data == None:
                continue
            elif data[0] != 6:
                break
            else:
                data = data[1]

            # print(data)

            self.playersX[(self.player_nmbr + 1) % 2] = data[0][0]
            self.playersY[(self.player_nmbr + 1) % 2] = data[0][1]
            self.playersXSpeed[(self.player_nmbr + 1) % 2] = data[0][2]
            self.playersYSpeed[(self.player_nmbr + 1) % 2] = data[0][3]

            if self.player_nmbr == 1:
                self.ballX = data[1][0]
                self.ballY = data[1][1]

            self.player(self.playersX[self.player_nmbr], self.playersY[self.player_nmbr])
            self.enemy(self.playersX[(self.player_nmbr + 1) % 2], self.playersY[(self.player_nmbr + 1) % 2])
            self.ball(self.ballX, self.ballY)

            pygame.display.update()

            if self.ballY + 2 * self.ballRadius >= self.height - 100:
                if self.ballX < self.width / 2:
                    self.enemyPoints += 1
                else:
                    self.playerPoints += 1

                # time.sleep(1)
                # self.initialize_player()
                # self.initialize_enemy()
                self.initialize_ball()
                self.initialize_payers()
                pygame.display.update()
                # time.sleep(1)

                if self.player_nmbr == 0:
                    if self.enemyPoints == 3:
                        # pygame.quit()
                        self.net.game_won_by((self.player_nmbr + 1) % 2)
                    if self.playerPoints == 3:
                        # pygame.quit()
                        self.net.game_won_by(self.player_nmbr)

            self.clock.tick(100)
        return True
# game = Volleyball(1, 1)
# game.run()
