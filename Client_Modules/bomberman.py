import pygame
import sys

screen_width=950
screen_height=950
block_size=50
class Player:
	def __init__(self,player_nmbr,network):
		self.net=network
		self.player_nmbr=player_nmbr
		self.moved=False
		self.free_bombs=2
		self.bombs = []
		if(player_nmbr==0):
			self.position=[50,50]
		else:
			self.position=[screen_width-2*block_size,screen_height-2*block_size]

class Bomb:
	def __init__(self,position):
		self.position=position
		self.timer=60

	def __eq__(self, other):
		return self.position == other #Compare with list

	def explode(self):
		self.timer-=1
		if(self.timer):
			return False
		return True

class Bomberman:
	def __init__(self,player_nmbr,network):
		self.player_nmbr=player_nmbr
		self.net=network
		self.player=Player(player_nmbr,network)
		self.enemy=Player(player_nmbr%2,network)
		self.blocks=[]
		self.timer=0
		self.lost=False
		self.screen = pygame.display.set_mode((screen_width,screen_height))
		for x in range(2*block_size,screen_width-2*block_size,2*block_size):
			for y in range(2*block_size,screen_height-2*block_size,2*block_size):
				self.blocks.append([x,y])
	def explosion(self,position):
		pygame.draw.rect(self.screen, (255,165,000), [position[0],position[1], block_size, block_size])
		destroyed_cells=[]
		for y in range(4):
			if(position[0]+block_size*y<screen_width-50 and [position[0]+block_size*y,position[1]] not in self.blocks):
				pygame.draw.rect(self.screen, (255,165,000), [position[0]+block_size*y, position[1], block_size, block_size])
				destroyed_cells.append([position[0]+block_size*y,position[1]])
			else:
				break

		for y in range(4):
			if(position[0]-block_size*y>0 and [position[0]-block_size*y,position[1]] not in self.blocks):
				pygame.draw.rect(self.screen, (255,165,000), [position[0]-block_size*y, position[1], block_size, block_size])
				destroyed_cells.append([position[0]-block_size*y,position[1]])
			else:
				break

		for x in range(4):
			if(position[1]+block_size*x<screen_width-50 and [position[0],position[1]+block_size*x] not in self.blocks):
				pygame.draw.rect(self.screen, (255,165,000), [position[0], position[1]+block_size*x, block_size, block_size])
				destroyed_cells.append([position[0],position[1]+block_size*x])
			else:
				break

		for x in range(4):
			if(position[1]-block_size*x>0 and [position[0],position[1]-block_size*x] not in self.blocks):
				pygame.draw.rect(self.screen, (255,165,000), [position[0], position[1]-block_size*x, block_size, block_size])
				destroyed_cells.append([position[0],position[1]-block_size*x])
			else:
				break
		if(not self.lost and self.player.position in destroyed_cells):
			self.net.game_won_by((self.player_nmbr+1)%2)
			self.lost = True
			print("YOU LOST")

	def draw(self):
		self.screen.fill((110,110,110))
		for block in self.blocks:
			pygame.draw.rect(self.screen, (101,67,33), [block[0], block[1], block_size, block_size])

		pygame.draw.rect(self.screen, (101,67,33), [0, 0, screen_width, block_size])
		pygame.draw.rect(self.screen, (101,67,33), [0, 0, block_size, screen_height])
		pygame.draw.rect(self.screen, (101,67,33), [screen_width-block_size, 0, block_size, screen_height])
		pygame.draw.rect(self.screen, (101,67,33), [0, screen_height-block_size, screen_width, block_size])

		pygame.draw.rect(self.screen, (0,255,0), [self.player.position[0],self.player.position[1], block_size, block_size])
		pygame.draw.rect(self.screen, (148,0,211), [self.enemy.position[0],self.enemy.position[1], block_size, block_size])

		for bomb in self.player.bombs:
			pygame.draw.rect(self.screen, (255,0,0), [bomb.position[0], bomb.position[1], block_size, block_size])
		for bomb in self.enemy.bombs:
			pygame.draw.rect(self.screen, (255,0,0), [bomb.position[0], bomb.position[1], block_size, block_size])

	def isOutsideOfMap(self):
		return self.player.position[0]<50 or self.player.position[1]<50 or self.player.position[0]>=screen_width-50 or self.player.position[1]>=screen_height-50
	
	def run (self):
		while self.net.current_minigame()==6:
			self.player.moved=False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return False
				elif event.type == pygame.KEYDOWN and not self.player.moved:
					prev_position=self.player.position.copy()
					if event.key == pygame.K_UP:
						self.player.position[1]-=block_size
					elif event.key == pygame.K_DOWN:
						self.player.position[1]+=block_size
					elif event.key == pygame.K_RIGHT:
						self.player.position[0]+=block_size
					elif event.key == pygame.K_LEFT:
						self.player.position[0]-=block_size
					elif self.player.free_bombs and event.key == pygame.K_SPACE and self.player.position not in self.player.bombs:
						self.player.free_bombs-=1
						self.player.bombs.append(Bomb(self.player.position.copy()))
					else:
						continue

					if(self.isOutsideOfMap() or self.player.position in self.blocks or self.player.position in self.player.bombs or self.player.position in self.enemy.bombs or self.player.position==self.enemy.position):
						self.player.position=prev_position
					else:
						self.player.moved=True

			self.net.send((6,self.player.position,self.player.bombs))
			data=self.net.get_data()
			if data!=None and data[0]==6:#Find out why Nonetype is returned
				data=data[1]
				self.enemy.position=data[0]
				for bomb in data[1]:
					if bomb not in self.enemy.bombs:
						self.enemy.bombs.append(bomb)
			self.draw()
			for bomb in list(self.player.bombs):
				if bomb.explode():
					self.explosion(bomb.position)
					self.player.bombs.remove(bomb)
					self.player.free_bombs+=1
			for bomb in list(self.enemy.bombs):
				if bomb.explode():
					self.explosion(bomb.position)
					self.enemy.bombs.remove(bomb)


			self.timer+=1
			if(self.timer%90==0):
				self.player.free_bombs+=1
				self.timer=0

			pygame.display.flip()
			pygame.time.Clock().tick(15)
		return True
