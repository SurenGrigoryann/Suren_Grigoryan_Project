# importing all the necessary libraries
import pygame
import amaps
import maps
import adetails
import amenu
import aslides
import sys


# colors

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
CYAN = (0,255,255)

# setting up the clock
clock = pygame.time.Clock()


# The dimensions of the screen held as constans
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# all the needed images
images = {
    'no_gun': pygame.image.load('pictures/no_gun.png'),
    'red_gun' : pygame.image.load('pictures/red_gun.png'),
    'blue_gun': pygame.image.load('pictures/blue_gun.png'),
    'bullet': pygame.image.load('pictures/bullet.png'),
    'fast_enemy': pygame.image.load('pictures/fast.png'),
    'tank_enemy': pygame.image.load('pictures/Tank.png'),
    'spell': pygame.image.load('pictures/color_changin_spell.png'),
    'red_player': pygame.image.load('pictures/red_player.png'),
    'blue_player': pygame.image.load('pictures/blue_player.png'),
    'red_door': pygame.image.load('pictures/red_door.png'),
    'blue_door': pygame.image.load('pictures/blue_door.png'),
    'menu_button': pygame.image.load('pictures/menu_button.png'),
    'next_level_button': pygame.image.load('pictures/next_level.png'),
    'restart_the_level_button': pygame.image.load('pictures/restart_the_level.png'),
    'losing_screen' : pygame.image.load('pictures/lost.png'),
    'pause_button': pygame.image.load('pictures/pause_button.png'),
    'back_button': pygame.image.load('pictures/back_button.png'),
    'lift_fan': pygame.image.load('pictures/lift_fan.png'),
    'purple_portal': pygame.image.load('pictures/purple_portal.png'),
    'purple_portal_opener': pygame.image.load('pictures/purple_portal_opener.png'),
    'orange_portal': pygame.image.load('pictures/orange_portal.png'),
    'orange_portal_opener': pygame.image.load('pictures/orange_portal_opener.png'),
    'cyan_portal': pygame.image.load('pictures/cyan_portal.png'),
    'cyan_portal_opener': pygame.image.load('pictures/cyan_portal_opener.png'),
    'brown_portal': pygame.image.load('pictures/brown_portal.png'),
    'brown_portal_opener': pygame.image.load('pictures/brown_portal_opener.png')
    

}






# defining a list that will contain all the objects
all_sprite_list = pygame.sprite.Group()

# setting all the other lists
wall_list = pygame.sprite.Group()

# setting the lake groups
red_lake_list = pygame.sprite.Group()
blue_lake_list = pygame.sprite.Group()
black_lake_list = pygame.sprite.Group()

# setting the dictionary for all lakes
all_lakes_list = {RED: [], BLUE: [], BLACK: []}

# setting up the gun list
all_gun_list = pygame.sprite.Group()

# settinp up the bullet list
bullet_list = pygame.sprite.Group()

# setting up the enemy list
all_enemy_list = pygame.sprite.Group()

# setting up the spell list
all_spell_list = pygame.sprite.Group()

#creating a door dictionary
door_list = {'red': [], 'blue': []}

# creating a fan list
lift_fan_list = pygame.sprite.Group()


# creating a sprite group to hold all portal sprites 
portal_list_spr = pygame.sprite.Group()
# creating a dictionary to organize portals by color
portal_list = {'purple': [], 'cyan': [], 'orange': [], 'brown': []}
# creating a sprite group to hold all portal opener sprites
portal_opener_list_spr = pygame.sprite.Group()
# creating a dictionary to organize portal openers by color
portal_opener_list = {'purple': [], 'cyan': [], 'orange': [], 'brown': []}

def delete_map():
    global all_sprite_list, wall_list, red_lake_list, blue_lake_list, black_lake_list
    global all_lakes_list, all_gun_list, bullet_list, all_enemy_list, door_list, lift_fan_list
    global portal_list_spr, portal_list, portal_opener_list, portal_opener_list_spr
    # clearing all the sprites
    all_sprite_list.empty()
    wall_list.empty()
    red_lake_list.empty()
    blue_lake_list.empty()
    black_lake_list.empty()
    all_lakes_list[RED].clear()
    all_lakes_list[BLUE].clear()
    all_lakes_list[BLACK].clear()
    all_gun_list.empty()
    bullet_list.empty()
    all_enemy_list.empty()
    all_spell_list.empty()
    door_list['red'].clear()
    door_list['blue'].clear()
    lift_fan_list.empty()
    portal_list_spr.empty()
    portal_opener_list_spr.empty()
    portal_list['brown'].clear()
    portal_list['orange'].clear()
    portal_list['purple'].clear()
    portal_list['cyan'].clear()
    portal_opener_list['brown'].clear()
    portal_opener_list['orange'].clear()
    portal_opener_list['purple'].clear()
    portal_opener_list['cyan'].clear()
# end procedure


class Stack:
     # defining the stack
    def __init__(self):
        self.items = []
    # push procedure
    def push(self, item):
        self.items.append(item)
    # end procedure

    # pop function
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("pop from empty stack")
        # end if
    # end function

    # peek function
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("peek from empty stack")
        # end if
    # end function

    # checking if the stack is empty
    def is_empty(self):
        return len(self.items) == 0
    # end function
    
    # checking the size of the stack
    def size(self):
        return len(self.items)
    # end function
# end class








# classses
class Player(pygame.sprite.Sprite):

    # Constructor 
    def __init__(self, x, y, color):
        
        super().__init__()
        # height, width
        self.color = color
        if self.color == RED:
            self.image = pygame.transform.scale(images['red_player'], (25, 35))
        elif self.color == BLUE:
            self.image = pygame.transform.scale(images['blue_player'], (25, 35))

        self.image_right = self.image  # original image facing right
        self.image_left = pygame.transform.flip(self.image, True, False)  # flipped image for left movement

 
        # setting the positon 
        self.rect = self.image.get_rect()
        # setting the position
        self.rect.y = y
        self.rect.x = x
        # setting the color
        self.color = color
        # setting the color as constant that will never be changed
        self.original_color = color
        # setting up the color duration timer as 10 seconds
        self.color_duration = 10000

        # speed vector
        self.change_x = 0
        self.change_y = 0

        # walls collisions
        self.walls = None

        # portal collisions
        self.portals = None

        # guns
        self.guns = False
        # time for the gun
        self.timer = False
        # 10 seconds of duration for the gun
        self.duration = 10000
        
        # settting up the previous direction.
        # 1 will represent right -1 will represnt left
        self.previous_direction = 1

        # setting up the color timer
        self.color_timer = None

        # setting up life
        self.life = 1

    # end constructor

    def update(self):
        # calculating gravitiy
        self.calc_grav()
        # updating player's position
        self.rect.x += self.change_x
        

        # Checking if we hit anything horizontally
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)

        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the wall and the same if we are moving left
            
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # do the same for left
                self.rect.left = block.rect.right
                # checking for collisions of the portals and players

        if self.portals is not None:
            portal_hit_list = pygame.sprite.spritecollide(self, self.portals, False)
        else:
            portal_hit_list = []
        # end if
        for portal in portal_hit_list:
 
            # Handle horizontal collisions
            # If moving right, place the player's right side next to the portal's left side
            if self.change_x > 0:
                self.rect.right = portal.rect.left
            # same for the opposite    
            elif self.change_x < 0:
                self.rect.left = portal.rect.right
            # end if
        # next portal



            # end if
        # next block
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
 
            # If we are moving up, set our up side to the bottom side of
            # the wall and the same if we are moving down
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

        # checking for collisions of the portals and players
        if self.portals is not None:
            portal_hit_list = pygame.sprite.spritecollide(self, self.portals, False)
        else:
            portal_hit_list = []
        # end if
        
        for portal in portal_hit_list:
 
            # If we are moving up, set our up side to the bottom side of
            # the portal and the same if we are moving down
            if self.change_y > 0:
                self.rect.bottom = portal.rect.top
            elif self.change_y < 0:
                self.rect.top = portal.rect.bottom

            self.change_y = 0
            # end if
        # next portal
        
        # Check if the player's color has been changed from the original
        # and that the color timer has been started
        if self.color != self.original_color and self.color_timer is not None:
            
            # Get the current time in milliseconds
            current_time = pygame.time.get_ticks()
            
            # Check if the color duration has passed (e.g., 10 seconds)
            if current_time - self.color_timer >= self.color_duration:
                
                # Time is up: revert the player's color back to the original
                self.color = self.original_color

                # Update the player's image based on the original color
                if self.color == RED:
                    new_image = pygame.transform.scale(images['red_player'], (25, 35))
                elif self.color == BLUE:
                    new_image = pygame.transform.scale(images['blue_player'], (25, 35))
                # endif

                self.image_right = new_image
                self.image_left = pygame.transform.flip(new_image, True, False)
                # Reset current image based on current facing direction
                if self.previous_direction == -1:
                    self.image = self.image_left
                else:
                    self.image = self.image_right
                # Stop the color timer
                self.color_timer = None    
                # end if
            # end if
        # end if


    # end procedure

    # movement procedure
    def go_left(self):
        self.previous_direction = -1
        self.change_x = -3
        # Set image to the left-facing flipped version
        self.image = self.image_left

    # end procedure
    def go_right(self):
        self.previous_direction = 1
        self.change_x = 3
        # Set image to the original right-facing version
        self.image = self.image_right        

    # end procedure
    def stop(self):
        self.change_x = 0
    # end procedure
    def jump(self):
        # Temporarily move the player down by 2 pixels
        # This helps check if the player is standing on a block
        self.rect.y += 2

        # Check for collision with walls while slightly lower
        walls_hit_list = pygame.sprite.spritecollide(self, self.walls, False)

        # Check for collision with portals while slightly lower
        if self.portals is not None:
             portals_hit_list = pygame.sprite.spritecollide(self, self.portals, False)
        else:
            portals_hit_list = []
        # end if

        # make a single platform list
        platform_hit_list = walls_hit_list + portals_hit_list

        # Move the player back to their original position
        self.rect.y -= 2

        # If the player is touching a platform, allow jumping
        if len(platform_hit_list) > 0:
            # Apply an upward accelaration to simulate a jump
            self.change_y = -6.5
        # end if
    # end procedure

    def calc_grav(self):
        # checking if it is in the air or not
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .25
        # end if
    # end procedure

    def shoot(self):
        # Create a bullet based on the direction the player is facing
        if self.previous_direction == 1:
            # Facing right
            bullet = Bullet(self.rect.x, self.rect.y, "right")
        elif self.previous_direction == -1:
            # Facing left
            bullet = Bullet(self.rect.x, self.rect.y, "left")
        else:
            # Default to right if direction is undefined
            bullet = Bullet(self.rect.x, self.rect.y, "right")
        # end if

        # Add the bullet to the bullet group for individual handling
        bullet_list.add(bullet)

        # Add the bullet to the main sprite group so it gets updated and drawn
        all_sprite_list.add(bullet)
    # end procedure

    def change_color(self, changing_color):
        # Check if the new color is different from the current color
        if self.color != changing_color:
            # Start the color change timer by recording the current time in milliseconds
            self.color_timer = pygame.time.get_ticks()

            # Update the player's color to the new one
            self.color = changing_color

            # Update the player's image to match the new color
            # If the color is RED, use the red player image
            if self.color == RED:
                new_image = pygame.transform.scale(images['red_player'], (25, 35))

            # If the color is BLUE, use the blue player image
            elif self.color == BLUE:
                new_image = pygame.transform.scale(images['blue_player'], (25, 35))
            # end if
            self.image_right = new_image
            self.image_left = pygame.transform.flip(new_image, True, False)

            # Set the current image based on the player's current facing direction
            if self.previous_direction == -1:
                self.image = self.image_left
            else:
                self.image = self.image_right
            # end if
    # end procedure

 
# end class


class Block(pygame.sprite.Sprite):
    # Creating a class block in which players cannot collide to
    # Constructor 
    def __init__(self, x, y):

        super().__init__()
 
        # Making a dark green block with 10 heigth and 10 width from which we will build our walls
        self.image = pygame.Surface([10,10])
        self.image.fill(DARK_GREEN)
 
        # set positions
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    # end constructor
# end class 


class Lakes(pygame.sprite.Sprite):
    # creating a class lakes. Red player can go through the red lake but not the blue lake. The opposite for the Blue player.
    # constructor
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


class Gun(pygame.sprite.Sprite):
    # creating a gun class. Players will be able to collect those
    # constructor
    def __init__(self,x,y):
        super().__init__()

        self.image = pygame.transform.scale(images['no_gun'], (40,30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    # end procedure
# end class
    
class Bullet(pygame.sprite.Sprite):
    # creating a bullet class
    # Constructor
    def __init__(self,x,y, direction):
        super().__init__()
        
        self.image = pygame.transform.scale(images['bullet'], (10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        if self.direction == "right":
            self.speed_x = 5
        elif direction == "left":
            self.flipped_image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.flipped_image, (10, 10))
            self.speed_x = -5
        else:
            self.speed_x = 0
        self.speed_y = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # end if
    # end constructor
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH:
            self.kill()
        # end if
    # end procedure
# end class


class Enemy(pygame.sprite.Sprite):
    # creating a enemy class
    # Constructor
    def __init__(self,x,y,type):
        super().__init__()
        
            
        self.type = type
        self.life = 0
        # depending on the give type, enemies will have different dimensions, health and speed
        if self.type == "Fast":
            self.length = 45
            self.width = 40
            self.life = 5
            self.speed = 2
            self.image = pygame.transform.scale(images['fast_enemy'], (self.width, self.length))

        elif self.type == "Tank":
            self.length = 60
            self.width = 50
            self.life = 10
            self.speed = 0.75
            self.image = pygame.transform.scale(images['tank_enemy'], (self.width, self.length))
        # end if

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.x = x
        self.y = y
    # end constructor
    def attack(self, player):
        # checking whether the player's y coordinate is within the enemy's 'attack zone'
        if not (player.rect.y <= self.rect.y + self.length and player.rect.y > self.rect.y - 25):
            return  # if player is not vertically in the range, then do nothing: skip the rest of the code
        
        # end if

        # checking whether the player is on the left or right side of the enemy   
        if player.rect.x >= self.rect.x:
            # player is on the right side
            if self.type == "Tank" and player.rect.x <= self.x + 160:
                # Tank enemy: if the player is within 160 pixels to the right of its original x (self.x)
                # then set the normal tank image and move right slowly
                self.image = pygame.transform.scale(images['tank_enemy'], (self.width, self.length))
                self.rect.x += 0.75  # move right at a slow speed
            elif self.type == "Fast" and player.rect.x <= self.x + 200:
                # Fast enemy: if the player is within 200 pixels to the right,
                # then set the normal fast enemy image and move right fast
                self.image = pygame.transform.scale(images['fast_enemy'], (40, 45))
                self.rect.x += 2  # move right at a fas speed
            # end if
        else:
            # player is on the left side
            if self.type == "Tank" and player.rect.x >= self.x - 160:
                # Tank enemy: if the player is within 160 pixels to the left,
                # then flip the tank image horizontally, scale it, and move left slowly.
                self.image = pygame.transform.scale(pygame.transform.flip(images['tank_enemy'], True, False), (50, 60))
                self.rect.x -= 0.75  # Move left at a slow speed
            elif self.type == "Fast" and player.rect.x >= self.x - 200:
                # Fast enemy: if the player is within 200 pixels to the left,
                # then flip the fast enemy image horizontally, scale it, and move left faster.
                self.image = pygame.transform.scale(pygame.transform.flip(images['fast_enemy'], True, False), (40, 45))
                self.rect.x -= 2  # move left at a fast speed
            # end if
        # end if
    # end method
# end class



class Spell(pygame.sprite.Sprite):
    # creating a spell class
    # Constructor
    def __init__(self,x,y):
        super().__init__()
        
        self.image = pygame.transform.scale(images['spell'], (35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    # end constructor
# end class


class Door(pygame.sprite.Sprite):
    # creating a door class
    # Constructor
    def __init__(self,x,y,color):
        super().__init__()

        self.color = color
        if self.color == LIGHT_RED:
            self.image = pygame.transform.scale(images['red_door'], (35, 50))
        elif self.color == LIGHT_BLUE:
            self.image = pygame.transform.scale(images['blue_door'], (35, 50))
        # end if
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    # end constructor

    def update_door(self, player):
        # returns true if there is collision
        return self.rect.colliderect(player.rect)
    # end function
# end class

class LiftFan(pygame.sprite.Sprite):
    # Creating a fan class that gradually lifts players upward.
    # constructor
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(images['lift_fan'], (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # parameters for the lift procedure
        self.lift_margin = 100        
        self.upward_acceleration = 2  
        self.max_upward_speed = -10   
    # end constructor
    def high(self, player):
        # If the player is standing on the fan
        if self.rect.colliderect(player.rect):
            target_y = self.rect.top - self.lift_margin  # the maximum height

            # If player is not on the maximum height, it pushes the player higher until maximum is reached
            if player.rect.top > target_y:
                player.change_y -= self.upward_acceleration  # Push the player further each time

                # Don't go too fast
                if player.change_y < self.max_upward_speed:
                    player.change_y = self.max_upward_speed
                # end if
            # end if
        # end if
    # end procedure
# end class

class Portal_opener(pygame.sprite.Sprite):
    # creating a portal opener class
    # constructor
    def __init__(self,x,y,color):
        super().__init__()
        self.color = color
        if self.color == PURPLE:
            self.image = pygame.transform.scale(images['purple_portal_opener'], (20, 10))
        elif self.color == ORANGE:
            self.image = pygame.transform.scale(images['orange_portal_opener'], (20, 10))
        elif self.color == CYAN:
            self.image = pygame.transform.scale(images['cyan_portal_opener'], (20, 10))
        elif self.color == BROWN:
            self.image = pygame.transform.scale(images['brown_portal_opener'], (20, 10))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # end constructor
# end class


def collisions_portal_opener(player, portal_opener):
    return ((portal_opener.rect.x - 5) <= player.rect.x <= (portal_opener.rect.x + 5) and
        (portal_opener.rect.y - 25) <= player.rect.y <= (portal_opener.rect.y + 25))
# end procedure


class Portal(pygame.sprite.Sprite):
    # creating portal class
    # constructor
    def __init__(self,x,y,color):
        super().__init__()
        self.color = color
        if self.color == PURPLE:
            self.image = pygame.transform.scale(images['purple_portal'], (20, 10))
        elif self.color == ORANGE:
            self.image = pygame.transform.scale(images['orange_portal'], (20, 10))
        elif self.color == CYAN:
            self.image = pygame.transform.scale(images['cyan_portal'], (20, 10))
        elif self.color == BROWN:
            self.image = pygame.transform.scale(images['brown_portal'], (20, 10))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


        # Store position values for future use
        self.x1 = x
        self.y1 = y 
        self.x2 = x + 110
        self.x3 = x - 300
        self.y2 = y + 110
        self.y3 = y - 110
    # end constructor
    def open_portal(self, portal_opener, p1, p2, direction):
        
        # if there is no collision it will not return anything, and none of the portals will move
        if not (collisions_portal_opener(p1, portal_opener) or collisions_portal_opener(p2, portal_opener)):
            # if the portal is not in its initial position, while there is no collision 
            # between the player and the portal move it back to the initial positon
            if self.rect.x > self.x1:
                self.rect.x -= 1.25
            elif self.rect.x < self.x1:
                self.rect.x += 1.25
            if self.rect.y > self.y1:
                self.rect.y -= 1.25
            elif self.rect.y < self.y1:
                self.rect.y += 1.25
            # end if
            return
        # end if

        # if there is collision, it will check the direction and depending on that
        # it will change the coordiantes of the portals
        if direction == "down":
            if self.rect.y < self.y2:
                # checks whether it is at its maximum distance.
                self.rect.y += 1.25  # move downward if it is not
            # Once self.rect.y reaches self.y2, no further movement occurs.

        elif direction == "up":
            # checks whether it is at its maximum distance.
            if self.rect.y > self.y3:
                self.rect.y -= 1.25  # move upward if it is not
            # Once self.rect.y reaches self.y3, no further movement occurs.

        # same works for x coordinares
        elif direction == "left":
            # checks whether it is at its maximum distance.
            if self.rect.x > self.x3:
                self.rect.x -= 1.25  # move left if it is not
            # Once self.rect.x reaches self.x3, no further movement occurs.
        elif direction == "right":
            # checks whether it is at its maximum distance.
            if self.rect.x < self.x2: # move right if it is not
                self.rect.x += 1.25
            # Once self.rect.x reaches self.x2, no further movement occurs.  
    # end constructor
# end class


def create_players(x,y,color):
    global all_sprite_list
    global wall_list
    global portal_list_spr
    player = Player(x,y,color)
    player.walls = wall_list
    player.portals = portal_list_spr
    all_sprite_list.add(player)
    return player
# end procedure

player1 = create_players(25,300,RED)
player2 = create_players(20,600,BLUE)     

def check_die(player, lake_dict, enemies):
    # Check collisions with lakes of a different color
    for lake_color, lakes in lake_dict.items():
        # Only check lakes that are not the same color as the player
        if player.color != lake_color:
            for lake in lakes: 
                # Use colliderect to check for collision between player and lake
                if player.rect.colliderect(lake.rect):
                    player.life -= 1
                # end if
            # next lake
        # end if
    # next lake_color, lakes

    # Check collisions with the enemies
    for enemy in enemies:
        # Use colliderect to check for collision between player and enemy
        if player.rect.colliderect(enemy.rect):
            player.life -= 1
        # end if
    # next enemy
# end procedure






start_time = pygame.time.get_ticks()







# Initializing pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Seting the title of the window
pygame.display.set_caption('Twin to Win')


def create_map(map):
    x = 0 
    y = 0
    for i in map:
        for j in i:
            if j == 1:
                # creating the block objects and adding them to the correct groups they belong
                wall = Block(x, y)
                wall_list.add(wall)
                all_sprite_list.add(wall)
            
            elif j == 2:
                # creating blue lakes
                blue_lake = Lakes(x, y,LIGHT_BLUE)
                blue_lake_list.add(blue_lake)    
                all_sprite_list.add(blue_lake)
                all_lakes_list[BLUE].append(blue_lake)

            elif j == 3:
                # creating red lakes
                red_lake = Lakes(x, y,LIGHT_RED)
                red_lake_list.add(red_lake)    
                all_sprite_list.add(red_lake)
                all_lakes_list[RED].append(red_lake)

            elif j == 7:
                # creating black lakes
                black_lake = Lakes(x, y,BLACK)
                black_lake_list.add(black_lake)    
                all_sprite_list.add(black_lake)
                all_lakes_list[BLACK].append(black_lake)
            elif j == 'G':
                # creating gun objects
                gun = Gun(x,y)
                all_gun_list.add(gun)
                all_sprite_list.add(gun)
                
            elif j == 'T':
                # creating tank enemy
                Tank_enemy = Enemy(x,y, 'Tank')
                all_enemy_list.add(Tank_enemy)
                all_sprite_list.add(Tank_enemy)
            elif j == 'F':
                # creating fast enemy
                fast_enemy = Enemy(x,y, 'Fast')
                all_enemy_list.add(fast_enemy)
                all_sprite_list.add(fast_enemy)
            elif j == 's':
                # creating color changing spells
                spell = Spell(x,y)
                all_spell_list.add(spell)
                all_sprite_list.add(spell)
            elif j == 5:
                # creating the blue door
                blue_door = Door(x,y,LIGHT_BLUE)
                door_list['blue'].append(blue_door)    
                all_sprite_list.add(blue_door)
            elif j == 6:
                # creating the red door
                red_door = Door(x,y,LIGHT_RED)
                door_list['red'].append(red_door)
                all_sprite_list.add(red_door)
            elif j == 4:
                # creating the fan
                fan = LiftFan(x,y)
                lift_fan_list.add(fan)
                all_sprite_list.add(fan)
            elif j == 'p':
                # creating purple portal
                purple_portal = Portal(x,y,PURPLE)
                portal_list_spr.add(purple_portal)
                portal_list['purple'].append(purple_portal) 
                all_sprite_list.add(purple_portal)
            elif j == 'P':
                # creating purple portal opener
                purple_portal_opener = Portal_opener(x,y,PURPLE)
                portal_opener_list_spr.add(purple_portal_opener)
                portal_opener_list['purple'].append(purple_portal_opener) 
                all_sprite_list.add(purple_portal_opener)                    
            elif j == 'b':
                # creating brown portal
                brown_portal = Portal(x,y, BROWN)
                portal_list_spr.add(brown_portal)
                portal_list['brown'].append(brown_portal) 
                all_sprite_list.add(brown_portal)
            elif j == 'B':
                # creating brown portal opener
                brown_portal_opener = Portal_opener(x,y,BROWN)
                portal_opener_list_spr.add(brown_portal_opener)
                portal_opener_list['brown'].append(brown_portal_opener) 
                all_sprite_list.add(brown_portal_opener)    
            elif j == 'o':
                # creating orange portal
                orange_portal = Portal(x,y,ORANGE)
                portal_list_spr.add(orange_portal)
                portal_list['orange'].append(orange_portal) 
                all_sprite_list.add(orange_portal)
            elif j == 'O':
                # creating orange portal opener
                orange_portal_opener = Portal_opener(x,y,ORANGE)
                portal_opener_list_spr.add(orange_portal_opener)
                portal_opener_list['orange'].append(orange_portal_opener) 
                all_sprite_list.add(orange_portal_opener)   
            elif j == 'c':
                # creating cyan portal
                cyan_portal = Portal(x,y,CYAN)
                portal_list_spr.add(cyan_portal)
                portal_list['cyan'].append(cyan_portal) 
                all_sprite_list.add(cyan_portal)
            elif j == 'C':
                # creating cyan portal opener
                cyan_portal_opener = Portal_opener(x,y,CYAN)
                portal_opener_list_spr.add(cyan_portal_opener)
                portal_opener_list['cyan'].append(cyan_portal_opener) 
                all_sprite_list.add(cyan_portal_opener) 
            # end if
            x += 10
        # next j
        x = 0
        y += 10

    # next i
# end procedure
        




# creating the map for level one
create_map(amaps.level_one)


current_map = 'level_one'
previous_map = Stack()


def live_map():
    global current_map
    if current_map == 'level_one':

        # check if the the door_list is not empty and check if the lists under 'red' and 'blue' are not empty as well
        if door_list['red'] and len(door_list['red']) >= 1 and door_list['blue'] and len(door_list['blue']) >= 1:
            # check if both players are next to their own doors
            if ((door_list['red'][0].update_door(player1) and player1.color == RED) and 
                (door_list['blue'][0].update_door(player2) and player2.color == BLUE)
                or
                ((door_list['red'][0].update_door(player2) and player2.color == RED) and 
                (door_list['blue'][0].update_door(player1) and player1.color == BLUE))                                                                   
                                                                                        
                ):    
                previous_map.push(current_map)
                current_map = 'winning'
            # end if
        # end if

        # Check if players have collided with lakes or enemies and reduce life if necessary
        check_die(player1, all_lakes_list, all_enemy_list)
        check_die(player2, all_lakes_list, all_enemy_list)

        # If either player has no remaining life, switch to the losing screen
        if player1.life <= 0 or player2.life <= 0:
            previous_map.push(current_map)
            current_map = 'losing'
        # end if
        ingame()

    elif current_map == 'losing':
        delete_map()
        lost_map()
    elif current_map == 'winning':
        delete_map()
        winning()
    elif current_map == 'pause':
        current_map = pause()
    elif current_map == 'back':
        current_map = previous_map.pop()

    # end if
# end procedure





def ingame():
    global current_time
    global all_lakes_list
    global all_spell_list
    global all_sprite_list
    global all_enemy_list
    global all_gun_list

    # Check if player 1 does not currently have a gun
    if not player1.guns:
        # Check for collision with any gun object, and remove the gun if picked up
        gun_hits = pygame.sprite.spritecollide(player1, all_gun_list, True)
        if gun_hits:
            player1.guns = True  # Grant the player the ability to shootp
            player1.timer = pygame.time.get_ticks()
            # starting the timer
            print('player 1 took the gun')
        # end if
    # end if

    # Check if player 2 does not currently have a gun
    if not player2.guns:
        # Check for collision with any gun object, and remove the gun if picked up
        gun_hits = pygame.sprite.spritecollide(player2, all_gun_list, True)
        if gun_hits:
            player2.guns = True  # Grant the player the ability to shoot
            player2.timer = pygame.time.get_ticks()
            # starting the timer
            print('player 2 took the gun')
        # end if
    # end if


    # checking any collisions between the players and the spells
    player1_spell_hit  = pygame.sprite.spritecollide(player1, all_spell_list, True)
    player2_spell_hit = pygame.sprite.spritecollide(player2, all_spell_list, True)
    # if there are any call the change_color for both players 
    if player1_spell_hit or player2_spell_hit:
        player1.change_color(BLUE)            
        player2.change_color(RED)
    # end if


    # Set the font 
    font = pygame.font.Font('freesansbold.ttf', 30)

    # Display player1's current color next to the red gun (left side)
    # Check if player1's color is RED
    if player1.color == (255, 0, 0):
        text = font.render('Color : Red', True, RED)
    else:
        # If not red, it must be blue
        text = font.render('Color : Blue', True, BLUE)

    # Position the text on the left side of the screen 
    textRect = text.get_rect()
    textRect.center = (1280 // 4 + 50, 40)  # Left half of the screen
    screen.blit(text, textRect)  # Draw the text

    # Repeat the same for player2 (right side)
    font = pygame.font.Font('freesansbold.ttf', 30)
    # Check if player1's color is red again — this might be a logic bug!
    # You probably meant to check player2's color here
    if player1.color == (255, 0, 0):
        text = font.render('Color : Blue', True, BLUE)
    else:
        text = font.render('Color : Red', True, RED)

    # Position the text on the right side of the screen 
    textRect = text.get_rect()
    textRect.center = ((1280 // 2 + 1280) // 2, 40)  # Right half of the screen
    screen.blit(text, textRect)  # Draw the text




    # display gun icon and timer for player 1
    if player1.guns:
        # if player 1 has a gun, display red gun
        red_gun = pygame.transform.scale(images['red_gun'], (50, 50))
        screen.blit(red_gun, (200, 20))

        # calculate remaining time before the gun disappears
        remaining_time = (player1.duration - (current_time - player1.timer)) / 1000

        # display the remaining time next to the gun icon
        timer_text = font.render(str(int(remaining_time)), True, RED)
        screen.blit(timer_text, (260, 35))

        # when the timer runs out remove the gun from player 1
        if current_time - player1.timer > player1.duration:
            player1.guns = False
            player1.timer = None
        # end if
    else:
        # if player 1 doesn't have a gun, display black gun
        no_gun = pygame.transform.scale(images['no_gun'], (50, 50))
        screen.blit(no_gun, (200, 20))
    #end if

    # display gun icon and timer for player 1
    if player2.guns:
        # if player 1 has a gun, display red gun
        blue_gun = pygame.transform.scale(images['blue_gun'], (50, 50))
        screen.blit(blue_gun, (1080, 20))

        # calculate remaining time before the gun disappears
        remaining_time = (player2.duration - (current_time - player2.timer)) / 1000

        # display the remaining time next to the gun icon
        timer_text = font.render(str(int(remaining_time)), True, BLUE)
        screen.blit(timer_text, (1140, 35))

        # If the timer runs out, remove the gun from player 2
        if current_time - player2.timer > player2.duration:
            player2.guns = False
            player2.timer = None
        # end if
    else:
        # if player 1 doesn't have a gun, display black gun
        no_gun = pygame.transform.scale(images['no_gun'], (50, 50))
        screen.blit(no_gun, (1080, 20))
    # end if
        
    # Get the current time in milliseconds since the game started
    current_time = pygame.time.get_ticks()

    # Calculate the elapsed time since the game started
    elapsed_time = current_time - start_time

    # Convert elapsed time to seconds and minutes
    seconds = elapsed_time // 1000
    minutes = seconds // 60
    seconds %= 60  # Keep seconds in the 0–59 range

    # Format the time as MM:SS
    time_string = f"{minutes:02}:{seconds:02}"
    final_time_string = time_string  # Store it for other use (e.g., end screen)

    # Render the timer text to display on the screen
    font = pygame.font.Font(None, 50)
    timer = font.render(time_string, True, WHITE)

    # Position the timer at the top center of the screen
    timer_rect = timer.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(timer, timer_rect)  # Draw the timer text on the screen


    # updating all the objects on the screen
    all_sprite_list.update()

    for bullet in bullet_list:
        # checking for collisions of the bullets with blocks
        block_hits = pygame.sprite.spritecollide(bullet, wall_list, False)
        if block_hits:
            # removing the bullets
            bullet.kill()
        # end if
        # checking the collisions of the bullets with enemies
        enemy_hits = pygame.sprite.spritecollide(bullet, all_enemy_list, False)
        if enemy_hits:
            # killing the bullet straight after it touches the enemy
            bullet.kill()
            for enemy in enemy_hits:
                if enemy.life > 1: 
                    enemy.life -= 1
                    print(enemy.life)
                else:
                    # killing enemy when it has 0 health
                    enemy.kill()
                    # removing it from all the groups
                    all_sprite_list.remove(enemy)
                    all_enemy_list.remove(enemy)
            # next enemy
        # end if
    # next bullet

    for enemy in all_enemy_list:
        enemy.attack(player1)
        enemy.attack(player2)
    # next enemy

    for fan in lift_fan_list:
        fan.high(player1)
        fan.high(player2)
    # next fan


    # Get purple portal opener if it exists
    if portal_opener_list['purple']:
        p_opener_purple = portal_opener_list['purple'][0]
    else:
        p_opener_purple = []
    # end if

    # Get brown portal opener if it exists
    if portal_opener_list['brown']:
        p_opener_brown = portal_opener_list['brown'][0]
    else:
        p_opener_brown = []
    # end if
    # Get orange portal opener if it exists
    if portal_opener_list['orange']:
        p_opener_orange = portal_opener_list['orange'][0]
    else:
        p_opener_orange = []
    # end if
    # Get cyan portal opener if it exists
    if portal_opener_list['cyan']:
        p_opener_cyan = portal_opener_list['cyan'][0]
    else:
        p_opener_cyan = []
    # end if
    # opening the portals
    # opening purple portals (move down)
    for portal in portal_list['purple']:
        portal.open_portal(p_opener_purple, player1, player2, "down")
    # next portal

    # opening brown portals (move up)
    for portal in portal_list['brown']:
        portal.open_portal(p_opener_brown, player1, player2, "up")
    # next portal

    # opening orange portals (move left)
    for portal in portal_list['orange']:
        portal.open_portal(p_opener_orange, player1, player2, "left")
    # next portal

    # Opening cyan portals (move right) 
    for portal in portal_list['cyan']:
        portal.open_portal(p_opener_cyan, player1, player2, "right")  
    # next portal

    # setting up the pause button
    pause_img = pygame.transform.scale(images['pause_button'], (50, 50))
    pause_rect = pause_img.get_rect(topleft=(30, 20))  # sets the top-left corner
    screen.blit(pause_img, pause_rect)


    # drawing all the objects on the screen
    all_sprite_list.draw(screen)



def winning():
    # overdrawing everything that was there before
    screen.fill(DARK_GRAY)
    while True:
        # Create a font object for the title with size 64
        title_font = pygame.font.Font('freesansbold.ttf', 64)
        title_text = title_font.render('Level Passed!', True, BLACK)
        # Get the rectangle for the text
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        # Draw  the text onto the screen
        screen.blit(title_text, title_rect)


        # get the menu image and transform in size
        menu_img = pygame.transform.scale(images['menu_button'], (300, 300))
        # Get the rectangle for the menu button
        menu_rect = menu_img.get_rect(center=(SCREEN_WIDTH // 2 - 160, 600))
        # draw the image onto the screen
        screen.blit(menu_img, menu_rect)

        # get the next level image and transform in size
        next_level_img = pygame.transform.scale(images['next_level_button'], (300, 300))
        # get the rectangle for the next level button
        next_level_rect = next_level_img.get_rect(center=(SCREEN_WIDTH // 2 + 160, 600))
        # draw the image onto the screen
        screen.blit(next_level_img, next_level_rect)

        # flipping the screen
        pygame.display.flip()
        # checking for quit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
# end procedure


def lost_map():
    screen.fill(DARK_GRAY)
    while True:
        # Create a font object for the title with size 64
        title_font = pygame.font.Font('freesansbold.ttf', 64)
        title_text = title_font.render('You lost!', True, BLACK)
        # Get the rectangle for the text
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        # Draw  the text onto the screen
        screen.blit(title_text, title_rect)


        # get the losing screen image and transform in size
        lost_img = pygame.transform.scale(images['losing_screen'], (300, 300))
        # Get the rectangle for the losing screen image 
        lost_rect = lost_img.get_rect(center=(SCREEN_WIDTH // 2, 350))
        # draw the image onto the screen
        screen.blit(lost_img, lost_rect)

        # get the menu image and transform in size
        menu_img = pygame.transform.scale(images['menu_button'], (300, 300))
        # Get the rectangle for the menu button
        menu_rect = menu_img.get_rect(center=(SCREEN_WIDTH // 2 - 160, 600))
        # draw the image onto the screen
        screen.blit(menu_img, menu_rect)


        # get the next level image and transform in size
        restart_the_level_img = pygame.transform.scale(images['restart_the_level_button'], (300, 300))
        # get the rectangle for the next level button
        restart_the_level_rect = restart_the_level_img.get_rect(center=(SCREEN_WIDTH // 2 + 160, 600))
        # draw the image onto the screen
        screen.blit(restart_the_level_img, restart_the_level_rect)

        # flipping the screen
        pygame.display.flip()
        # checking for quit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            # end if
        # next event
    # end while
# end procedure


def pause():
    global start_time
    screen.fill(DARK_GRAY)
    # Record the time when pause starts
    pause_start = pygame.time.get_ticks()

    while True:
        # Create a font object for the title with size 64
        title_font = pygame.font.Font('freesansbold.ttf', 64)
        title_text = title_font.render('Level paused!', True, BLACK)
        # Get the rectangle for the text
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        # Draw  the text onto the screen
        screen.blit(title_text, title_rect)

        # get the menu image and transform in size
        menu_img = pygame.transform.scale(images['menu_button'], (300, 300))
        # Get the rectangle for the menu button
        menu_rect = menu_img.get_rect(center=(SCREEN_WIDTH // 2 - 160, 600))
        # draw the image onto the screen
        screen.blit(menu_img, menu_rect)


        # get the next level image and transform in size
        restart_the_level_img = pygame.transform.scale(images['restart_the_level_button'], (300, 300))
        # get the rectangle for the next level button
        restart_the_level_rect = restart_the_level_img.get_rect(center=(SCREEN_WIDTH // 2 + 160, 600))
        # draw the image onto the screen
        screen.blit(restart_the_level_img, restart_the_level_rect)

        # fet the back button and transform in size
        back_img = pygame.transform.scale(images['back_button'], (150, 150))
        # get the rectangle for the back button
        back_rect = back_img.get_rect(center=(100,100))
        # draw the image onto the screen
        screen.blit(back_img, back_rect)

        # flipping the screen
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # Get the current mouse position
                if back_rect.collidepoint(pos):
                    # When leaving pause, calculate how long we were paused
                    pause_end = pygame.time.get_ticks()
                    paused_duration = pause_end - pause_start

                    # Adjust the global start_time so the level timer doesn't include pause time
                    start_time += paused_duration

                    # Also adjust the timers for gun power-ups and color change effects
                    # (This stops their countdown during pause)
                    if player1.guns and player1.timer is not None:
                        player1.timer += paused_duration
                    if player2.guns and player2.timer is not None:
                        player2.timer += paused_duration
                    if player1.color_timer is not None:
                        player1.color_timer += paused_duration
                    if player2.color_timer is not None:
                        player2.color_timer += paused_duration
                    return 'back'
            # end if
        # next event
    # end while
# end procedure


        


done = False

# the main loop for the game
while not done:
    # setting up the quit button
    # this will allow us to exit the game
    # when we press the x button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # checking the movements of the players    
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_LEFT:
                player1.go_left()
            elif event.key == pygame.K_RIGHT:
                player1.go_right()
            elif event.key == pygame.K_UP:
                    player1.jump()
            # end if
            if event.key == pygame.K_DOWN:
                if player1.guns:
                    player1.shoot()
            # end if

            elif event.key == pygame.K_a:
                player2.go_left()
            elif event.key == pygame.K_d:
                player2.go_right()
            elif event.key == pygame.K_w:
                player2.jump()
            # end if
            if event.key == pygame.K_s:
                if player2.guns:
                    player2.shoot()
            # end if   
        # end if

        # handling keyup cases, to stop the movements of the players
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player1.change_x < 0:
                player1.stop()
            elif event.key == pygame.K_RIGHT and player1.change_x > 0:
                player1.stop()

            elif event.key == pygame.K_a and player2.change_x < 0:
                player2.stop()
            elif event.key == pygame.K_d and player2.change_x > 0:
                player2.stop()
            # end if
        # end if
        # Check if an event is a mouse button press
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse click
            pos = pygame.mouse.get_pos()
            x, y = pos[0], pos[1]

            # Check if the mouse click is within the specified rectangular area (button zone)
            if (x > 30 and x < 80) and (y > 20 and y < 70):
                # If the current map is 'level_one', switch to the 'pause' screen
                if current_map == 'level_one':
                    previous_map.push(current_map)
                    current_map = 'pause'  # Change the state to pause
                # end if
            # end if
        # end if

                

    # next event

    # filling the screen with a color
    
    screen.fill(GREEN)

    # calling the main map
    live_map()

    # flipping the screen
    # this will update the screen, and show the changes made to the screen
    pygame.display.flip()

    clock.tick(60)
    # setting the frame rate to 60 fps


# end while




# defining the quit procedure, which will quit pygame and exit the program
def quit():
    pygame.quit()
    sys.exit()
# end procedure

quit()
# end main