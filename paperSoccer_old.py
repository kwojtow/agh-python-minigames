import pygame, sys, random
from networking import Network
import pickle


pygame.display.set_caption('PaperSoccer')

screen = pygame.display.set_mode((600, 1000))

running = True

height = 8
width = 6

moves = [[[False for i in range(10)] for j in range(width + 1)] for k in range(height + 3)]

for i in range(height + 3):
    for j in range(width + 1):
        moves[i][j][5] = True
        moves[i][j][0] = True
#
for i in range(width + 1):
    moves[0][i][7] = True
    moves[0][i][8] = True
    moves[0][i][9] = True
    moves[0][i][4] = True
    moves[0][i][6] = True

    moves[height + 2][i][1] = True
    moves[height + 2][i][2] = True
    moves[height + 2][i][3] = True
    moves[height + 2][i][4] = True
    moves[height + 2][i][6] = True

    moves[1][i][4] = True
    moves[1][i][7] = True
    moves[1][i][8] = True
    moves[1][i][9] = True
    moves[1][i][6] = True

    moves[height + 1][i][4] = True
    moves[height + 1][i][1] = True
    moves[height + 1][i][2] = True
    moves[height + 1][i][3] = True
    moves[height + 1][i][6] = True

for i in range(height + 3):
    moves[i][0][7] = True
    moves[i][0][4] = True
    moves[i][0][1] = True
    moves[i][0][8] = True
    moves[i][0][2] = True
    moves[i][width][9] = True
    moves[i][width][6] = True
    moves[i][width][3] = True
    moves[i][width][8] = True
    moves[i][width][2] = True

moves[1][int(width / 2 - 1)][9] = False
moves[1][int(width / 2 - 1)][6] = False
moves[1][int(width / 2)][4] = False
moves[1][int(width / 2)][7] = False
moves[1][int(width / 2)][8] = False
moves[1][int(width / 2)][9] = False
moves[1][int(width / 2)][6] = False
moves[1][int(width / 2 + 1)][4] = False
moves[1][int(width / 2 + 1)][7] = False

ball_position = (int(100 * width / 2), int(100 * (height + 2) / 2))

screen.fill((255, 255, 255))

player_number = 0
color = pygame.Color(255, 0, 0)


def direction(x):
    return {
        1: (-100, 100),
        2: (0, 100),
        3: (100, 100),
        4: (-100, 0),
        6: (100, 0),
        7: (-100, -100),
        8: (0, -100),
        9: (100, -100),
    }[x]


def move_if_possible(dir, ball_pos):
    global player_number, color
    offset = direction(dir)
    if not moves[int(ball_pos[1] / 100)][int(ball_pos[0] / 100)][dir]:
        old_position = ball_pos
        ball_pos = (ball_pos[0] + offset[0], ball_pos[1] + offset[1])
        pygame.draw.line(screen, color, old_position, ball_pos, 3)
        moves[int(old_position[1] / 100)][int(old_position[0] / 100)][dir] = True
        moves[int(ball_pos[1] / 100)][int(ball_pos[0] / 100)][10 - dir] = True
        if not can_still_move(ball_pos):
            player_number = (player_number + 1) % 2
            color = pygame.Color(255 * ((player_number + 1) % 2), 0, 255 * player_number)
    return ball_pos


def can_still_move(ball_pos):
    all_occupied = True
    no_occupied = 0
    for k in moves[int(ball_pos[1] / 100)][int(ball_pos[0] / 100)]:
        all_occupied = all_occupied and k
        if k:
            no_occupied += 1
    return no_occupied > 3 and not all_occupied


for i in range(1, width):
    pygame.draw.line(screen, pygame.Color(222, 222, 222), (100 * i, 0), (100 * i, 100 * (height + 2)))

for i in range(1, height + 2):
    pygame.draw.line(screen, pygame.Color(222, 222, 222), (0, 100 * i), (100 * width, 100 * i))

left_edge = int(100 * (width / 2 - 1))
right_edge = int(100 * (width / 2 + 1))
half_width = int(100 * (width / 2 - 1))

pygame.draw.rect(screen, pygame.Color(255, 1, 255), (0, 0, half_width, 100))
pygame.draw.rect(screen, pygame.Color(255, 1, 255), (right_edge, 0, half_width, 100))
pygame.draw.rect(screen, pygame.Color(255, 1, 255), (0, 100 * (height + 1), half_width, 100))
pygame.draw.rect(screen, pygame.Color(255, 1, 255), (int(100 * (width / 2 + 1)), 100 * (height + 1), half_width, 100))
pygame.draw.polygon(screen, pygame.Color(0, 0, 0),
                    [(left_edge, 0), (right_edge, 0), (right_edge, 100), (100 * width, 100), (100 * width, 100 * (height + 1)),
                     (right_edge, 100 * (height + 1)), (right_edge, 100 * (height + 2)),
                     (left_edge, 100 * (height + 2)), (left_edge, 100 * (height + 1)), (0, 100 * (height + 1)), (0, 100), (left_edge, 100)
                     ], 3)



while running:#self.net.current_minigame()==1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP1:
                ball_position = move_if_possible(1, ball_position)
                print(ball_position)
            if event.key == pygame.K_KP2:
                ball_position = move_if_possible(2, ball_position)
                print(ball_position)
            if event.key == pygame.K_KP3:
                ball_position = move_if_possible(3, ball_position)
                print(ball_position)
            if event.key == pygame.K_KP4:
                ball_position = move_if_possible(4, ball_position)
                print(ball_position)
            if event.key == pygame.K_KP6:
                ball_position = move_if_possible(6, ball_position)
                print(ball_position)
            if event.key == pygame.K_KP7:
                ball_position = move_if_possible(7, ball_position)
                print(ball_position)
            if event.key == pygame.K_KP8:
                ball_position = move_if_possible(8, ball_position)
                print(ball_position)
            if event.key == pygame.K_KP9:
                ball_position = move_if_possible(9, ball_position)
                print(ball_position)

    pygame.draw.circle(screen, color, ball_position, 5)

    pygame.display.update()
    pygame.time.Clock().tick(100)
