import pygame, sys, random
from networking import Network
import pickle

class Pong2:
	def __init__(self, player_nmbr,network):
		self.player_nmbr=player_nmbr
		self.screen_width = 1280
		self.screen_height = 960
		self.ball_speed_x = 7 * random.choice((1,-1))
		self.ball_speed_y = 7 * random.choice((1,-1))
		self.player_speed = 0
		self.n=network
		# Colors
		self.light_grey = (200,200,200)
		# Game Rectangles
		self.ball = pygame.Rect(self.screen_width / 2 - 15, self.screen_height / 2 - 15, 30, 30)
		self.player = pygame.Rect(self.screen_width - 20, self.screen_height / 2 - 70, 10,140)
		self.opponent = pygame.Rect(10, self.screen_height / 2 - 70, 10,140)
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))

	def ball_animation(self):	
		self.ball.x += self.ball_speed_x
		self.ball.y += self.ball_speed_y

		if self.ball.top <= 0 or self.ball.bottom >= self.screen_height:
			self.ball_speed_y *= -1
		if self.ball.left <= 0 or self.ball.right >= self.screen_width:
			self.ball_start()

		if self.ball.colliderect(self.player) or self.ball.colliderect(self.opponent):
			self.ball_speed_x *= -1

	def set_opponent(self,data):
		self.get_opponent().y=data

	def get_player(self):
		if(self.player_nmbr==0):
			return self.player
		else:
			return self.opponent

	def get_opponent(self):
		if(self.player_nmbr==0):
			return self.opponent
		else:
			return self.player

	def player_animation(self):

		self.get_player().y += self.player_speed
		if self.get_player().top <= 0:
			self.get_player().top = 1
			self.n.send("newgame")#FOR TEST PURPOSE
		if self.get_player().bottom >= self.screen_height:
			self.get_player().bottom = self.screen_height
		self.n.send(self.get_player().y)



	def ball_start(self):
		self.ball.center = (self.screen_width/2, self.screen_height/2)
		self.ball_speed_y *= random.choice((1,-1))
		self.ball_speed_x *= random.choice((1,-1))

	def run(self):

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						self.player_speed -= 6
					if event.key == pygame.K_DOWN:
						self.player_speed += 6
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_UP:
						self.player_speed = 0
					if event.key == pygame.K_DOWN:
						self.player_speed = 0
	
			#Game Logic
			self.ball_animation()
			self.player_animation()
			self.set_opponent(self.n.send("get"))
			# Visuals 
			self.screen.fill((100,100,100))
			pygame.draw.rect(self.screen, self.light_grey, self.player)
			pygame.draw.rect(self.screen, self.light_grey, self.opponent)
			pygame.draw.ellipse(self.screen, self.light_grey, self.ball)
			pygame.draw.aaline(self.screen, self.light_grey, (self.screen_width / 2, 0),(self.screen_width / 2, self.screen_height))
			pygame.display.flip()
			if(self.n.send("minigame")!=2):
				break
			self.clock.tick(60)
