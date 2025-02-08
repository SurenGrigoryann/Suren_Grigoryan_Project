# importing libraries
import pygame
import random
import maps
import time

 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
RED = (255,0,0)
LIGHT_RED = (255,144,144)
LIGHT_BLUE = (135,206,235)
GREEN = (0,255,0)
DARK_GREEN = (1, 50, 32)
YELLOW = (255,255,0)

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Classes

class Player(pygame.sprite.Sprite):
    
    # Constructor function
    def __init__(self, x, y,color):
        
        super().__init__()
 
        # height, width
        self.image = pygame.Surface([25,25])
        self.image.fill(color)
 
        # setting the positon 
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.color = color
 
        # speed vector
        self.change_x = 0
        self.change_y = 0
        # walls and lakes collisions
        self.walls = None
        self.coins = None
        self.lakes = None
        self.ghosts = None
        # lives
        self.life = 1
        # power level
        self.level = None
    # end procedure

    # updating the players cordinations and other features
    def update(self):

        self.calc_grav()
        # updating player's position
        self.rect.x += self.change_x
 
        # Checking if we hit anything horizontally
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the wall
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # do the same for left
                self.rect.left = block.rect.right
            # end if
        # next block
 
        # moving up or down
        self.rect.y += self.change_y
 
        # Checking if we hit anything 
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
 
            # If we are moving up, set our up side to the bottom side of
            # the wall and the same if we are moving down
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0


            # end if
        # next block
    # end procedure

    def calc_grav(self):
        # checking if it is in the air or not
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .25
        # end if
    
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
        # end if
    # end procedure

    def jump(self):

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -6
        # end if
    # end procedure

    # movements procedures
    def go_left(self):
        self.change_x = -3
    # end procedure

    def go_right(self):
        self.change_x = 3
    # end procedure

    def stop(self):
        self.change_x = 0
    # end procedure

    # setting the life
    def set_life(self,life):
        self.life = life
    # end procedure

    # getting the life
    def get_life(self):
        return self.life
    # end procedure

# end class Player
 

class Block(pygame.sprite.Sprite):
    # Creating a class block in which players cannot collide to
    # Constructor function
    def __init__(self, x, y):

        super().__init__()
 
        # Making a dark green block with 18 heigth and 18 width from which we will build our walls
        self.image = pygame.Surface([10,10])
        self.image.fill(DARK_GREEN)
 
        # set positions
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    # end procedure
# end class Block

class Lakes(pygame.sprite.Sprite):
    # creating a class lakes. Red player can go through the red lake but not the blue lake. The opposite for the Blue player.
    # Cosntructor function
    def __init__(self,x,y,COLOR):

        super().__init__()
        self.image = pygame.Surface([10,10])
        self.image.fill(COLOR)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.color = COLOR
    # end procedure
# end class Lakes

class Trapeze(pygame.sprite.Sprite):
    def __init__(self,x,y):

        super().__init__()
        self.image = pygame.Surface([10,10])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coins(pygame.sprite.Sprite):
    def __init__ (self,x,y,color):


        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        


    def draw(self,screen_to_draw):
        if self.color == RED:
             red_coin = pygame.image.load('red_coin.jpg')
             red_coin_image = pygame.transform.scale(red_coin, (20,20))
             screen_to_draw.blit(red_coin_image, (self.x,self.y))
        if self.color == BLUE:
             blue_coin = pygame.image.load('blue_coin.jpg')
             blue_coin_image = pygame.transform.scale(blue_coin, (20,20))
             screen_to_draw.blit(blue_coin_image, (self.x,self.y))
    



# Initializing pygame
pygame.init()
 
# Creating the screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
 
# Seting the title of the window
pygame.display.set_caption('Fboy and Wgirl')

# Setting all of our groums that we are going to use
all_sprite_list = pygame.sprite.Group()
 
wall_list = pygame.sprite.Group()

red_lake_list = pygame.sprite.Group()

blue_lake_list = pygame.sprite.Group()

trapeze_list = pygame.sprite.Group()

coins_list = pygame.sprite.Group()

red_coin_list = pygame.sprite.Group()

blue_coin_list = pygame.sprite.Group()





# sc_map is the current map

sc_map = maps.level_one
# sm is the starting map
sm = maps.level_one



# creating the map from a 2D list of numbers
def create_map(map):
        global all_sprite_list
        global wall_list
        x = 0
        y = 0
        for i in map:
            for j in i:
                if j == 1:
                    wall = Block(x, y)
                    wall_list.add(wall)
                    all_sprite_list.add(wall)
                elif j == 3:
                    red_lake = Lakes(x, y,LIGHT_RED)
                    red_lake_list.add(red_lake)    
                    all_sprite_list.add(red_lake)

                elif j == 2:
                    blue_lake = Lakes(x, y,LIGHT_BLUE)
                    blue_lake_list.add(blue_lake)    
                    all_sprite_list.add(blue_lake)
                
                elif j == 4:
                    trapeze = Trapeze(x,y)
                    trapeze_list.add(trapeze)
                    all_sprite_list.add(trapeze)

                elif j == 8:
                    red_coin = Coins(x,y,RED)
                    red_coin_list.add(red_coin)
                    coins_list.add(red_coin)

                elif j == 9:
                    blue_coin = Coins(x,y,BLUE)
                    blue_coin_list.add(blue_coin)
                    coins_list.add(blue_coin)

                # end if

                x += 10
            # next i
            x = 0
            y += 10
        # next j 

# end procedure

# creates player 1 or the Fboy


def delete_map():
    global all_sprite_list 
    all_sprite_list.empty()
    wall_list.empty()
    coins_list.empty()
# end procedure

    

def check_die(player,lake_list):
    for lake in lake_list:
        if(player.rect.x+24 >= lake.rect.x and player.rect.x - 9 <= lake.rect.x) and (player.rect.y +24 >= lake.rect.y  and player.rect.y -9 <= lake.rect.y ):
            player.life = player.life - 1
        # end if
    # next lake
# end procedure
def high(player,list_of_trapeze):
    for trapeze in list_of_trapeze:
        if(player.rect.x+12 >= trapeze.rect.x and player.rect.x - 9 <= trapeze.rect.x) and (player.rect.y +12 >= trapeze.rect.y - 170  and player.rect.y -9 <= trapeze.rect.y ):
                return True

def red_score(player):
    global coins_list
    for coin in coins_list:
        if(player.rect.x+24 >= coin.x and player.rect.x - 9 <= coin.x) and (player.rect.y +24 >= coin.y  and player.rect.y -9 <= coin.y ):
            coins_list.remove(coin)

                
                 
        
def create_players(x,y,color):
    player = Player(x, y, color)
    player.walls = wall_list
    all_sprite_list.add(player)
    return player
# end function

player1 = create_players(25,575,RED)
player2 = create_players(1225,575,BLUE)    

# creating the map

def initial_map(first_m):
    create_map(first_m)
# end procedure

def live_map(current_map,player_one,player_two):
    global sm
    
   
    if player1.life <= 0 or player2.life <= 0 or current_map == [1] :
        delete_map()
        lose()
        return_to_menu()
        current_map = 1

    elif current_map == [0]:
        delete_map()
        menu()
        

    elif current_map != sm:
        delete_map()
        create_map(current_map)
        player_one.walls = wall_list
        player_two.walls = wall_list
        all_sprite_list.add(player1)
        all_sprite_list.add(player2)
    # end if
    for coin in coins_list:
        coin.draw(screen)
    sm = current_map
# end procedure

def menu():
    screen.fill(WHITE)
    font = pygame.font.Font('freesansbold.ttf',82)
    text = font.render('Menu',True,GREEN,BLUE)
    textRect = text.get_rect()
    textRect.center = ( 1280//2, 720//2)
    font2 = pygame.font.Font('freesansbold.ttf',32)
    text2 = font2.render('To return to the game press B or the button on the top right', True, GREEN,BLUE)
    text2Rect = text2.get_rect()
    text2Rect.center = (1280//2, 720//2 + 100)
    screen.blit(text, textRect)
    screen.blit(text2,text2Rect)
# end procedure

def lose():
    global sc_map
    screen.fill(BLACK)
    font = pygame.font.Font('freesansbold.ttf',82)
    lose = font.render('You Lost!', True, WHITE,RED)
    loseRect = lose.get_rect()
    loseRect.center = (1280//2, 720//2)
    screen.blit(lose, loseRect)
    sc_map =[1]
# end procedure
    
def return_to_menu():
    return_font = pygame.font.Font('freesansbold.ttf',32)
    menu= return_font.render('Press the button R to restart the game!', True, WHITE,RED)
    menuRect = menu.get_rect()
    menuRect.center = (1280//2, 720//2 + 300)
    screen.blit(menu, menuRect)





def scores(p1,p2,c_list, rc_list, bc_list,score):
    textfont = pygame.font.SysFont('monospace',50)
    textTBD = textfont.render(f'score {score}',1,(RED))
    screen.blit(textTBD)
# end procedure

#setting up the clock
clock = pygame.time.Clock()
 

# drawinf the initial map
initial_map(sc_map)

done = False
# the main loop
while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # the quit method
            
        # Creating the keys for player 1 and player 2     
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1.go_left()
            elif event.key == pygame.K_RIGHT:
                player1.go_right()
            elif event.key == pygame.K_UP:
                player1.jump()


            if event.key == pygame.K_a:
                player2.go_left()
            elif event.key == pygame.K_d:
                player2.go_right()
            elif event.key == pygame.K_w:
                player2.jump()

            if event.key == pygame.K_l:
                sc_map = maps.map1
            if event.key == pygame.K_b:
                sc_map = maps.l
            if event.key == pygame.K_m:
                sc_map = [0]
            if event.key == pygame.K_r:
                if sc_map == [1]:
                    player1.life =1
                    player2.life = 1
                    player1.rect.x,player1.rect.y = 25,575
                    player2.rect.x,player2.rect.y = 1225,575
                    sc_map = [0]


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player1.change_x < 0:
                player1.stop()
            if event.key == pygame.K_RIGHT and player1.change_x > 0:
                player1.stop()

            if event.key == pygame.K_a and player2.change_x < 0:
                player2.stop()
            if event.key == pygame.K_d and player2.change_x > 0:
                player2.stop()


        if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x,y = pos[0],pos[1]
  
                if (x > 30 and x < 80) and (y > 20 and y < 70):
                    if sc_map == [0]:
                        sc_map = maps.l
                    else:
                        sc_map = [0]
        

    screen.fill(GREEN)

    live_map(sc_map,player1,player2)
    check_die(player1,blue_lake_list)
    check_die(player2,red_lake_list)
    while high(player1,trapeze_list):
        player1.rect.y = player1.rect.y - 10

    high(player2, trapeze_list)
    if sc_map == [0]:
        play = pygame.image.load('play_button.jpg')
        play_image = pygame.transform.scale(play, (50,50))
        screen.blit(play_image, (30,20))
    
    elif sc_map != [1]:

        pause = pygame.image.load('pause_button.jpg')
        pause_image = pygame.transform.scale(pause, (50,50))
        screen.blit(pause_image,(30,20))
    


    # end if
    
    # updating all of the objects
    all_sprite_list.update()

    all_sprite_list.draw(screen)
    
    # drawing everything
    pygame.display.flip()
    # fliping the display
    clock.tick(60)
 
pygame.quit()
# quiting the pygame