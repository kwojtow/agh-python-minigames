import time

import pygame
import pymunk


def convert_coordinates(point):
    return point[0], 800 - point[1]


class Player(pygame.sprite.Sprite):
    size = (100, 100)
    speed = [0, 0]

    def __init__(self, initial_position,
                 image_path):  # initial position is a tuple of center x and y in cartesian system
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path), self.size)
        self.rect = self.image.get_rect()
        self.rect.center = convert_coordinates(initial_position)

        self.body = pymunk.Body()
        self.body.position = initial_position
        self.shape = pymunk.Circle(self.body, self.size[0] // 2)
        self.shape.density = 10
        self.shape.elasticity = 0.5


class Ball(pygame.sprite.Sprite):
    size = (50, 50)

    def __init__(self, initial_position,
                 image_path):  # initial position is a tuple of center x and y in cartesian system
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path), self.size)
        self.rect = self.image.get_rect()
        self.rect.center = convert_coordinates(initial_position)

        self.body = pymunk.Body()
        self.body.position = initial_position
        self.shape = pymunk.Circle(self.body, self.size[0] // 2)
        self.shape.density = 1
        self.shape.elasticity = 1


class Stick(pygame.sprite.Sprite):
    def __init__(self, size, centerx, bottom):
        super().__init__()
        self.image = self.image = pygame.transform.scale(
            pygame.image.load('Client_Modules/Volleyball_Assets/stick.png'), size)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, convert_coordinates((self.rect.centerx, self.rect.bottom)),
                                    convert_coordinates((self.rect.centerx, self.rect.top + self.rect.width // 2)),
                                    self.rect.width // 2)
        self.shape.elasticity = 0.8


class Ground(pygame.sprite.Sprite):
    def __init__(self, size, parent_width, parent_height):
        super().__init__()
        self.image = self.image = pygame.transform.scale(pygame.image.load('Client_Modules/Volleyball_Assets/sand.jpg'),
                                                         size)
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.bottom = parent_height

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (0, 0), (parent_width, 0), self.rect.height)
        self.shape.elasticity = 0
        # self.shape.friction = 3500000000


class Volleyball:
    def __init__(self, player_nmbr, network):
        self.images = ['Client_Modules/Volleyball_Assets/rus.png', 'Client_Modules/Volleyball_Assets/pol.png',
                       'Client_Modules/Volleyball_Assets/ball.png']
        self.net = network
        self.player_nmbr = player_nmbr
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.clock = pygame.time.Clock()

        self.ground = Ground((self.width, 100), self.width, self.height)
        self.stick = Stick((20, self.height // 2 + 30), self.width // 2, self.height - 100)

        self.players = [Player((self.width // 4, self.height // 2), self.images[0]),
                        Player((3 * self.width // 4, self.height // 2), self.images[1])]
        self.ball = Ball((self.width // 2, self.height - 100), self.images[2])
        self.points = [0, 0]

        self.player = self.players[self.player_nmbr]
        self.enemy = self.players[(self.player_nmbr + 1) % 2]

        self.items = pygame.sprite.Group()
        self.items.add(self.ball)
        self.items.add(self.player)
        self.items.add(self.enemy)
        self.items.add(self.ground)
        self.items.add(self.stick)

        self.space = pymunk.space.Space()

        if self.player_nmbr == 0:
            self.space.gravity = 0, -1000

            self.space.add(self.ball.body, self.ball.shape)
            self.space.add(self.player.body, self.player.shape)
            self.space.add(self.enemy.body, self.enemy.shape)
            self.space.add(self.ground.body, self.ground.shape)
            self.space.add(self.stick.body, self.stick.shape)

            # bounds
            self.bl_body = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.bl_shape = pymunk.Segment(self.bl_body, (0, 0), (0, 10000), 0)
            self.bl_shape.elasticity = 1

            self.br_body = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.br_shape = pymunk.Segment(self.br_body, (self.width, 0), (self.width, 1000), 0)
            self.br_shape.elasticity = 1

            self.space.add(self.bl_body, self.bl_shape)
            self.space.add(self.br_body, self.br_shape)

        self.FPS = 50

    def reload(self):
        self.players[0].rect.center = (self.width / 4, self.height / 2)
        self.players[0].speed = [0, 0]

        self.players[1].rect.center = (3 * self.width / 4, self.height / 2)
        self.players[1].speed = [0, 0]

        self.space.remove(self.ball.body, self.ball.shape)
        self.items.remove(self.ball)
        self.ball = Ball((self.width // 2, self.height - 100), self.images[2])
        self.space.add(self.ball.body, self.ball.shape)
        self.items.add(self.ball)

        self.ball.body.position = convert_coordinates(self.ball.rect.center)
        self.player.body.position = convert_coordinates(self.player.rect.center)
        self.enemy.body.position = convert_coordinates(self.enemy.rect.center)

    def move_character(self, character, moving_up, moving_left, moving_right):
        if moving_up:
            character.body.apply_force_at_local_point((0, 3500000000), (0, 0))
        if moving_left:
            character.body.apply_force_at_local_point((-20000000, 0), (0, 0))
            # character.body.velocity = (-200, character.body.velocity[1])
        if moving_right:
            character.body.apply_force_at_local_point((20000000, 0), (0, 0))
            # character.body.velocity = (200, character.body.velocity[1])
        if not moving_left and not moving_right:
            character.body.velocity = (0.9 * character.body.velocity[0], character.body.velocity[1])
            # print(character.body.velocity)

    def check_points(self):
        if self.ball.rect.bottom >= self.height - 100:
            if self.ball.rect.centerx < self.width // 2:
                self.points[1] += 1
            else:
                self.points[0] += 1
            self.reload()
            if self.points[0] == 3:
                self.net.game_won_by(0)
            if self.points[1] == 3:
                self.net.game_won_by(1)

    def run(self):
        moving_left = False
        moving_right = False

        while self.net.current_minigame() == 7:
            moving_up = False
            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.height - self.player.rect.bottom <= 100:
                            moving_up = True
                    if event.key == pygame.K_LEFT:
                        moving_left = True
                        # self.player.body.velocity = (10, 0)
                    if event.key == pygame.K_RIGHT:
                        moving_right = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        moving_left = False
                    if event.key == pygame.K_RIGHT:
                        moving_right = False

            if self.player_nmbr == 0:
                data = self.net.get_data()
                if data[0]!=7:
                    break
                self.move_character(self.enemy, data[1][0], data[1][1], data[1][2])
                self.move_character(self.player, moving_up, moving_left, moving_right)

                self.player.rect.center = convert_coordinates(self.player.body.position)
                self.enemy.rect.center = convert_coordinates(self.enemy.body.position)
                self.ball.rect.center = convert_coordinates(self.ball.body.position)

                self.net.send((7, (self.player.rect.center, self.enemy.rect.center, self.ball.rect.center)))

                self.check_points()

            else:
                data = self.net.get_data()
                if data[0]!=7 or data[1] is None:
                    break
                self.player.rect.center = data[1][1]
                self.enemy.rect.center = data[1][0]
                self.ball.rect.center = data[1][2]

                self.net.send((7, (moving_up, moving_left, moving_right)))

            self.items.draw(self.screen)

            pygame.display.update()
            self.space.step(1 / self.FPS)
            self.clock.tick(self.FPS)
        return True
