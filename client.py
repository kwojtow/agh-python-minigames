from networking import Network
import pickle
from pong import Pong
from pong2 import Pong2
import pygame


def main():
    n = Network()
    player = int(n.get_player_nmbr())
    print("You are player number: ", player)#For debug
    pygame.init()
    screen = pygame.display.set_mode((1280,960))
    pygame.display.set_caption('Minigames PVP')
    clock = pygame.time.Clock()
    while True:#Temporary,in final version should be "while no one won"
        current_minigame=n.send("minigame")
        while current_minigame==-1:#LOBBY
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            current_minigame=n.send("minigame")
            clock.tick(30)
        if current_minigame==1:#PONG
            print("GAME 1")
            game=Pong(player,n)
            game.run()
        elif current_minigame==2:#PONG 2 FOR TESTS
            print("GAME 2")
            game2=Pong2(player,n)
            game2.run()


if __name__ == "__main__":
    main()