from networking import Network
import pickle
from pong import Pong
import pygame


def main():
    n = Network()
    player = int(n.get_player_nmbr())
    print("You are player number: ", player)#For debug
    pygame.init()
    screen = pygame.display.set_mode((1280,960))
    pygame.display.set_caption('Minigames PVP')
    clock = pygame.time.Clock()
    clock.tick(60)
    pygame.display.flip()

    current_minigame=n.send("minigame")
    while current_minigame==-1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        current_minigame=n.send("minigame")

    game=Pong(player,n)
    game.run()


if __name__ == "__main__":
    main()