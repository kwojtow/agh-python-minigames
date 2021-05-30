import pygame
import random


class Character(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.bottom = y
        self.group = pygame.sprite.Group()
        self.group.add(self)

    def draw(self, surface):
        self.group.draw(surface)

    def crash(self, walls):
        for wall in walls:
            for brick in wall.bricks:
                if pygame.sprite.collide_mask(self, brick):
                    print('kolizja')
                    return True
        return False


class Brick(pygame.sprite.Sprite):
    def __init__(self, image_path, postion):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = postion


class Wall:
    def __init__(self, image_path, x):
        self.x = x
        self.hole = random.randint(1, 14)
        self.bricks = pygame.sprite.Group()
        for i in range(13):
            self.bricks.add(Brick(image_path, (0, 0)))

    def random_hole_position(self):
        if self.x < -50:
            self.hole = random.randint(1, 14)

    def update(self):
        self.x -= 1
        if self.x < -51:
            self.x = 600
        i = 0
        for j in range(16):
            if j == self.hole or j - 1 == self.hole or j + 1 == self.hole:
                continue
            self.bricks.sprites()[i].rect.topleft = (self.x, 50 * j)
            i += 1

    def draw(self, surface):
        self.bricks.draw(surface)


class FlappyBird:
    def __init__(self, player_nmbr, network):
        self.net = network
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.player_nmbr = player_nmbr
        self.enemy_nmbr = (self.player_nmbr + 1) % 2

        self.screen = pygame.display.set_mode((600, 800))

        self.down_speed = 0
        self.down_acceleration = 0

        self.player = Character('Client_Modules/Flappybird_Assets/bird.png', 300, 400)
        self.enemy = Character('Client_Modules/Flappybird_Assets/bird.png', 300, 400)
        self.walls = [Wall('Client_Modules/Flappybird_Assets/brickwall.png', 600),
                      Wall('Client_Modules/Flappybird_Assets/brickwall.png', 900)]

        if self.player_nmbr == 1:
            data = self.net.get_data()
            if data[0]==4 and data[1] != 0:
                data = data[1]
                for i in range(len(data[2])):
                    self.walls[i].hole = data[2][i]

    def crash(self):
        if self.player.crash(self.walls):
            self.net.game_won_by(self.enemy_nmbr)
            return
        elif self.enemy.crash(self.walls):
            self.net.game_won_by(self.player_nmbr)
            return

    def run(self):
        while self.net.current_minigame() == 4:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.down_speed = -6
                        self.down_acceleration = 0.3

            self.screen.fill((255, 255, 255))

            for i in range(len(self.walls)):
                self.walls[i].update()

            data = self.net.get_data()
            if data[0] != 4:
                break
            else:
                data = data[1]

            if data != 0:
                if self.player_nmbr == 1:
                    for i in range(len(data[2])):
                        self.walls[i].hole = data[2][i]

                self.enemy.rect.x = data[0]
                self.enemy.rect.y = data[1]

            if self.player_nmbr == 0:
                for i in range(len(self.walls)):
                    self.walls[i].random_hole_position()

            for wall in self.walls:
                wall.draw(self.screen)

            self.enemy.draw(self.screen)

            self.player.rect.y += self.down_speed
            self.down_speed += self.down_acceleration
            self.player.draw(self.screen)

            self.net.send((4, self.player.rect.x, self.player.rect.y, [self.walls[0].hole, self.walls[1].hole]))

            pygame.display.update()

            if self.player_nmbr == 0:
                self.crash()

            self.clock.tick(self.FPS)

        return True
