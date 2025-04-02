# importing all the libraries needed
import pygame
import random
import  maps

import details
import  testmenu
from details import Button
import time
import sys
import menu
from menu import run_menu




# All the colors held as constants, in rgb
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
RED = (255,0,0)
LIGHT_RED = (255,144,144)
LIGHT_BLUE = (135,206,235)
GREEN = (0,255,0)
DARK_GREEN = (1, 50, 22)
LIGHT_GREEN = (0,130,0)
DARK_GRAY = (61,60,60)
YELLOW = (255,255,0)
PURPLE = (160,32,240)
BROWN = (139,69,19)
ORANGE = (255, 99, 7)

# The dimensions of the screen held as constans
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720



# all the images that will be used
images = {
    'red_player': pygame.image.load('pictures/red_player.png').convert_alpha(),
    'blue_player': pygame.image.load('pictures/blue_player.png').convert_alpha(),
    'fast_enemy': pygame.image.load('pictures/fast_enemy.png').convert_alpha(),
    'tank_enemy': pygame.image.load('pictures/Tank.png').convert_alpha(),
    'red_door': pygame.image.load('pictures/red_door.jpg').convert(),
    'blue_door': pygame.image.load('pictures/blue_door.jpg').convert(),
    'background': pygame.transform.scale(pygame.image.load("pictures/background1.jpg").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT-80)),
    'red_lake': pygame.image.load('pictures/red_lake.png').convert_alpha(),
    'blue_lake': pygame.image.load('pictures/blue_lake.png').convert_alpha(),
    'green_lake': pygame.image.load('pictures/green_lake.png').convert_alpha(),
    'red_coin': pygame.image.load('pictures/red_coin.png').convert_alpha(),
    'blue_coin': pygame.image.load('pictures/blue_coin.png').convert_alpha(),
    'no_gun': pygame.image.load('pictures/no_gun.png').convert_alpha(),
    'drink': pygame.image.load('pictures/drink.png').convert_alpha(),

    'block': pygame.image.load('pictures/block.jpg').convert(),
}




# stack held as a stack
class Stack:
    def __init__(self):
        self.items = []
    # defining the stack
    def push(self, item):
        self.items.append(item)
    # push procedure
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("pop from empty stack")
        # end if

    def peek(self):
        """Return the item at the top of the stack without removing it.
        
        Raises:
            IndexError: If the stack is empty.
        """
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("peek from empty stack")

    def is_empty(self):
        """Return True if the stack is empty, False otherwise."""
        return len(self.items) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self.items)









class Drink(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        
        self.image = pygame.transform.scale(images['drink'], (35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Classes
class Door(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super().__init__()

        self.color = color
        if self.color == LIGHT_RED:
            self.img= pygame.image.load('pictures/red_door.jpg')
        elif self.color == LIGHT_BLUE:
            self.img= pygame.image.load('pictures/blue_door.jpg')
        self.image = pygame.transform.scale(self.img, (35, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update_door(self, player):
        return self.rect.colliderect(player.rect)

class Portal(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super().__init__()

        self.image = pygame.Surface([10,10])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x1 = x
        self.y1 = y 
        self.x2 = x + 110
        self.x3 = x - 300
        self.y2 = y + 110
        self.y3 = y - 110
        self.color = color
    
    def open_portal(self,portal_opener,p1,p2, direction):
        if direction == "down":
            if ((self.y2 != self.rect.y) and 
            (((p1.rect.x <= portal_opener.rect.x + 15 and p1.rect.x >= portal_opener.rect.x - 15) and (p1.rect.y <= portal_opener.rect.y + 15 and p1.rect.y >= portal_opener.rect.y - 25))
            or
            ((p2.rect.x <= portal_opener.rect.x + 15 and p2.rect.x >= portal_opener.rect.x - 15) and (p2.rect.y <= portal_opener.rect.y + 15 and p2.rect.y >= portal_opener.rect.y - 25)))):
                self.rect.y += 1.25

            elif (self.y1 != self.rect.y):
                self.rect.y -= 1.25

        elif direction == "up":
            if ((self.y3 != self.rect.y) and 
            (((p1.rect.x <= portal_opener.rect.x + 15 and p1.rect.x >= portal_opener.rect.x - 15) and (p1.rect.y <= portal_opener.rect.y + 15 and p1.rect.y >= portal_opener.rect.y - 25))
            or
            ((p2.rect.x <= portal_opener.rect.x + 15 and p2.rect.x >= portal_opener.rect.x - 15) and (p2.rect.y <= portal_opener.rect.y + 15 and p2.rect.y >= portal_opener.rect.y - 25)))):
                self.rect.y -= 1.25
            elif (self.y1 != self.rect.y):
                self.rect.y += 1.25

        elif direction == "left":
            if ((self.x3 != self.rect.x) and 
            (((p1.rect.x <= portal_opener.rect.x + 15 and p1.rect.x >= portal_opener.rect.x - 15) and (p1.rect.y <= portal_opener.rect.y + 15 and p1.rect.y >= portal_opener.rect.y - 25))
            or
            ((p2.rect.x <= portal_opener.rect.x + 15 and p2.rect.x >= portal_opener.rect.x - 15) and (p2.rect.y <= portal_opener.rect.y + 15 and p2.rect.y >= portal_opener.rect.y - 25)))):
                self.rect.x -= 1.25
                
            elif (self.x1 != self.rect.x):
                self.rect.x += 1.25
                
class Portal_opener(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super().__init__()
        self.image = pygame.Surface([10,10])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color



class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,type):
        super().__init__()
            
        self.type = type
        self.life = 0
        self.gun = None
        if self.type == "Fast":
            self.length = 45
            self.width = 40
            self.life = 5
            self.speed = 2
            self.gun == "Short"
            self.image = pygame.transform.scale(images['fast_enemy'], (self.width, self.length))

        elif self.type == "Tank":
            self.length = 60
            self.width = 50
            self.life = 10
            self.speed = 0.75
            self.gun == "Short"
            self.image = pygame.transform.scale(images['tank_enemy'], (self.width, self.length))
            

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.x = x
        self.y = y
    def attack(self,player):
        if (player.rect.y <= self.rect.y + self.length and player.rect.y > self.rect.y -25) and ((player.rect.x >= self.rect.x) and (player.rect.x <= self.x + 160)):
                if self.type == "Tank":
                    self.image = pygame.transform.scale(images['tank_enemy'], (self.width, self.length))
                elif self.type == "Fast":
                    self.flipped_image = pygame.transform.flip(self.image, True, False)
                    self.image = pygame.transform.scale(self.flipped_image, (40, 45))

                self.rect.x += self.speed

            
        elif (player.rect.y <= self.rect.y + self.length and player.rect.y > self.rect.y - 25) and ((player.rect.x <= self.rect.x) and (player.rect.x >= self.x -160)):
                if self.type == "Tank":
                    self.flipped_image = pygame.transform.flip(self.image, True, False)
                    self.image = pygame.transform.scale(self.flipped_image, (50, 60))
                elif self.type == "Fast":
                    self.img= pygame.image.load('pictures/fast_enemy.png')
                    self.image = pygame.transform.scale(self.img, (40, 45))

                self.rect.x -= self.speed



        if self.type == "Tank":
            if (player.rect.y <= self.rect.y + self.length and player.rect.y > self.rect.y -25) and ((player.rect.x >= self.rect.x) and (player.rect.x <= self.x + 160)):
                self.image = pygame.transform.scale(images['tank_enemy'], (self.width, self.length))
                self.rect.x += 0.75
            
            elif (player.rect.y <= self.rect.y + self.length and player.rect.y > self.rect.y - 25) and ((player.rect.x <= self.rect.x) and (player.rect.x >= self.x -160)):
                self.flipped_image = pygame.transform.flip(self.image, True, False)
                self.image = pygame.transform.scale(self.flipped_image, (50, 60))

                self.rect.x -= 0.75
        elif self.type == "Fast":
            if (player.rect.y <= self.rect.y + self.length and player.rect.y > self.rect.y -25) and ((player.rect.x >= self.rect.x) and (player.rect.x <= self.x + 200)):
                self.flipped_image = pygame.transform.flip(self.image, True, False)
                self.image = pygame.transform.scale(self.flipped_image, (40, 45))

                self.rect.x += 2   

            elif (player.rect.y <= self.rect.y + self.length and player.rect.y > self.rect.y - 25) and ((player.rect.x <= self.rect.x) and (player.rect.x >= self.x -200)):
                self.img= pygame.image.load('pictures/fast_enemy.png')
                self.image = pygame.transform.scale(self.img, (40, 45))

                self.rect.x -= 2
                

class Gun(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.img= pygame.image.load('pictures/no_gun.png')
        self.image = pygame.transform.scale(self.img, (40,30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    


        

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y, direction):
        super().__init__()
        
        self.image = pygame.Surface([10,10])
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        if self.direction == "right":
            self.speed_x = 5
        elif direction == "left":
            self.speed_x = -5
        else:
            self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH:
            self.kill()



                

    
    


        




class Player(pygame.sprite.Sprite):
    
    # Constructor function
    def __init__(self, x, y, color):
        
        super().__init__()
        self.color = color

        if self.color == RED:
            self.image = pygame.transform.scale(images['red_player'], (25, 35))
            self.direction = "right"
            self.previous_direction = 1
        elif self.color == BLUE:
            self.image = pygame.transform.scale(images['blue_player'], (25, 35))
            self.direction = "left"
            self.previous_direction = -1
        # height, width
        # setting the positon 
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.color = color
 
        self.original_color = color

        self.color_timer = None
        self.color_duration = 10000



        # speed vector
        self.change_x = 0
        self.change_y = 0
        self.enemies = None
        # walls and lakes collisions
        self.walls = None
        self.portals = None
        self.coins = None
        self.lakes = None
        self.guns = False
        self.timer = False
        self.duration = 10000
        # lives
        self.life = 1
        # power level
        
    
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

       
        if self.portals is not None:
            portal_hit_list = pygame.sprite.spritecollide(self, self.portals, False)
        else:
            portal_hit_list = []
        for portal in portal_hit_list:
 
            # If we are moving up, set our up side to the bottom side of
            # the wall and the same if we are moving down
            if self.change_y > 0:
                self.rect.bottom = portal.rect.top
            elif self.change_y < 0:
                self.rect.top = portal.rect.bottom

            self.change_y = 0

        if self.color != self.original_color and self.color_timer is not None:
            current_time = pygame.time.get_ticks()
            if current_time - self.color_timer >= self.color_duration:
                # 10 seconds have passed, revert to original
                self.color = self.original_color
                if self.color == RED:
                    self.image = pygame.transform.scale(images['red_player'], (25, 35))
                elif self.color == BLUE:
                    self.image = pygame.transform.scale(images['blue_player'], (25, 35))
                self.color_timer = None

       # gun_hit_list = pygame.sprite.spritecollide(self, self.guns, False)
        #for gun in gun_hit_list:

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
        walls_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        if self.portals is not None:
             portals_hit_list = pygame.sprite.spritecollide(self, self.portals, False)
        else:
            portals_hit_list = []
        platform_hit_list = walls_hit_list + portals_hit_list
        self.rect.y -= 2
        
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -6.5
        # end if
    # end procedure

    # movements procedures
    def go_left(self):
        if  self.direction == "right" and self.previous_direction == 1:
            if self.color == RED:
                self.img= pygame.image.load('pictures/red_player.png')
            elif self.color == BLUE:
                self.img= pygame.image.load('pictures/blue_player.png')

            self.flipped_image = pygame.transform.flip(self.img, True, False)
            self.image = pygame.transform.scale(self.flipped_image, (25, 35))
            screen.blit(self.image, (self.rect.x, self.rect.y))
            self.direction = "left"
            
        self.previous_direction = -1
        self.change_x = -3
        
        
    # end procedure

    def go_right(self):
        if self.direction =="left" and self.previous_direction == -1:
            if self.color == RED:
                
                self.img= pygame.image.load('pictures/red_player.png')
            elif self.color == BLUE:
                self.img= pygame.image.load('pictures/blue_player.png')

            
            self.image = pygame.transform.scale(self.img, (25, 35))
            screen.blit(self.image, (self.rect.x, self.rect.y))
            print(1)
            self.direction = "right"

        self.previous_direction = 1
        self.change_x = 3
    # end procedure

    def stop(self):
        if self.change_x == 3:
            self.previous_direction = 1
        elif self.change_x == -3:
            self.previous_direction = -1
        self.change_x = 0
    # end procedure

    # setting the life
    def set_life(self,life):
        self.life = life
    # end procedure

    # getting the life
    def get_life(self):
        return self.life
    def shoot(self):

        if self.guns:
            if self.previous_direction == 1:
                bullet = Bullet(self.rect.x,self.rect.y,"right")
                bullet_list.add(bullet)
                all_sprite_list.add(bullet)
            elif self.previous_direction == -1:
                bullet = Bullet(self.rect.x,self.rect.y,"left")
                bullet_list.add(bullet)
                all_sprite_list.add(bullet)

    def change_color(self, changing_color):
        if self.color != changing_color:
            self.color_timer = pygame.time.get_ticks()
            self.color = changing_color
            if self.color == RED:
                self.image = pygame.transform.scale(images['red_player'], (25, 35))
            elif self.color == BLUE:
                self.image = pygame.transform.scale(images['blue_player'], (25, 35))

    # end procedure

# end class Player
 

class Block(pygame.sprite.Sprite):
    # Creating a class block in which players cannot collide to
    # Constructor function

    def __init__(self, x, y):

        super().__init__()
        self.img = pygame.image.load('pictures/block.jpg')
        self.image = pygame.transform.scale(self.img, (10, 10))
        # Making a dark green block with 18 heigth and 18 width from which we will build our walls
      # all instances use the same image

        # set positions
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    # end procedure
# end class Block

class Lakes(pygame.sprite.Sprite):
    # creating a class lakes. Red player can go through the red lake but not the blue lake. The opposite for the Blue player.
    # Cosntructor function
    def __init__(self,x,y,color):

        super().__init__()
        self.color = color
        if self.color == LIGHT_RED:
            self.img = pygame.image.load('pictures/red_lake.png').convert_alpha()
        elif self.color == LIGHT_BLUE:
            self.img = pygame.image.load('pictures/blue_lake.png').convert_alpha()
        elif self.color == LIGHT_GREEN:
            self.img = pygame.image.load('pictures/green_lake.png').convert_alpha()
        self.image = pygame.transform.scale(self.img, (10, 10))
       
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

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
             red_coin = pygame.image.load('pictures/red_coin.png')
             red_coin_image = pygame.transform.scale(red_coin, (20,20))
             screen_to_draw.blit(red_coin_image, (self.x,self.y))
        if self.color == BLUE:
             blue_coin = pygame.image.load('pictures/blue_coin.png')
             blue_coin_image = pygame.transform.scale(blue_coin, (20,20))
             screen_to_draw.blit(blue_coin_image, (self.x,self.y))
    



# Initializing pygame
pygame.init()
 
# Creating the screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

 
# Seting the title of the window
pygame.display.set_caption('Fboy and Wgirl')

# Setting all of our groums that we are going to use

def create_lists():
    global all_sprite_list, all_players_list, wall_list, red_lake_list, blue_lake_list, green_lake_list
    global all_lakes_list, trapeze_list, coins_list, red_coin_list, blue_coin_list
    global all_enemy_list, all_gun_list, all_drink_list, bullet_list, portal_list_spr, portal_list
    global portal_opener_list_spr, portal_opener_list, door_list_spr, door_list

    all_sprite_list = pygame.sprite.Group()
    all_players_list = pygame.sprite.Group()
    wall_list = pygame.sprite.Group()
    red_lake_list = pygame.sprite.Group()
    blue_lake_list = pygame.sprite.Group()
    green_lake_list = pygame.sprite.Group()
    all_lakes_list = {RED: [], BLUE: [], LIGHT_GREEN: []}
    trapeze_list = pygame.sprite.Group()
    coins_list = pygame.sprite.Group()
    red_coin_list = pygame.sprite.Group()
    blue_coin_list = pygame.sprite.Group()
    all_enemy_list = pygame.sprite.Group()
    all_gun_list = pygame.sprite.Group()
    all_drink_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    portal_list_spr = pygame.sprite.Group()
    portal_list = {'purple': [], 'yellow ': [], 'orange': [], 'black': [], 'brown': []}
    portal_opener_list_spr = pygame.sprite.Group()
    portal_opener_list = {'purple': [], 'yellow ': [], 'orange': [], 'black': [], 'brown': []}
    door_list_spr = pygame.sprite.Group()
    door_list = {'red': [], 'blue': []}

create_lists()

def create_players(x,y,color):
    player = Player(x, y, color)
    player.walls = wall_list
    player.enemies = all_enemy_list
    player.portals = portal_list_spr
    all_sprite_list.add(player)

    return player

player1 = create_players(25,575,RED)
player2 = create_players(20,400,BLUE)   



# sc_map is the current map

sc_map = maps.level_three

# sm is the starting map
sm = [1]
start_time = pygame.time.get_ticks() 


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
                    all_lakes_list[RED].append(red_lake)

                elif j == 2:
                    blue_lake = Lakes(x, y,LIGHT_BLUE)
                    blue_lake_list.add(blue_lake)    
                    all_sprite_list.add(blue_lake)
                    all_lakes_list[BLUE].append(blue_lake)
                
                elif j == 4:
                    trapeze = Trapeze(x,y)
                    trapeze_list.add(trapeze)
                    all_sprite_list.add(trapeze)
                elif j == 5:
                    blue_door = Door(x,y,LIGHT_BLUE)
                    door_list_spr.add(blue_door)  
                    door_list['blue'].append(blue_door)    
                    all_sprite_list.add(blue_door)
                elif j == 6:
                    red_door = Door(x,y,LIGHT_RED)
                    door_list_spr.add(red_door)  
                    door_list['red'].append(red_door)    
                    all_sprite_list.add(red_door)
                elif j == 7:
                    green_lake = Lakes(x, y,LIGHT_GREEN)
                    green_lake_list.add(green_lake)    
                    all_sprite_list.add(green_lake)
                    all_lakes_list[LIGHT_GREEN].append(green_lake)
                

                elif j == 8:
                    red_coin = Coins(x,y,RED)
                    red_coin_list.add(red_coin)
                    coins_list.add(red_coin)


                elif j == 9:
                    blue_coin = Coins(x,y,BLUE)
                    blue_coin_list.add(blue_coin)
                    coins_list.add(blue_coin)


                elif j == 'p':
                    purple_portal = Portal(x,y,PURPLE)
                    portal_list_spr.add(purple_portal)
                    portal_list['purple'].append(purple_portal) 
                    all_sprite_list.add(purple_portal)
                elif j == 'P':
                    purple_portal_opener = Portal_opener(x,y,PURPLE)
                    portal_opener_list_spr.add(purple_portal_opener)
                    portal_opener_list['purple'].append(purple_portal_opener) 
                    all_sprite_list.add(purple_portal_opener)                    
                elif j == 'b':
                    brown_portal = Portal(x,y, BROWN)
                    portal_list_spr.add(brown_portal)
                    portal_list['brown'].append(brown_portal) 
                    all_sprite_list.add(brown_portal)
                elif j == 'B':
                    brown_portal_opener = Portal_opener(x,y,BROWN)
                    portal_opener_list_spr.add(brown_portal_opener)
                    portal_opener_list['brown'].append(brown_portal_opener) 
                    all_sprite_list.add(brown_portal_opener)    
                elif j == 'o':
                    orange_portal = Portal(x,y,ORANGE)
                    portal_list_spr.add(orange_portal)
                    portal_list['orange'].append(orange_portal) 
                    all_sprite_list.add(orange_portal)
                elif j == 'O':
                    orange_portal_opener = Portal_opener(x,y,ORANGE)
                    portal_opener_list_spr.add(orange_portal_opener)
                    portal_opener_list['orange'].append(orange_portal_opener) 
                    all_sprite_list.add(orange_portal_opener)    
                elif j == 'F':
                    fast_enemy = Enemy(x,y, 'Fast')
                    all_enemy_list.add(fast_enemy)
                    all_sprite_list.add(fast_enemy)
                elif j == 'T':
                    Tank_enemy = Enemy(x,y, 'Tank')
                    all_enemy_list.add(Tank_enemy)
                    all_sprite_list.add(Tank_enemy)

                elif j == 'G':
                    gun = Gun(x,y)
                    all_gun_list.add(gun)
                    all_sprite_list.add(gun)
                elif j == 'd':
                    drink = Drink(x,y)
                    all_drink_list.add(drink)
                    all_sprite_list.add(drink)                               

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
    trapeze_list.empty()
    red_lake_list.empty()
    blue_lake_list.empty()
    all_lakes_list[RED].clear()
    all_lakes_list[BLUE].clear()
    all_lakes_list[LIGHT_GREEN].clear()
    green_lake_list.empty()
    all_enemy_list.empty()
    all_gun_list.empty()
    bullet_list.empty()
    portal_list_spr.empty()
    portal_opener_list_spr.empty()
    portal_list['black'].clear()
    portal_list['brown'].clear()
    portal_list['orange'].clear()
    portal_list['purple'].clear()
    portal_list['yellow '].clear()
    portal_opener_list['black'].clear()
    portal_opener_list['brown'].clear()
    portal_opener_list['orange'].clear()
    portal_opener_list['purple'].clear()
    portal_opener_list['yellow '].clear()
    door_list_spr.empty()   
    door_list['red'].clear()
    door_list['blue'].clear()
    player1.guns = False
    player2.guns = False
    player1.lakes = None
    player2.lakes = None
    player1.coins = None
    player2.coins = None
    player1.portals = None
    player2.portals = None
    player1.walls = None
    player2.walls = None



# end procedure

    

def check_die(player,lake_list, enemies):
    for key in lake_list:
        if player.color != key:

            for lake in lake_list[key]:
                if(player.rect.x+24 >= lake.rect.x and player.rect.x - 9 <= lake.rect.x) and (player.rect.y +34 >= lake.rect.y  and player.rect.y -14 <= lake.rect.y ):
                    player.life = player.life - 1
            for enemy in enemies:
                if(player.rect.x + 25 >= enemy.rect.x and player.rect.x <= enemy.rect.x) and (player.rect.y +25 >= enemy.rect.y  and player.rect.y -15 <= enemy.rect.y ):
                    player.life = player.life - 1
                

        # end if
    # next lake
# end procedure
def high(player,list_of_trapeze):
    for trapeze in list_of_trapeze:
        if(player.rect.x >= trapeze.rect.x-10 and player.rect.x <= trapeze.rect.x + 10) and (player.rect.y <= trapeze.rect.y and player.rect.y > trapeze.rect.y - 200):
            return 1

        elif (player.rect.x >= trapeze.rect.x-10 and player.rect.x <= trapeze.rect.x + 10) and player.rect.y == trapeze.rect.y - 250:
            return 2
            #and (player.rect.y >= trapeze.rect.y - 20 and player.rect.y <= trapeze.rect.y + 200):
   


def score_total(player):
    if player.color == BLUE: 
        for coin in blue_coin_list:
            if(player.rect.x+24 >= coin.x and player.rect.x - 9 <= coin.x) and (player.rect.y +24 >= coin.y  and player.rect.y -9 <= coin.y ):
                blue_coin_list.remove(coin)
                coins_list.remove(coin)
                
                return 1
        
    elif player.color == RED:
        for coin in red_coin_list:
            if(player.rect.x+24 >= coin.x and player.rect.x - 9 <= coin.x) and (player.rect.y +24 >= coin.y and player.rect.y -9 <= coin.y ):
                red_coin_list.remove(coin)
                coins_list.remove(coin)
                return 1
    return 0
    

                




all_maps = ['starting', 'levels', 'controls','settings','slides','level_one','level_two','level_three','level_four','level_five', 'winning',
            'losing', 'pause', 'quit','thanks']
current_map = 'starting'
previous_map = Stack()


map = [0]
# ['win'] is the winning screen
# ['lose'] is the losing screen
# ['menu'] is the menu screen
# ['details'] is the details screen




final_time_string = ""

def live_map():
    global map
    global current_map
    global previous_map
    global all_sprite_list
    global player1,player2

    if current_map == 'starting':
        previous_map.push(current_map)
        current_map = starting_map()
        
    elif current_map == 'levels':
        result = testmenu.main()
        if result == 'back':
            current_map = previous_map.pop()
        else:
            previous_map.push(current_map)
            current_map = result

    elif current_map =='controls':
        result = details.main()
        if result == 'back':
            current_map = previous_map.pop()
        else:
            previous_map.push(current_map)
            current_map = result
    elif current_map == 'settings':
        result = settings()
        if result == 'back':
            current_map = previous_map.pop()
        else:
            previous_map.push(current_map)
            current_map = result
    elif current_map == 'level_one':
        if previous_map.peek() != 'level_one':
            delete_map()
            create_lists()
            map = maps.level_one
            player1 = create_players(25,575,RED)
            player2 = create_players(20,400,BLUE)
            player1.walls = wall_list
            player2.walls = wall_list
            all_sprite_list.add(player1)
            all_sprite_list.add(player2)
            create_map(map)
            previous_map.push(current_map)
        check_die(player1,all_lakes_list,all_enemy_list)
        check_die(player2,all_lakes_list,all_enemy_list)
        if player1.life <= 0 or player2.life <= 0:
            delete_map()
            current_map = 'losing'
        if door_list['red'] and len(door_list['red']) >= 1 and door_list['blue'] and len(door_list['blue']) >= 1:
            if door_list['red'][0].update_door(player1) and door_list['blue'][0].update_door(player2):
                delete_map()
                testmenu.level_one.set_condition('passed')
                testmenu.level_two.set_condition('unlocked')
                current_map = 'winning'  
                print('hailo')
        ingame()

                
                 
    elif current_map == 'level_two':
        if previous_map.peek() != 'level_two':
            delete_map()
            create_lists()
            map = maps.level_two
            player1 = create_players(610,80,RED)
            player2 = create_players(645,80,BLUE)
            player1.walls = wall_list
            player2.walls = wall_list
            all_sprite_list.add(player1)
            all_sprite_list.add(player2)
            create_map(map)
            previous_map.push(current_map)
        check_die(player1,all_lakes_list,all_enemy_list)
        check_die(player2,all_lakes_list,all_enemy_list)
        if player1.life <= 0 or player2.life <= 0:
            delete_map()
            current_map = 'losing'
        if door_list['red'] and len(door_list['red']) >= 1 and door_list['blue'] and len(door_list['blue']) >= 1:
            if door_list['red'][0].update_door(player1) and door_list['blue'][0].update_door(player2):
                delete_map()
                testmenu.level_two.set_condition('passed')
                testmenu.level_three.set_condition('unlocked')
                current_map = 'winning'   
        ingame()
    
    elif current_map == 'level_three':
        if previous_map.peek() != 'level_three':
            delete_map()
            create_lists()
            map = maps.level_three
            player1 = create_players(25,575,RED)
            player2 = create_players(20,400,BLUE)
            player1.walls = wall_list
            player2.walls = wall_list
            all_sprite_list.add(player1)
            all_sprite_list.add(player2)
            create_map(map)
            previous_map.push(current_map)
        check_die(player1,all_lakes_list,all_enemy_list)
        check_die(player2,all_lakes_list,all_enemy_list)
        if player1.life <= 0 or player2.life <= 0:
            delete_map()
            current_map = 'losing'
        if door_list['red'] and len(door_list['red']) >= 1 and door_list['blue'] and len(door_list['blue']) >= 1:
            if door_list['red'][0].update_door(player1) and door_list['blue'][0].update_door(player2):
                delete_map()
                testmenu.level_three.set_condition('passed')
                testmenu.level_four.set_condition('unlocked')
                current_map = 'winning'   
        ingame()        
    elif current_map == 'level_four':
        if previous_map.peek() != 'level_four':
            delete_map()
            create_lists()
            map = maps.level_four
            player1 = create_players(25,575,RED)
            player2 = create_players(20,400,BLUE)
            player1.walls = wall_list
            player2.walls = wall_list
            all_sprite_list.add(player1)
            all_sprite_list.add(player2)
            create_map(map)
            previous_map.push(current_map)
        check_die(player1,all_lakes_list,all_enemy_list)
        check_die(player2,all_lakes_list,all_enemy_list)
        if player1.life <= 0 or player2.life <= 0:
            delete_map()
            current_map = 'losing'
        if door_list['red'] and len(door_list['red']) >= 1 and door_list['blue'] and len(door_list['blue']) >= 1:
            if door_list['red'][0].update_door(player1) and door_list['blue'][0].update_door(player2):
                delete_map()
                testmenu.level_four.set_condition('passed')
                testmenu.level_five.set_condition('unlocked')
                current_map = 'winning'   
        ingame()





    elif current_map == 'winning':
        delete_map()
        screen.fill(WHITE)
        result = winning()
        
        if result == 'back':
            current_map = previous_map.pop()
        else:
            previous_map.push(current_map)
            current_map = result        
        
    elif current_map == 'losing':
        delete_map()
        screen.fill(BLACK)
        result = lost_map()
        if result == 'back':
            current_map = previous_map.pop()
        else:
            previous_map.push(current_map)
            current_map = result

        for i in all_enemy_list:
            all_enemy_list.remove(i)
        for coin in blue_coin_list:
            blue_coin_list.remove(coin)
        for coin in red_coin_list:
            red_coin_list.remove(coin)
    
    print(door_list)



    print(current_map)

    
    # end if
    c = 11

    if portal_opener_list['purple']:
        p_opener_purple = portal_opener_list['purple'][0]
    else:
        p_opener_purple = []

    if portal_opener_list['brown']:
        p_opener_brown = portal_opener_list['brown'][0]
    else:
        p_opener_brown = []

    if portal_opener_list['orange']:
        p_opener_orange = portal_opener_list['orange'][0]
    else:
        p_opener_orange = []

    
    
    #p.open_portal(p_opener,player1)
    
    for i in portal_list['purple']:

        i.open_portal(p_opener_purple, player1, player2,"down")
    for i in portal_list['brown']:

        i.open_portal(p_opener_brown, player1, player2, "down")
    for i in portal_list['orange']:
        i.open_portal(p_opener_orange, player1, player2, "left")
        
    for enemy in all_enemy_list:
        enemy.attack(player1)
        enemy.attack(player2)


    #for i in portal_list['brown']:
       #rb i.open_portal(p_opener_brown,player1, player2)

    
   
   # print(x)


    for coin in coins_list:
        coin.draw(screen)




def starting_map():
    # Fill background
    global current_map
    while True:
        screen.fill(DARK_GRAY)
        
        # Draw the title
        title_font = pygame.font.Font('freesansbold.ttf', 64)
        title_text = title_font.render('TWIN TO WIN', True, BLACK)
        # Position the title at the top-center
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

        screen.blit(title_text, title_rect)



        levels_img = pygame.image.load('pictures/levels_button.png')
        levels_img = pygame.transform.scale(levels_img, (300, 300))
        levels_rect = levels_img.get_rect(center=(SCREEN_WIDTH // 4, 250))
        screen.blit(levels_img, levels_rect)

        start_img = pygame.image.load('pictures/start_button.png')
        start_img = pygame.transform.scale(start_img, (300, 300))
        start_rect = start_img.get_rect(center=(SCREEN_WIDTH //2, 400))
        screen.blit(start_img, start_rect)

        tutorial_img = pygame.image.load('pictures/tutorial_button.png')
        tutorial_img = pygame.transform.scale(tutorial_img, (300, 300))
        tutorial_rect = tutorial_img.get_rect(center=(SCREEN_WIDTH //4, 550))
        screen.blit(tutorial_img, tutorial_rect)



        settings_img = pygame.image.load('pictures/settings_button.png')
        settings_img = pygame.transform.scale(settings_img, (300, 300))
        settings_rect = settings_img.get_rect(center=(SCREEN_WIDTH - SCREEN_WIDTH //5 - 100, 550))
        screen.blit(settings_img, settings_rect)


        story_img = pygame.image.load('pictures/story_button.png')
        story_img = pygame.transform.scale(story_img, (300, 300))
        story_rect = story_img.get_rect(center=(SCREEN_WIDTH - SCREEN_WIDTH //5 - 100, 250))
        screen.blit(story_img, story_rect)

        question_rect = question_button()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # or return some value to handle closing
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # Get the current mouse position
                if levels_rect.collidepoint(pos):
                    return 'levels'
                elif start_rect.collidepoint(pos):
                    return 'start'
                elif tutorial_rect.collidepoint(pos):
                    return 'tutorial'
                elif settings_rect.collidepoint(pos):
                    return 'settings'
                elif story_rect.collidepoint(pos):
                    return 'story'
                elif question_rect.collidepoint(pos):
                    return 'controls'
    

def settings():
    global current_map
    while True:
        screen.fill(DARK_GRAY)

                # Draw the title
        title_font = pygame.font.Font('freesansbold.ttf', 64)
        title_text = title_font.render('Settings', True, BLACK)
        # Position the title at the top-center
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)


        restart_img = pygame.image.load('pictures/restart_the_game.png')
        restart_img = pygame.transform.scale(restart_img, (300, 300))
        restart_rect = restart_img.get_rect(center=(SCREEN_WIDTH // 2 - 300, 400))
        screen.blit(restart_img, restart_rect)

        menu_img = pygame.image.load('pictures/menu_button.png')
        menu_img = pygame.transform.scale(menu_img, (300, 300))
        menu_rect = menu_img.get_rect(center=(SCREEN_WIDTH // 2, 400))
        screen.blit(menu_img, menu_rect)

        quit_img = pygame.image.load('pictures/Quit.png')
        quit_img = pygame.transform.scale(quit_img, (300, 300))
        quit_rect = quit_img.get_rect(center=(SCREEN_WIDTH // 2 + 300, 400))
        screen.blit(quit_img, quit_rect)

        question_rect = question_button()
        back_rect = back_button()



        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
             # or return some value to handle closing
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # Get the current mouse position
                if restart_rect.collidepoint(pos):
                    return 'levels'
                elif menu_rect.collidepoint(pos):
                    return 'starting'
                elif quit_rect.collidepoint(pos):
                    return 'tutorial'
                elif question_rect.collidepoint(pos):
                    return 'controls'
                elif back_rect.collidepoint(pos):
                    return 'back'

def lost_map():
    while True:
        screen.fill(DARK_GRAY)
        # Draw the title
        title_font = pygame.font.Font('freesansbold.ttf', 64)
        title_text = title_font.render('You Lost!', True, BLACK)
        # Position the title at the top-center
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)



        lost_img = pygame.image.load('pictures/lost.png')
        lost_img = pygame.transform.scale(lost_img, (300, 300))
        lost_rect = lost_img.get_rect(center=(SCREEN_WIDTH // 2, 350))
        screen.blit(lost_img, lost_rect)

        menu_img = pygame.image.load('pictures/menu_button.png')
        menu_img = pygame.transform.scale(menu_img, (300, 300))
        menu_rect = menu_img.get_rect(center=(SCREEN_WIDTH // 2 - 160, 600))
        screen.blit(menu_img, menu_rect)

        restart_the_level_img = pygame.image.load('pictures/restart_the_level.png') 
        restart_the_level_img = pygame.transform.scale(restart_the_level_img, (300, 300))
        restart_the_level_rect = restart_the_level_img.get_rect(center=(SCREEN_WIDTH // 2 + 160, 600))
        screen.blit(restart_the_level_img, restart_the_level_rect)
        




        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
             # or return some value to handle closing
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # Get the current mouse position
                if menu_rect.collidepoint(pos):
                    return 'starting'
                if restart_the_level_rect.collidepoint(pos):
                    return 'back'



def winning():
    global final_time_string
    while True:
        title_font = pygame.font.Font('freesansbold.ttf', 64)
        title_text = title_font.render('Level Passed!', True, BLACK)
    # Position the title at the top-center
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)
        # Draw the title
        menu_img = pygame.image.load('pictures/menu_button.png')
        menu_img = pygame.transform.scale(menu_img, (300, 300))
        menu_rect = menu_img.get_rect(center=(SCREEN_WIDTH // 2 - 160, 600))
        screen.blit(menu_img, menu_rect)

        next_level_img = pygame.image.load('pictures/next_level.png')
        next_level_img = pygame.transform.scale(next_level_img, (300, 300))
        next_level_rect = next_level_img.get_rect(center=(SCREEN_WIDTH // 2 + 160, 600))
        screen.blit(next_level_img, next_level_rect)
    

        time_font = pygame.font.Font('freesansbold.ttf', 64)
        time_text = time_font.render(f'Time: {final_time_string}', True, BLACK)
    # Position the title at the top-center
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 300))

        screen.blit(time_text, time_rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
             # or return some value to handle closing
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # Get the current mouse position
                if menu_rect.collidepoint(pos):
                    return 'starting'
                if next_level_rect.collidepoint(pos):
                    return 'levels'





def ingame():
    global final_score
    global current_time
    final_score = final_score + score_total(player2) + score_total(player1)


    k1 = high(player1,trapeze_list)
    
    if k1 == 1:
        player1.rect.y -= 10
        player1.change_y = 0
        player1.rect.y += 8
    elif k1 == 2:
        player1.rect.y += 10
        player1.change_y = 0
        player1.rect.y -= 8

    k2 = high(player2, trapeze_list)          
    if k2 == 1:
        player2.rect.y -= 10
        player2.change_y = 0
        player2.rect.y += 8
    elif k2 == 2:
        player2.rect.y += 10
        player2.change_y = 0
        player2.rect.y -= 8

    if not player1.guns:
        gun_hits = pygame.sprite.spritecollide(player1, all_gun_list, True)
        if gun_hits:
            player1.guns = True
            player1.timer = pygame.time.get_ticks()
    if not player2.guns:
        gun_hits = pygame.sprite.spritecollide(player2, all_gun_list, True)
        if gun_hits:
            player2.guns = True
            player2.timer = pygame.time.get_ticks()

    player1_drink_hit  = pygame.sprite.spritecollide(player1, all_drink_list, True)
    player2_drink_hit = pygame.sprite.spritecollide(player2, all_drink_list, True)
    if player1_drink_hit or player2_drink_hit:
        player1.change_color(BLUE)            
        player2.change_color(RED)




           # time.sleep(0.001)

    screen.blit(question_img,(1200,20))
    if current_map == 'level_one' or current_map == 'level_two' or current_map == 'level_three' or current_map == 'level_four' or current_map == 'level_five':  
        screen.blit(pause_img, (30, 20))



        font = pygame.font.Font('freesansbold.ttf',30)
        if player1.color == (255,0,0):
            text = font.render(f'Color : Red',True,RED)
        else:
            text = font.render(f'Color : Blue',True, BLUE)

        textRect = text.get_rect()
        textRect.center = ( 1280//2//2 + 50, 40)
        screen.blit(text, textRect)

        font = pygame.font.Font('freesansbold.ttf',30)
        if player1.color == (255,0,0):
            text = font.render(f'Color : Blue',True,BLUE)
        else:
             text = font.render(f'Color : Red',True,RED)

        textRect = text.get_rect()
        textRect.center = ((1280//2+1280)//2, 40)
        screen.blit(text, textRect)


        score(final_score)
        if player1.guns:
            screen.blit(red_gun_img, (200, 20))
            remaining_time = (player1.duration - (current_time - player1.timer)) / 1000
            timer_text = font.render(str(int(remaining_time)), True, RED)
            screen.blit(timer_text, (260, 35))
            if current_time - player1.timer > player1.duration:
                player1.guns = False
                player1.timer = None
            
        # Blit the timer text next to the gun icon:
            screen.blit(timer_text, (260, 35))
        else:
            screen.blit(no_gun_img, (200, 20))
        if player2.guns:
            screen.blit(blue_gun_img, (1080, 20))
            remaining_time = (player2.duration - (current_time - player2.timer)) / 1000
            timer_text = font.render(str(int(remaining_time)), True, BLUE)
            screen.blit(timer_text, (1140, 35))
            if current_time - player2.timer > player2.duration:
                player2.guns = False
                player2.timer = None
            screen.blit(timer_text, (1140, 35))
        else:
            screen.blit(no_gun_img, (1080, 20))


    
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        seconds = elapsed_time // 1000
        minutes = seconds // 60
        seconds %= 60    
        time_string = f"{minutes:02}:{seconds:02}"
        final_time_string = time_string

        # Render the timer text
        font = pygame.font.Font(None, 50)
        timer = font.render(time_string, True, WHITE)
        timer_rect = timer.get_rect(center=(SCREEN_WIDTH//2, 50))
        screen.blit(timer, timer_rect)


   # elif sc_map == [0]:
        #screen.blit(play_img, (30, 20))

    
    


    # end if
    
    # updating all of the objects
    all_sprite_list.update()
    for bullet in bullet_list:
        enemy_hits = pygame.sprite.spritecollide(bullet, all_enemy_list, False)
        if enemy_hits:
            bullet.kill()
            for enemy in enemy_hits:

                if enemy.life > 1:
                    enemy.life -= 1
                    print(enemy.life)
                else:
                    enemy.kill()
                    final_score += 10
            
        block_hits = pygame.sprite.spritecollide(bullet, wall_list, False)
        if block_hits:
            bullet.kill()
    all_sprite_list.draw(screen)
    #screen.blit(background_image, (0, 0))




def question_button():
    question_img = pygame.image.load('pictures/question_grey.png')
    question_img = pygame.transform.scale(question_img, (150, 150))
    question_rect = question_img.get_rect(center=(1200,100))
    screen.blit(question_img, question_rect)
    return question_rect

def back_button():
    back_img = pygame.image.load('pictures/back_button.png')
    back_img = pygame.transform.scale(back_img, (150, 150))
    back_rect = back_img.get_rect(center=(100,100))
    screen.blit(back_img, back_rect)
    return back_rect

    









                

                
                 
        

# creating the map

#def initial_map(first_m):
 #   create_map(first_m)
# end procedure


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

def score(current_score):
    font = pygame.font.Font('freesansbold.ttf',25)
    text = font.render(f'Score {current_score}',True,GREEN,BLUE)
    textRect = text.get_rect()
    textRect.center = (800, 50)
    #screen.blit(text, textRect)


def lose():
    global sc_map
    screen.fill(BLACK)
    font = pygame.font.Font('freesansbold.ttf',82)
    lose = font.render('You Lost!', True, WHITE,RED)
    loseRect = lose.get_rect()
    loseRect.center = (1280//2, 720//2)
    screen.blit(lose, loseRect)
    sc_map =[1]
    for i in all_enemy_list:
        all_enemy_list.remove(i)
    for coin in blue_coin_list:
        blue_coin_list.remove(coin)
    for coin in red_coin_list:
        red_coin_list.remove(coin)
def win():
    global sc_map
    screen.fill(WHITE)
    font = pygame.font.Font('freesansbold.ttf',82)
    win = font.render('You WIIIIN!', True, LIGHT_BLUE,BLUE)
    winRect = win.get_rect()
    winRect.center = (1280//2, 720//2)
    screen.blit(win, winRect)
    sc_map =[2]

# end procedure
    
def return_to_menu():
    return_font = pygame.font.Font('freesansbold.ttf',32)
    menu= return_font.render('Press the button R to restart the game!', True, WHITE,RED)
    menuRect = menu.get_rect()
    menuRect.center = (1280//2, 720//2 + 300)
    screen.blit(menu, menuRect)




# end procedure


def create_players(x,y,color):
    player = Player(x, y, color)
    player.walls = wall_list
    player.enemies = all_enemy_list
    player.portals = portal_list_spr
    all_sprite_list.add(player)

    return player
# end function
player1 = create_players(20,500,RED)
player2 = create_players(20,50,BLUE)



#setting up the clock
clock = pygame.time.Clock()
 

# drawinf the initial map
#initial_map(sc_map)

done = False
SCORE = 0
final_score = 0

pause_img = pygame.image.load('pictures/pause_button.png')
pause_img = pygame.transform.scale(pause_img, (50, 50))

question_img = pygame.image.load('pictures/question_mark.png')
question_img = pygame.transform.scale(question_img, (50,50))

red_gun_img = pygame.image.load('pictures/red_gun.png')
red_gun_img = pygame.transform.scale(red_gun_img, (50, 50))

blue_gun_img = pygame.image.load('pictures/blue_gun.png')
blue_gun_img = pygame.transform.scale(blue_gun_img, (50, 50))

no_gun_img = pygame.image.load('pictures/no_gun.png')
no_gun_img = pygame.transform.scale(no_gun_img, (50, 50))

play_img = pygame.image.load('pictures/play_button.png')
play_img = pygame.transform.scale(play_img, (50, 50))


#background_image = pygame.image.load("background.jpg").convert()
#background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
# the main loop





while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # the quit method
            
        # Creating the keys for player 1 and player 2     
        if current_map =='level_one' or current_map == 'level_two' or current_map == 'level_three' or current_map == 'level_four' or current_map == 'level_five':
            if event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_LEFT:
                    player1.go_left()
                elif event.key == pygame.K_RIGHT:
                    player1.go_right()
                elif event.key == pygame.K_UP:
                    player1.jump()

                if event.key == pygame.K_DOWN:
                    player1.shoot()

                if event.key == pygame.K_a:
                    player2.go_left()
                elif event.key == pygame.K_d:
                    player2.go_right()
                elif event.key == pygame.K_w:
                    player2.jump()
                if event.key == pygame.K_s:
                    player2.shoot()
            # end if   



            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player1.change_x < 0:
                    player1.stop()
                if event.key == pygame.K_RIGHT and player1.change_x > 0:
                    player1.stop()

                if event.key == pygame.K_a and player2.change_x < 0:
                    player2.stop()
                if event.key == pygame.K_d and player2.change_x > 0:
                    player2.stop()






    # end if
    screen.fill(GREEN)   

    live_map()
    
    # drawing everything




    # TIME
    if sc_map not in ([0], [1], [2]):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        seconds = elapsed_time // 1000
        minutes = seconds // 60
        seconds %= 60    
        time_string = f"{minutes:02}:{seconds:02}"

        # Render the timer text
        font = pygame.font.Font(None, 50)
        text = font.render(time_string, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 50))
        #screen.blit(text, text_rect)



    
    pygame.display.flip()
    # fliping the display
    clock.tick(60)
    
 

def quit():
    pygame.quit()
    # quiting the pygame


quit()

