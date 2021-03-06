import pygame
import sys

screen_width = 1000
screen_height = 1000
block_size = 50
minigameID = 5

class Player:

	def __init__(self,player_nmbr,network):
		self.net = network
		self.body = []
		self.moved = True
		self.apple = (-50, -50)
		self.player_nmbr = player_nmbr
		if(player_nmbr == 0):
			self.direction = pygame.K_RIGHT
			self.body.append((0, 0))
			self.head = [0, 0]
		else:
			self.direction = pygame.K_LEFT
			self.body.append((screen_width-block_size, screen_height-block_size))
			self.head = [screen_width-block_size, screen_height-block_size]

	def change_direction(self,new_direction):
		#Check if can change from current direction
		if  (self.moved and
			((self.direction in [pygame.K_UP,pygame.K_DOWN] and new_direction in [pygame.K_LEFT,pygame.K_RIGHT]) or
			 (self.direction in [pygame.K_LEFT,pygame.K_RIGHT] and new_direction in [pygame.K_UP,pygame.K_DOWN]))):
			self.direction = new_direction
			self.moved = False

	def move(self):
		self.moved = True
		lost = False
		#If apple was eaten, "add" new block by not deleting oldest
		if not(self.apple[0] == self.head[0] and self.apple[1] == self.head[1]):
			self.body.pop(0)
		else:
			self.net.send("ate")
		#Check for hitting walls
		if(self.direction == pygame.K_UP):
			self.head[1] -= block_size
			if self.head[1] < 0:
				lost = True
		elif (self.direction == pygame.K_DOWN):
			self.head[1] += block_size
			if self.head[1] >= screen_height:
				lost = True
		elif (self.direction == pygame.K_LEFT):
			self.head[0] -= block_size
			if self.head[0] < 0:
				lost = True
		else:
			self.head[0] += block_size
			if self.head[0] >= screen_width:
				lost = True

		if lost:
			self.net.game_won_by((self.player_nmbr + 1) % 2)
			return False
		else:
			self.body.append(tuple(self.head))
			return True

class Snakes:

	def __init__(self,player_nmbr,network):
		self.player_nmbr = player_nmbr
		self.net = network
		self.screen = pygame.display.set_mode((screen_width, screen_height))
		self.player = Player(player_nmbr, network)
		self.enemy_body = []
		if(player_nmbr == 1):
			self.enemy_body.append((0, 0))
			self.enemy_head=[0, 0]
		else:
			self.enemy_body.append((screen_width - block_size, screen_height - block_size))
			self.enemy_head = [screen_width - block_size, screen_height - block_size]

	def draw(self):
		self.screen.fill((110, 110, 110))
		#Draw apple
		pygame.draw.rect(self.screen, (255, 0, 0), [self.player.apple[0], self.player.apple[1], block_size, block_size])
		#Draw player
		for body_part in self.player.body[:-1]:
			pygame.draw.rect(self.screen, (0, 128, 0), [body_part[0], body_part[1], block_size, block_size])
		#Draw enemy
		for body_part in self.enemy_body[:-1]:
			pygame.draw.rect(self.screen, (0, 0, 128), [body_part[0], body_part[1], block_size, block_size])
		#Draw heads in diffrent color
		pygame.draw.rect(self.screen, (0, 255, 0), [self.player.head[0], self.player.head[1], block_size, block_size])
		pygame.draw.rect(self.screen, (0, 0, 255), [self.enemy_head[0], self.enemy_head[1], block_size, block_size])

		pygame.display.flip()

	def run (self):
		while self.net.current_minigame() == minigameID:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return False
				if event.type == pygame.KEYDOWN:
					self.player.change_direction(event.key)

			if not(self.player.move()):
				break

			self.net.send((minigameID, self.player.body, self.player.head))
			data = self.net.get_data()
			if(data[0] != 5):
				break
			else:
				self.enemy_body, self.enemy_head, self.player.apple = data[1][0],data[1][1],data[2]

			#If colided with enemy, lose
			if(tuple(self.player.head) in self.enemy_body+self.player.body[:-1]):
				self.net.game_won_by((self.player_nmbr + 1) % 2)

			self.draw()
			pygame.time.Clock().tick(5)
		return True