import pygame, sys, random

class Pong:
	players_height = 100
	players_width = 10
	screen_width = 1280
	screen_height = 960
	minigameID = 1
	speed_multiplier = 1

	def __init__(self, player_nmbr,network):
		self.player_nmbr = player_nmbr
		self.net = network
		self.screen = pygame.display.set_mode((1280, 960))
		self.speed = 0
		self.player, self.enemy = self.initialize_players()
		self.ball = pygame.Rect(self.screen_width / 2 , self.screen_height / 2 , 20, 20)
		self.ball_speed_x = 10
		self.ball_speed_y = 0

	#Initialize players (rect) and return in correct order
	def initialize_players(self):
		player0 = pygame.Rect(5, (self.screen_height - self.players_height)/ 2, self.players_width, self.players_height)
		player1 = pygame.Rect(self.screen_width - self.players_width - 5,
							 (self.screen_height - self.players_height) / 2, self.players_width, self.players_height)
		if(self.player_nmbr == 0):
			return player0, player1
		else:
			return player1, player0

	#Get data from server and update location
	def update_enemy(self):
		data = self.net.get_data()
		if(data[0] == self.minigameID):
			data = data[1]
			#Player nmbr 1 gets logic data from server
			if(self.player_nmbr == 0):
				self.enemy.y = data
			else:
				self.enemy.y = data[0]
				self.ball.x = data[1]
				self.ball.y = data[2]

	#Move player and send current data to server
	def update_player(self):
		self.player.y += self.speed
		if (self.player.bottom > self.screen_height):
			self.player.bottom = self.screen_height
		elif (self.player.top <= 0):
			self.player.top = 1
		if(self.player_nmbr == 0):
			self.net.send((self.minigameID, (self.player.y,self.ball.x,self.ball.y)))
		else:
			self.net.send((self.minigameID, self.player.y))

	def update_ball(self):
		self.ball.x += self.ball_speed_x
		self.ball.y += self.ball_speed_y

		if self.ball.colliderect(self.player) or self.ball.colliderect(self.enemy):
			self.ball_speed_x *= -1
			self.speed_multiplier += 0.1
			if self.ball.y <= self.player.y:
				self.ball_speed_y=round(-8 * self.speed_multiplier)
			else :
				self.ball_speed_y=round(8 * self.speed_multiplier)

		elif self.ball.top <= 0:
			self.ball.top = 0
			self.ball_speed_y *= -1
		elif self.ball.bottom >= self.screen_height:
			self.ball.bottom = self.screen_height
			self.ball_speed_y *= -1

		if self.ball.left <= 0:
			self.net.game_won_by(1)
		elif self.ball.right >= self.screen_width:
			self.net.game_won_by(0)
			
	def draw(self):
		self.screen.fill((110, 110, 110))
		pygame.draw.rect(self.screen, (0, 0, 0), self.player)
		pygame.draw.rect(self.screen, (0, 0, 0), self.enemy)
		pygame.draw.ellipse(self.screen, (0, 0, 0), self.ball)
		pygame.display.flip()

	def run(self):
		while self.net.current_minigame() == self.minigameID:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return False
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_UP:
						self.speed = 0
					elif event.key == pygame.K_DOWN:
						self.speed = 0
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						self.speed = round(-8 * self.speed_multiplier)
					elif event.key == pygame.K_DOWN:
						self.speed = round(8 * self.speed_multiplier)
			self.draw()
			self.update_enemy()
			self.update_player()
			if(self.player_nmbr == 0):
				self.update_ball()
			pygame.time.Clock().tick(60)
		return True