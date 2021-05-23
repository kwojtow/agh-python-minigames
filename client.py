import pygame
import sys
import pickle
from Client_Modules.networking import Network
from Client_Modules.pong import Pong
from Client_Modules.battleships import Battleships
from Client_Modules.papersoccer import PaperSoccer
from Client_Modules.flappybird import FlappyBird
from Client_Modules.race import Race
from Client_Modules.snakes import Snakes
from Client_Modules.bomberman import Bomberman
from Client_Modules.volleyball import Volleyball


def main():
    pygame.init()
    pygame.font.init()
    restart = True
    while restart:
        restart = False
        net = Network()
        player_nmbr = int(net.get_player_nmbr())
        print("You are player number: ", player_nmbr)#For debug
        screen = pygame.display.set_mode((1280,960))
        pygame.display.set_caption('Minigames PVP')
        clock = pygame.time.Clock()
    
        screen.fill((100,100,100))
        font = pygame.font.Font(pygame.font.get_default_font(), 60)
        text = font.render('Waiting for second player',True, pygame.Color('green'))
        screen.blit(text,(260,480))
    
        pygame.display.flip()
        score=net.score()
        games = [Pong,Battleships,PaperSoccer,FlappyBird,Snakes,Bomberman,Volleyball,Race]
        run=True

        current_minigame=net.current_minigame()
        pygame.display.set_caption('Minigames PVP Score '+str(score[player_nmbr])+'-'+str(score[(player_nmbr+1)%2]))
        while current_minigame==-1 and run:#LOBBY
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run=False
            current_minigame=net.current_minigame()
            clock.tick(30)

        while run and score[0]<3 and score[1]<3:#Minigames
            current_minigame=net.current_minigame()
            game=games[current_minigame-1](player_nmbr,net)
            run=game.run()
            score=net.score()
            pygame.display.set_caption('Minigames PVP Score '+str(score[player_nmbr])+'-'+str(score[(player_nmbr+1)%2]))

        #Game End
        screen = pygame.display.set_mode((1280,960))
        if net.score()[player_nmbr]>=3:
            screen.fill((0,255,0))
        else:
            screen.fill((255,0,0))

        text = font.render('Press R to start new game',True, pygame.Color('black'))
        screen.blit(text,(260,480))

        pygame.display.flip()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run=False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restart = True
                        run = False
            clock.tick(30)
        net.close()
        if not restart:
            pygame.quit()

if __name__ == "__main__":
    main()