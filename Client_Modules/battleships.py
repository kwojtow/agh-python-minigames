import pygame,sys
from enum import Enum

class CellType(Enum):
    WATER = (0,0,255)
    SHIP = (0,255,0)
    MISS = (100,100,100)
    DESTROYED = (255,0,0)
class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

class Board:
    def __init__(self):
        #[CELLTYPE,(x,y),SHIP,ORIENTATION]
        self.board_cells=[ [[CellType.WATER,None,None,None] for p in range(10)] for _ in range(10)]
        self.free_ships=[1,2,3,4,5,6]
        self.orientation=Orientation.HORIZONTAL

    def change_orientation(self):
        if self.orientation == Orientation.HORIZONTAL:
            self.orientation = Orientation.VERTICAL
        else:
            self.orientation = Orientation.HORIZONTAL

    def can_place(self,x,y,size,orientation):
        if(orientation==Orientation.VERTICAL and y+size<=10):
            for i in range(y,y+size):
                if(self.board_cells[x][i][0]!=CellType.WATER):
                    return False
        elif(orientation==Orientation.HORIZONTAL and x+size<=10):
            for i in range(x,x+size):
                if(self.board_cells[i][y][0]!=CellType.WATER):
                    return False
        else:
            return False

        return True
    def place(self,x,y):
        if(len(self.free_ships)):
            ship=self.free_ships.pop()
            if(self.can_place(x,y,ship,self.orientation)):
                if(self.orientation==Orientation.HORIZONTAL):
                    for i in range(x,x+ship):
                        self.board_cells[i][y]=[CellType.SHIP,(x,y),ship,self.orientation]
                else:
                    for i in range(y,y+ship):
                        self.board_cells[x][i]=[CellType.SHIP,(x,y),ship,self.orientation]
            else:
                self.free_ships.append(ship)
    def remove(self,x,y):
        ship,orientation=self.board_cells[x][y][2:]
        x,y = self.board_cells[x][y][1]
        if(orientation==Orientation.HORIZONTAL):
            for i in range(x,x+ship):
                self.board_cells[i][y]=[CellType.WATER,None,None,None]
        else:
            for i in range(y,y+ship):
                self.board_cells[x][i]=[CellType.WATER,None,None,None]
        self.free_ships.append(ship)
    def clicked_tile(self,x,y):
        if(self.board_cells[x][y][0]==CellType.SHIP):
            self.remove(x,y)
        else:
            self.place(x,y)
    def shoot_player_cell(self,x,y):
        if self.board_cells[x][y][0]==CellType.WATER:
            self.board_cells[x][y][0]=CellType.MISS
        else:
            self.board_cells[x][y][0]=CellType.DESTROYED

    def shoot_enemy_cell(self,x,y,hit):
        if hit:
            self.board_cells[x][y][0]=CellType.DESTROYED
        else:
            self.board_cells[x][y][0]=CellType.MISS
class Display:
    def __init__(self,player_board,enemy_board):
        self.divider=35
        self.screen_width=361
        self.cell_size=35
        self.margin = 1
        self.screen_height=20*self.cell_size+20*self.margin+self.divider
        self.player_board=player_board
        self.enemy_board=enemy_board
        self.font = pygame.font.SysFont("Helvetica", 15)
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
        self.text="Press SPACEBAR to change ship direction"
    def show(self):
        self.screen.fill((36,36,36))
        self.show_text()
        for y in range(10):
            for x in range(10):
                pygame.draw.rect(self.screen,self.enemy_board.board_cells[x][y][0].value,
                                     [x * self.cell_size+(x+1)*self.margin,
                                      y * self.cell_size+(y+1)*self.margin,
                                      self.cell_size, self.cell_size])

                pygame.draw.rect(self.screen,self.player_board.board_cells[x][y][0].value,
                                     [x * self.cell_size+(x+1)*self.margin,
                                      y * self.cell_size+(10*self.cell_size)+(y+11)*self.margin+self.divider,
                                      self.cell_size, self.cell_size])
        pygame.display.flip()

    def show_text(self):
        x = self.margin
        y = 10*(self.cell_size + self.margin)
        label = self.font.render(self.text, True, (255,0,0))
        self.screen.blit(label, (x, y))


class Battleships:
    def __init__(self,player_nmbr,network):
        self.player_board=Board()
        self.enemy_board=Board()
        self.display=Display(self.player_board,self.enemy_board)
        self.player_board_ready=False
        self.player_move=False
        self.player_nmbr=player_nmbr
        self.net=network
        self.player_score=0

    def board_data_send(self):
        data=[[False for p in range(10)] for _ in range(10)]
        for i in range(10):
            for j in range(10):
                if self.player_board.board_cells[i][j][0]==CellType.SHIP:
                    data[i][j]=True
        self.net.send((2,"matrix",data))

    def update_text(self):
        if len(self.player_board.free_ships)>0:
            self.display.text=str(self.player_board.free_ships[len(self.player_board.free_ships)-1])
            if self.player_board.orientation==Orientation.HORIZONTAL:
                self.display.text+=" HORIZONTAL"
            else:
                self.display.text+=" VERTICAL"
        elif self.player_board_ready and not self.player_move:
            self.display.text="Waiting for second player"
        elif not self.player_board_ready:
            self.display.text="No more ships, press R if youre ready"
        else:
            self.display.text="Your move"

    def run(self):
        while self.net.current_minigame()==2:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    if(y>self.display.screen_height/2):
                        y-=10*(self.display.cell_size + self.display.margin)+self.display.divider
                        x = x // (self.display.cell_size+self.display.margin)
                        y = y// (self.display.cell_size+self.display.margin)
                        if x in range(10) and y in range(10) and not self.player_board_ready:
                            self.player_board.clicked_tile(x,y)
                            self.update_text()
                    else:
                        x = x // (self.display.cell_size+self.display.margin)
                        y = y// (self.display.cell_size+self.display.margin)
                        if x in range(10) and y in range(10):
                            if self.player_move and self.enemy_board.board_cells[x][y][0]==CellType.WATER:
                                self.player_move=False
                                self.update_text()
                                data=self.net.send_recv((2,"shot",(x,y)))
                                if data[0]:
                                    data=data[1]
                                    self.player_score+=data
                                    self.enemy_board.shoot_enemy_cell(x,y,data)
                                    if self.player_score==21:
                                        self.net.game_won_by(self.player_nmbr)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player_board.change_orientation()
                        self.update_text()
                    if event.key == pygame.K_r and len(self.player_board.free_ships)==0 and self.player_board_ready==False:
                        self.board_data_send()
                        self.player_board_ready=True
                        self.update_text()

            if (self.player_board_ready and not self.player_move):
                data=self.net.get_data()
                if data[0]==2 and data[1]!=None:
                    data=data[1]
                    self.player_move=True
                    self.update_text()
                    if data != (-1,-1) and data !=430: #Solves 1st move problem + Temporary solve
                        self.player_board.shoot_player_cell(data[0],data[1])

            self.display.show()
            pygame.time.Clock().tick(60)

        return True