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



# all the needed images
images = {
    'no_gun': pygame.image.load('pictures/no_gun.png'),
    'red_gun' : pygame.image.load('pictures/red_gun.png'),
    'blue_gun': pygame.image.load('pictures/blue_gun.png'),
    'bullet': pygame.image.load('pictures/bullet.png'),
    'fast_enemy': pygame.image.load('pictures/fast_enemy.png'),
    'tank_enemy': pygame.image.load('pictures/Tank.png'),
    'spell': pygame.image.load('pictures/color_changin_spell.png'),
    'red_player': pygame.image.load('pictures/red_player.png'),
    'blue_player': pygame.image.load('pictures/blue_player.png')

}



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

 
        # setting the positon 
        self.rect = self.image.get_rect()
        # setting the position
        self.rect.y = y
        self.rect.x = x
        # setting the color
        self.color = color

        # speed vector
        self.change_x = 0
        self.change_y = 0

        # walls collisions
        self.walls = None

        # guns
        self.guns = False
        # time for the gun
        self.timer = False
        # 10 seconds of duration for the gun
        self.duration = 10000
        
        # settting up the previous direction.
        # 1 will represent right -1 will represnt left
        self.previous_direction = 1


        # setting the color as constant that will never be changed
        self.original_color = color
        # setting up the color duration timer as 10 seconds
        self.color_duration = 10000
        # setting up the color timer
        self.color_timer = None



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
                    self.image = pygame.transform.scale(images['red_player'], (25, 35))
                elif self.color == BLUE:
                    self.image = pygame.transform.scale(images['blue_player'], (25, 35))
                
                # Reset the color timer to None (stops tracking until next change)
                self.color_timer = None




    # end procedure

    # movement procedure
    def go_left(self):
        self.previous_direction = -1
        self.change_x = -3
    # end procedure
    def go_right(self):
        self.previous_direction = 1
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
                self.image = pygame.transform.scale(images['red_player'], (25, 35))

            # If the color is BLUE, use the blue player image
            elif self.color == BLUE:
                self.image = pygame.transform.scale(images['blue_player'], (25, 35))
            # end if
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

class Gun(pygame.sprite.Sprite):
    # creating a gun class. Players will be able to collect those
    # Cosntructor function
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




def create_players(x,y,color):
    player = Player(x,y,color)
    player.walls = wall_list
    all_sprite_list.add(player)
    return player

# end procedure

player1 = create_players(25,400,RED)
player2 = create_players(20,500,BLUE)     





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

            # end if
            x += 10
        # next j
        x = 0
        y += 10

    # next i
# end procedure


def check_die(player, lake_dict, enemies):
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

    # Check collisions with the enemies
    for enemy in enemies:
        # Use colliderect to check for collision between player and enemy
        if player.rect.colliderect(enemy.rect):
            print('dead by enemy')
        # end if
    # next enemy
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


start_time = pygame.time.get_ticks()

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
    check_die(player1,all_lakes_list, all_enemy_list)
    check_die(player2,all_lakes_list, all_enemy_list)

    # checking any collisions between the players and the spells
    player1_spell_hit  = pygame.sprite.spritecollide(player1, all_spell_list, True)
    player2_spell_hit = pygame.sprite.spritecollide(player2, all_spell_list, True)
    # if there are any call the change_color for both players 
    if player1_spell_hit or player2_spell_hit:
        player1.change_color(BLUE)            
        player2.change_color(RED)
    # end if


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