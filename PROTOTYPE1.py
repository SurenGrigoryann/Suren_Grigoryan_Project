# importing all the necessary libraries
import pygame
import amaps
import details
import menu
import slides
import sys

# The dimensions of the screen held as constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

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


# classses
class Player(pygame.sprite.Sprite):

    # Constructor 
    def __init__(self, x, y, color):
        
        super().__init__()
        # height, width
        self.image = pygame.Surface([25,25])
        self.image.fill(color)
 
        # setting the positon 
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        # setting the color
        self.color = color
        # speed vectors
        self.change_x = 0
        self.change_y = 0

        # walls collisions
        self.walls = None


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


    # end procedure

    # movement procedure
    def go_left(self):
        self.change_x = -3
    # end procedure
    def go_right(self):
        self.change_x = 3
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

        # Move the player back to their original position
        self.rect.y -= 2

        # If the player is on the ground or touching a platform, allow jumping
        if len(walls_hit_list) > 0:
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



    
# end class

class Block(pygame.sprite.Sprite):
    # Creating a class block in which players cannot collide to
    # Constructor constructor
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




def create_players(x,y,color):
    player = Player(x,y,color)
    player.walls = wall_list
    all_sprite_list.add(player)
    return player

# end procedure

player1 = create_players(20,500,RED)
player2 = create_players(25,300,BLUE)     





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
                

            # end if
            x += 10
        # next j
        x = 0
        y += 10

    # next i
# end procedure


def check_die(player, lake_dict):
    # Check collisions with lakes of a different color
    for lake_color, lakes in lake_dict.items():
        # Only check lakes that are not the same color as the player
        if player.color != lake_color:
            for lake in lakes:
                # Use colliderect to check for collision between player and lake
                if player.rect.colliderect(lake.rect):
                    print('dead')
                
                # end if
            # next lake
        # end if
    # next lake_color, lakes
# end procedure






create_map(amaps.level_one)
# setting up the clock
clock = pygame.time.Clock()

# Initializing pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Seting the title of the window
pygame.display.set_caption('Twin to Win')

done = False

# the main loop for the game
while not done:
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

            elif event.key == pygame.K_a:
                player2.go_left()
            elif event.key == pygame.K_d:
                player2.go_right()
            elif event.key == pygame.K_w:
                player2.jump()

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

    # next event




    # filling the screen with a color
    screen.fill(GREEN)

    # check for both players, if they collide with wrong lakes
    check_die(player1,all_lakes_list)
    check_die(player2,all_lakes_list)


    # creating the map for level one


    # updating all the objects on the screen
    all_sprite_list.update()
    # drawing all the objects on the screen
    all_sprite_list.draw(screen)

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
