from enum import Enum

import pygame
import random


class Direction(Enum):
    STRAIGHT = 0
    LEFT = 1
    RIGHT = 2


class Car(pygame.sprite.Sprite):
    car_width = 50
    car_height = 100
    max_speed = 10
    rolling_resistance = 0.99
    trace = 0
    score = 0
    collisions = 0

    def __init__(self, initial_position, image_path, initial_speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path), (self.car_width, self.car_height))
        self.speed = initial_speed
        self.initial_speed = initial_speed
        self.initial_position_y = initial_position[1]
        self.rect = self.image.get_rect()
        self.rect.center = initial_position
        self.mask = pygame.mask.from_surface(self.image)
        self.real_position = self.rect.center

    def accelerate(self, acceleration):
        if abs(self.speed[1] + acceleration) < self.max_speed:
            self.speed = (self.speed[0], self.speed[1] + acceleration)

    def change_direction(self, direction):
        if direction == Direction.STRAIGHT:
            self.speed = (0, self.speed[1])
        if direction == Direction.LEFT:
            self.speed = (-abs(self.speed[1]), self.speed[1])
        if direction == Direction.RIGHT:
            self.speed = (abs(self.speed[1]), self.speed[1])

    def move(self, limits):
        self.real_position = (self.real_position[0] + self.speed[0], self.real_position[1] + self.speed[1])
        if self.real_position[0] < limits[0]:
            self.real_position = (limits[0], self.real_position[1])
        if self.real_position[0] + self.car_width > limits[1]:
            self.real_position = (limits[1] - self.car_width, self.real_position[1])

    def add_resistance(self):
        self.speed = (self.speed[0], self.speed[1] * self.rolling_resistance)


class Race:
    screen_width = 420
    screen_height = 1000
    images = ['Client_Modules/Race_Assets/green_car.png', 'Client_Modules/Race_Assets/red_car.png',
              'Client_Modules/Race_Assets/grey_car.png']
    background = pygame.transform.scale(pygame.image.load('Client_Modules/Race_Assets/background.png'), (420, 325))
    background_pos = [-325, 0, 325, 650, 975, 1300]
    race_length = 5000
    obstacles_number = 20

    def __init__(self, player_nmbr, network):
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.player_nmbr = player_nmbr
        self.enemy_nmbr = (self.player_nmbr + 1) % 2
        self.net = network
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.player = Car(((1 + self.player_nmbr) * int(self.screen_width / 3), self.screen_height - 300),
                          self.images[self.player_nmbr], (0, 0))
        self.enemy = Car(((1 + self.enemy_nmbr) * int(self.screen_width / 3), self.screen_height - 300),
                         self.images[self.enemy_nmbr], (0, 0))

        self.position_bounds = (
            int(self.player.car_width / 2) + 65, int(self.screen_width - self.player.car_width / 2) - 65)

        self.obstacles_data = []
        self.obstacles = []

        if self.player_nmbr == 0:
            for i in range(self.obstacles_number):
                self.obstacles_data.append(((random.randint(self.position_bounds[0], self.position_bounds[1]),
                                             -random.randint(0, self.race_length)),
                                            (0, -random.randint(1, 5))))
        self.exchange_data()

        for obstacle_data in self.obstacles_data:
            self.obstacles.append(Car(obstacle_data[0], self.images[2], obstacle_data[1]))

        self.cars = pygame.sprite.Group()
        self.cars.add(self.player)
        self.cars.add(self.enemy)
        self.cars.add(self.obstacles)

    def check_collision_with_enemy(self):
        if pygame.sprite.collide_mask(self.player, self.enemy):
            if abs(self.player.speed[1]) > abs(self.enemy.speed[1]):
                self.player.speed = (0, self.enemy.speed[1])
            if abs(self.player.real_position[0] > self.enemy.real_position[0]) and self.enemy.real_position[
                0] + 1.5 * self.player.car_width < self.screen_width - 65:
                self.player.real_position = (self.player.real_position[0] + 1, self.player.real_position[1])
            elif self.enemy.real_position[0] - 1.5 * self.player.car_width > 65:
                self.player.real_position = (self.player.real_position[0] - 1, self.player.real_position[1])
            if abs(self.player.real_position[1] > self.enemy.real_position[1]):
                self.player.real_position = (self.player.real_position[0], self.player.real_position[1] + 1)
            else:
                self.player.real_position = (self.player.real_position[0], self.player.real_position[1] - 1)

    def update_background_position(self, offset):
        for i in range(len(self.background_pos)):
            self.background_pos[i] = (self.background_pos[i] + offset) % 1625 - 325

    def check_collision_with_obstacles(self, in_touch):
        in_touch_before = in_touch
        in_touch = False
        for ob in self.obstacles:
            if pygame.sprite.collide_mask(self.player, ob):
                if abs(self.player.speed[1]) > abs(ob.speed[1]):
                    self.player.speed = (0, ob.speed[1])
                    in_touch = True
                    if abs(self.player.real_position[0] > ob.real_position[0]):
                        if ob.real_position[0] + 1.5 * self.player.car_width < self.screen_width - 65:
                            self.player.real_position = (self.player.real_position[0] + 1, self.player.real_position[1])
                        else:
                            self.player.real_position = (self.player.real_position[0] - 1, self.player.real_position[1])
                    else:
                        if ob.real_position[0] - 1.5 * self.player.car_width > 65:
                            self.player.real_position = (self.player.real_position[0] - 1, self.player.real_position[1])
                        else:
                            self.player.real_position = (self.player.real_position[0] + 1, self.player.real_position[1])
                    if abs(self.player.real_position[1] > ob.real_position[1]):
                        self.player.real_position = (self.player.real_position[0], self.player.real_position[1] + 1)
                    else:
                        self.player.real_position = (self.player.real_position[0], self.player.real_position[1] - 1)

        if not in_touch_before and in_touch:
            self.player.collisions += 1

    def check_obstacles_collision(self):
        for ob1 in self.obstacles:
            for ob2 in self.obstacles:
                if pygame.sprite.collide_mask(ob1, ob2):
                    if ob1.rect.x < ob2.rect.x:
                        if ob1.rect.left > 65:
                            ob1.real_position = (ob1.real_position[0] - 1, ob1.real_position[1])
                        if ob2.rect.right < self.screen_width - 65:
                            ob2.real_position = (ob2.real_position[0] + 1, ob2.real_position[1])
                    else:
                        if ob1.rect.right < self.screen_width - 65:
                            ob1.real_position = (ob1.real_position[0] + 1, ob1.real_position[1])
                        if ob2.rect.left > 65:
                            ob2.real_position = (ob2.real_position[0] - 1, ob2.real_position[1])

    def move_cars(self):
        limits = (65, self.screen_width - 65)
        self.player.move(limits)
        self.enemy.move(limits)
        for obstacle in self.obstacles:
            obstacle.move(limits)

    def prepare_to_draw(self):
        offset = -self.player.real_position[1] + self.player.initial_position_y
        self.player.rect.x = self.player.real_position[0]
        self.player.rect.y = self.player.real_position[1] + offset
        self.enemy.rect.x = self.enemy.real_position[0]
        self.enemy.rect.y = self.enemy.real_position[1] + offset
        for obstacle in self.obstacles:
            obstacle.rect.x = obstacle.real_position[0]
            obstacle.rect.y = obstacle.real_position[1] + offset

    def update_scores(self):
        self.player.score = abs(
            self.player.real_position[1] - self.player.initial_position_y) - 100 * self.player.collisions

    def check_if_win(self):
        if self.player.score >= 10000:
            self.net.game_won_by(0)
        if self.enemy.score >= 10000:
            self.net.game_won_by(1)

    def exchange_data(self):
        self.net.send((8, (self.player.real_position, self.player.score), self.obstacles_data))
        if self.player_nmbr == 0:
            for i in range(len(self.obstacles)):
                self.obstacles_data[i] = (self.obstacles[i].real_position, self.obstacles[i].speed)

        data = self.net.get_data()
        self.enemy.real_position = data[1][0]
        self.enemy.score = data[1][1]

        if self.player_nmbr == 1:
            self.obstacles_data = data[2]

    def run(self):
        up_acceleration = False
        down_acceleration = False
        in_touch = False
        while self.net.current_minigame() == 8:
            for p in self.background_pos:
                self.screen.blit(self.background, (0, p))
            textsurface = self.font.render("Score: " + str(int(self.player.score)), False, (255, 0, 0))

            self.exchange_data()

            for i in range(len(self.obstacles_data)):
                self.obstacles[i].real_position = self.obstacles_data[i][0]
                self.obstacles[i].speed = self.obstacles_data[i][1]

            self.screen.blit(textsurface, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        up_acceleration = True
                    if event.key == pygame.K_DOWN:
                        down_acceleration = True
                    if event.key == pygame.K_RIGHT:
                        self.player.change_direction(Direction.RIGHT)
                    if event.key == pygame.K_LEFT:
                        self.player.change_direction(Direction.LEFT)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        up_acceleration = False
                    if event.key == pygame.K_DOWN:
                        down_acceleration = False
                    if event.key == pygame.K_RIGHT:
                        self.player.change_direction(Direction.STRAIGHT)
                    if event.key == pygame.K_LEFT:
                        self.player.change_direction(Direction.STRAIGHT)

            if up_acceleration:
                self.player.accelerate(-0.1)
            if down_acceleration:
                self.player.accelerate(0.1)

            self.player.add_resistance()

            self.check_collision_with_enemy()
            self.check_collision_with_obstacles(in_touch)

            self.move_cars()

            offset = - self.player.speed[1]
            self.update_background_position(offset)
            self.check_obstacles_collision()

            self.prepare_to_draw()
            self.cars.draw(self.screen)
            pygame.display.update()

            self.update_scores()
            if self.player_nmbr == 0:
                self.check_if_win()

            self.clock.tick(30)
        return True
