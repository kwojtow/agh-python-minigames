import pygame, sys, random
from networking import Network
import pickle

pygame.init()
pygame.display.set_caption('FlappyBird')

screen = pygame.display.set_mode((600, 800))

running = True

playerImg = pygame.image.load('bird.png')
playerImg = pygame.transform.scale(playerImg, (50, 50))
playerX = 300
playerY = 400

brickImg = pygame.image.load('brickwall.png')
brickImg = pygame.transform.scale(brickImg, (50, 50))
bricksX = [600, 900]
holes = [random.randint(1, 14), random.randint(1, 14)]

downSped = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


def random_bricks_position():
    global holes
    for i in range(len(bricksX)):
        if bricksX[i] < -50:
            holes[i] = random.randint(1, 14)

    for k in range(len(bricksX)):
        for j in range(16):
            if j == holes[k] or j - 1 == holes[k] or j + 1 == holes[k]:
                continue
            screen.blit(brickImg, (bricksX[k], 50 * j))


def crash():
    global bricksX
    global holes
    result = False
    if playerY <= 0 or playerY >= 750:
        result = True
    for i in range(2):
        if playerX + 50 >= bricksX[i] and playerX <= bricksX[i] + 50:
            if playerY <= (holes[i] - 1) * 50 or playerY >= (holes[i] + 1) * 50:
                result = True
    return result


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                downSped = -6

    screen.fill((255, 255, 255))

    playerY += downSped
    for i in range(len(bricksX)):
        bricksX[i] -= 1
        if bricksX[i] < -51:
            bricksX[i] = 600
    downSped += 0.3
    player(playerX, playerY)
    random_bricks_position()
    if crash():
        print("!!!!!!!!!!!!! CRASH !!!!!!!!!!!!!!!")

    pygame.display.update()
    pygame.time.Clock().tick(100)
