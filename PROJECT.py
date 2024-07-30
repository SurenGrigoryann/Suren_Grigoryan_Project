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
 
        # speed vector
        self.change_x = 0
        self.change_y = 0
        self.walls = None
        self.ghosts = None
        self.live = 3
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
            self.change_y = -10

    def go_left(self):
        self.change_x = -6
 
    def go_right(self):
        self.change_x = 6
 
    def stop(self):
        self.change_x = 0
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
                    red_lake = Lakes(x, y,RED)
                    red_lake_list.add(red_lake)    
                    all_sprite_list.add(red_lake)
                elif j == 3:
                    blue_lake = Lakes(x, y,BLUE)
                    blue_lake_list.add(blue_lake)    
                    all_sprite_list.add(blue_lake)
                x += 10
            x = 0
            y += 10


def delete_map():
    global all_sprite_list 
    all_sprite_list.empty()
    wall_list.empty()


    

# creating the map
def initial_map(first_m):
    create_map(first_m)

def live_map(current_map):
    global sm
    
    if current_map == [0]:
        delete_map()
        menu()
        
    elif current_map != sm:
        delete_map()
        create_map(current_map)

    sm = current_map

def menu():
    screen.fill(WHITE)
    font = pygame.font.Font('freesansbold.ttf',82)
    text = font.render('Menu',True,GREEN,BLUE)
    textRect = text.get_rect()
    textRect.center = ( 1280//2, 720//2)
    screen.blit(text, textRect)
    

# we will need to players so
# creates player 1 or the Fboy
player1 = Player(100, 100, RED)
player1.walls = wall_list
all_sprite_list.add(player1)

# creates player 2 or the Wgirl
player2 = Player(900, 100, BLUE)
player2.walls = wall_list
all_sprite_list.add(player2)


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
  
                if (x > 5 or x < 55) and (y > 5 or y < 45):
                    if sc_map == [0]:
                        sc_map = maps.l
                    else:
                        sc_map = [0]
    

    screen.fill(GREEN)
    live_map(sc_map)
    if sc_map == [0]:
        play = pygame.image.load('play_button.jpg')
        play_image = pygame.transform.scale(play, (50,50))
        screen.blit(play_image, (30,20))
    else:

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

