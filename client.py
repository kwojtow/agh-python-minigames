import pygame
import sys
import pickle
import argparse
from Client_Modules.networking import Network
from Client_Modules.pong import Pong
from Client_Modules.battleships import Battleships
from Client_Modules.papersoccer import PaperSoccer
from Client_Modules.flappybird import FlappyBird
from Client_Modules.race import Race
from Client_Modules.snakes import Snakes
from Client_Modules.bomberman import Bomberman
from Client_Modules.volleyball import Volleyball
from socket import error as SockError
from socket import timeout as SockTimeout

def main():

    pygame.init()
    pygame.font.init()
    restart = True
    net = Network()
    games = [Pong,Battleships, PaperSoccer, FlappyBird, Snakes, Bomberman, Volleyball, Race]
    game_names = ["Pong", "Battleships", "PaperSoccer", "FlappyBird", "Snakes", "Bomberman", "Volleyball", "Race"]
    screen = pygame.display.set_mode((1280, 960))
    clock = pygame.time.Clock()
    font = pygame.font.Font(pygame.font.get_default_font(), 60)

    while restart:
        restart = False
        run=True

        net.connect();
        player_nmbr = int(net.get_player_nmbr())
        print("You are player number: ", player_nmbr)#For debug
        score = (0,0)
        current_minigame=-1

        if not player_nmbr:
            pygame.display.set_caption('Minigames PVP')
            screen.fill((100, 100, 100))
            text = font.render('Waiting for second player',True, pygame.Color('green'))
            screen.blit(text,(260, 480))
            pygame.display.flip()

            while current_minigame == -1 and run:#LOBBY
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                current_minigame = net.current_minigame()
                clock.tick(30)


        pygame.display.set_caption('Minigames PVP Score '+str(score[player_nmbr])+'-'+str(score[(player_nmbr + 1) % 2]))

        while run and all(points < 3 for points in score):#Minigames
            current_minigame=net.current_minigame()

            screen = pygame.display.set_mode((1280, 960))

            screen.fill((255, 255, 255))
            text = font.render('Next game is ' + game_names[current_minigame-1],True, pygame.Color('black'))
            screen.blit(text,(280, 480))
            pygame.display.flip()

            current_time = pygame.time.get_ticks()
            while run and current_time + 3000 > pygame.time.get_ticks():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False


            game = games[current_minigame - 1](player_nmbr,net)
            try:
                run = game.run()
                score = net.score()
            except SockTimeout:
                print("TIMED OUT !!!")
                run = False
            except SockError as e:
                #Second player left
                print("Enemy Left")
                run = False
                net.close()
            except Exception as e:
                #Some other error
                print(e)
                run = False

            pygame.display.set_caption('Minigames PVP Score '+str(score[player_nmbr])+'-'+str(score[(player_nmbr + 1) % 2]))

        #Game End
        screen = pygame.display.set_mode((1280, 960))
        if net.connected:
            if net.score()[player_nmbr]>=3:
                screen.fill((0, 255, 0))
            else:
                screen.fill((255, 0, 0))

            text = font.render('Press R to start new game',True, pygame.Color('black'))
            screen.blit(text,(260, 480))
        else:
            screen.fill((0, 255, 0))
            text = font.render('Enemy left the game',True, pygame.Color('black'))
            screen.blit(text,(260, 480))
            text = font.render('Press R to start new game',True, pygame.Color('black'))
            screen.blit(text,(260, 540))
            run = True

        pygame.display.flip()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restart = True
                        run = False
            clock.tick(30)
        if net.connected:#We shut connection here and not above to make sure second player gets data before deleting game from server
            net.close()
        if not restart:
            pygame.quit()

if __name__ == "__main__":
    main()