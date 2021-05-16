import pygame
import sys
import pickle
from Client_Modules.networking import Network
from Client_Modules.pong import Pong
from Client_Modules.battleships import Battleships
from Client_Modules.papersoccer import PaperSoccer
from Client_Modules.flappybird import FlappyBird
from Client_Modules.snakes import Snakes
from Client_Modules.bomberman import Bomberman


def main():
    net = Network()
    player_nmbr = int(net.get_player_nmbr())
    print("You are player number: ", player_nmbr)#For debug
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1280,960))
    pygame.display.set_caption('Minigames PVP')
    clock = pygame.time.Clock()
    screen.fill((100,100,100))
    pygame.display.flip()
    score=net.score()
    run=True

    current_minigame=net.current_minigame()
    pygame.display.set_caption('Minigames PVP Score '+str(score[player_nmbr])+'-'+str(score[(player_nmbr+1)%2]))
    while current_minigame==-1 and run:#LOBBY
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
        current_minigame=net.current_minigame()
        clock.tick(30)

    while run and score[0]<3 and score[1]<3:
        current_minigame=net.current_minigame()
        if current_minigame==1:#PONG
            game=Pong(player_nmbr,net)
            run=game.run()
        elif current_minigame==2:#BATTLESHIPS
            game=Battleships(player_nmbr,net)
            run=game.run()
        elif current_minigame==3:#PAPERSOCCER
            game=PaperSoccer(player_nmbr,net)
            run=game.run()
        elif current_minigame==4:#FLAPPYBIRD
            game=FlappyBird(player_nmbr,net)
            run=game.run()
        elif current_minigame==5:#SNAKES
            game=Snakes(player_nmbr,net)
            run=game.run()
        elif current_minigame==6:#BOMBERMAN
            game=Bomberman(player_nmbr,net)
            run=game.run()
        score=net.score()
        pygame.display.set_caption('Minigames PVP Score '+str(score[player_nmbr])+'-'+str(score[(player_nmbr+1)%2]))

    if net.score()[player_nmbr]>=3:
        screen.fill((0,255,0))
    else:
        screen.fill((255,0,0))

    pygame.display.flip()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
        clock.tick(30)
    net.close()
    pygame.quit()

if __name__ == "__main__":
    main()