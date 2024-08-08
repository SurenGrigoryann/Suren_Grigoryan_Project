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
GREEN = (0,255,0)
DARK_GREEN = (1, 50, 32)

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

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
        self.walls = None
        self.lakes = None
        self.ghosts = None
        self.life = 1
        self.level = None
    # end procedure


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
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .25
    
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -6

    def go_left(self):
        self.change_x = -3
 
    def go_right(self):
        self.change_x = 3
 
    def stop(self):
        self.change_x = 0
    
    def set_life(self,life):
        self.life = life

    def get_life(self):
        return self.life

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
# Initializing pygame
pygame.init()
 
# Creating the screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
 
# Seting the title of the window
pygame.display.set_caption('Fboy and Wgirl')

all_sprite_list = pygame.sprite.Group()
 
wall_list = pygame.sprite.Group()

red_lake_list = pygame.sprite.Group()

blue_lake_list = pygame.sprite.Group()





# the map
sc_map = maps.l
sm = maps.l
ft = 0



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
                elif j == 2:
                    red_lake = Lakes(x, y,LIGHT_RED)
                    red_lake_list.add(red_lake)    
                    all_sprite_list.add(red_lake)

                elif j == 3:
                    blue_lake = Lakes(x, y,BLUE)
                    blue_lake_list.add(blue_lake)    
                    all_sprite_list.add(blue_lake)

                x += 10
            x = 0
            y += 10

# creates player 1 or the Fboy


def delete_map():
    global all_sprite_list 
    all_sprite_list.empty()
    wall_list.empty()

    

def check_die(player,lake_list):
    for lake in lake_list:
        if(player.rect.x+24 >= lake.rect.x and player.rect.x - 9 <= lake.rect.x) and (player.rect.y +24 >= lake.rect.y  and player.rect.y -9 <= lake.rect.y ):
            player.life = player.life - 1

        
def create_players(x,y,color):
    
    player = Player(x, y, color)
    player.walls = wall_list
    all_sprite_list.add(player)
    return player

player1 = create_players(100,100,RED)
player2 = create_players(900,200,BLUE)    

# creating the map
def initial_map(first_m):
    create_map(first_m)

def live_map(current_map,player_one,player_two):
    global sm
    
   
    if player1.life <= 0 or player2.life <= 0 or current_map == [1] :
        delete_map()
        lose()
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

        

    sm = current_map

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

def lose():
    global sc_map
    screen.fill(BLACK)
    font = pygame.font.Font('freesansbold.ttf',82)
    lose = font.render('You Lost!', True, WHITE,RED)
    loseRect = lose.get_rect()
    loseRect.center = (1280//2, 720//2)
    screen.blit(lose, loseRect)
    sc_map =[1]



clock = pygame.time.Clock()

done = False
initial_map(sc_map)
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
                    player1.rect.x,player1.rect.y = 100,100
                    player2.rect.x,player2.rect.y = 900,100
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
    if sc_map == [0]:
        play = pygame.image.load('play_button.jpg')
        play_image = pygame.transform.scale(play, (50,50))
        screen.blit(play_image, (30,20))
    
    elif sc_map != [1]:

        pause = pygame.image.load('pause_button.jpg')
        pause_image = pygame.transform.scale(pause, (50,50))
        screen.blit(pause_image,(30,20))
    
    # updating all of the objects
    all_sprite_list.update()


    all_sprite_list.draw(screen)
    
    # drawing everything
    pygame.display.flip()
    # fliping the display
    clock.tick(60)
 
pygame.quit()
# quiting the pygame

# add special lakes

