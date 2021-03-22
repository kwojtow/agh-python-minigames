from networking import Network
import pickle
from pong import Pong
from battleships import Battleships
import pygame
import sys

def main():
    net = Network()
    player_nmbr = int(net.get_player_nmbr())
    print("You are player number: ", player_nmbr)#For debug
    pygame.init()
    screen = pygame.display.set_mode((1280,960))
    pygame.display.set_caption('Minigames PVP')
    clock = pygame.time.Clock()
    screen.fill((100,100,100))
    pygame.display.flip()
    while 3 not in net.score():#Temporary,in final version should be "while no one won"
        current_minigame=net.current_minigame()
        while current_minigame==-1:#LOBBY
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            current_minigame=net.current_minigame()
            clock.tick(30)
        if current_minigame==1:#PONG
            print("GAME 1")
            game=Pong(player_nmbr,net)
            game.run()
        elif current_minigame==2:#BATTLESHIPS
            game=Battleships(player_nmbr,net)
            game.run()

    if net.score()[player_nmbr]==3:
        screen.fill((0,255,0))
    else:
        screen.fill((255,0,0))
    pygame.display.flip()

if __name__ == "__main__":
    main()