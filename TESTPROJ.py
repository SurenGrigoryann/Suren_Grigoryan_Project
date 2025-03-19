# PROJECT.py
import pygame
import random
import maps
import details
import time
import sys
import menu
from menu import run_menu, change_level

# ------------------------
# COLORS
# ------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
RED = (255, 0, 0)
LIGHT_RED = (255, 144, 144)
LIGHT_BLUE = (135, 206, 235)
GREEN = (0, 255, 0)
DARK_GREEN = (1, 50, 22)
LIGHT_GREEN = (0, 130, 0)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)
BROWN = (139, 69, 19)
ORANGE = (255, 99, 7)

# ------------------------
# SCREEN DIMENSIONS
# ------------------------
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# ------------------------
# IMAGE ASSETS
# ------------------------
images = {
    'red_player': pygame.image.load('pictures/red_player.png').convert_alpha(),
    'blue_player': pygame.image.load('pictures/blue_player.png').convert_alpha(),
    'fast_enemy': pygame.image.load('pictures/fast_enemy.png').convert_alpha(),
    'tank_enemy': pygame.image.load('pictures/Tank.png').convert_alpha(),
    'red_door': pygame.image.load('pictures/red_door.jpg').convert(),
    'blue_door': pygame.image.load('pictures/blue_door.jpg').convert(),
    'background': pygame.transform.scale(pygame.image.load("pictures/background1.jpg").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT-80)),
    'block': pygame.image.load('pictures/block.jpg').convert(),
}

# ------------------------
# SPRITE CLASSES
# ------------------------
class Drink(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.color = color
        if self.color == LIGHT_RED:
            self.img = pygame.image.load('pictures/red_door.jpg')
        elif self.color == LIGHT_BLUE:
            self.img = pygame.image.load('pictures/blue_door.jpg')
        self.image = pygame.transform.scale(self.img, (35, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update_door(self, player):
        # Check if player is near enough to trigger door activation.
        if (player.rect.x <= self.rect.x + 20 and player.rect.x >= self.rect.x - 20) and (player.rect.y <= self.rect.y + 20 and player.rect.y >= self.rect.y - 20):
            return True
        else:
            return False

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x1 = x
        self.y1 = y 
        self.x2 = x 
        self.y2 = y + 110
        self.y3 = y - 110
        self.color = color
    
    def open_portal(self, portal_opener, p1, p2, direction):
        if direction == "down":
            if (self.y2 != self.rect.y) and (
               ((p1.rect.x <= portal_opener.rect.x + 15 and p1.rect.x >= portal_opener.rect.x - 15) and
                (p1.rect.y <= portal_opener.rect.y + 15 and p1.rect.y >= portal_opener.rect.y - 25))
                or
               ((p2.rect.x <= portal_opener.rect.x + 15 and p2.rect.x >= portal_opener.rect.x - 15) and
                (p2.rect.y <= portal_opener.rect.y + 15 and p2.rect.y >= portal_opener.rect.y - 25))
            ):
                self.rect.y += 1.25
            elif self.y1 != self.rect.y:
                self.rect.y -= 1.25

        elif direction == "up":
            if (self.y3 != self.rect.y) and (
               ((p1.rect.x <= portal_opener.rect.x + 15 and p1.rect.x >= portal_opener.rect.x - 15) and
                (p1.rect.y <= portal_opener.rect.y + 15 and p1.rect.y >= portal_opener.rect.y - 25))
                or
               ((p2.rect.x <= portal_opener.rect.x + 15 and p2.rect.x >= portal_opener.rect.x - 15) and
                (p2.rect.y <= portal_opener.rect.y + 15 and p2.rect.y >= portal_opener.rect.y - 25))
            ):
                self.rect.y -= 1.25
            elif self.y1 != self.rect.y:
                self.rect.y += 1.25

class Portal_opener(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.life = 0
        self.gun = None
        if self.type == "Fast":
            self.length = 45
            self.width = 40
            self.life = 5
            self.gun = "Short"
            self.image = pygame.transform.scale(images['fast_enemy'], (self.width, self.length))
        elif self.type == "Tank":
            self.length = 60
            self.width = 50
            self.life = 10
            self.gun = "Short"
            self.image = pygame.transform.scale(images['tank_enemy'], (self.width, self.length))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

    def attack(self, player):
        if self.type == "Tank":
            if (player.rect.y <= self.rect.y + self.length and player.rect.y > self.rect.y - 25) and (player.rect.x >= self.rect.x and player.rect.x <= self.x + 160):
                self.image = pygame.transform.scale(images['tank_enemy'], (self.width, self.length))
                self.rect.x += 0.75
            elif (player.rect.y <= self.rect.y + self.length and player.rect.y > self.rect.y - 25) and (player.rect.x <= self.rect.x and player.rect.x >= self.x - 160):
                self.flipped_image = pygame.transform.flip(self.image, True, False)
                self.image = pygame.transform.scale(self.flipped_image, (50, 60))
                self.rect.x -= 0.75
        elif self.type == "Fast":
            if (player.rect.y <= self.rect.y + self.length and player.rect.y > self.rect.y - 25) and (player.rect.x >= self.rect.x and player.rect.x <= self.x + 200):
                self.flipped_image = pygame.transform.flip(self.image, True, False)
                self.image = pygame.transform.scale(self.flipped_image, (40, 45))
                self.rect.x += 2
            elif (player.rect.y <= self.rect.y + self.length and player.rect.y > self.rect.y - 25) and (player.rect.x <= self.rect.x and player.rect.x >= self.x - 200):
                self.img = pygame.image.load('pictures/fast_enemy.png')
                self.image = pygame.transform.scale(self.img, (40, 45))
                self.rect.x -= 2

class Gun(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img = pygame.image.load('pictures/no_gun.png')
        self.image = pygame.transform.scale(self.img, (40, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        if self.direction == "right":
            self.speed_x = 5
        elif self.direction == "left":
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
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = 0
        self.change_y = 0
        self.enemies = None
        self.walls = None
        self.portals = None
        self.coins = None
        self.lakes = None
        self.guns = False
        self.timer = False
        self.duration = 10000  # milliseconds
        self.life = 1
        self.level = None

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
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
            if self.change_y > 0:
                self.rect.bottom = portal.rect.top
            elif self.change_y < 0:
                self.rect.top = portal.rect.bottom
            self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.25
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += 2
        walls_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        if self.portals is not None:
            portals_hit_list = pygame.sprite.spritecollide(self, self.portals, False)
        else:
            portals_hit_list = []
        platform_hit_list = walls_hit_list + portals_hit_list
        self.rect.y -= 2
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -6.5

    def go_left(self):
        if self.direction == "right" and self.previous_direction == 1:
            if self.color == RED:
                self.img = pygame.image.load('pictures/red_player.png')
            elif self.color == BLUE:
                self.img = pygame.image.load('pictures/blue_player.png')
            self.flipped_image = pygame.transform.flip(self.img, True, False)
            self.image = pygame.transform.scale(self.flipped_image, (25, 35))
            screen.blit(self.image, (self.rect.x, self.rect.y))
            self.direction = "left"
        self.previous_direction = -1
        self.change_x = -3

    def go_right(self):
        if self.direction == "left" and self.previous_direction == -1:
            if self.color == RED:
                self.img = pygame.image.load('pictures/red_player.png')
            elif self.color == BLUE:
                self.img = pygame.image.load('pictures/blue_player.png')
            self.image = pygame.transform.scale(self.img, (25, 35))
            screen.blit(self.image, (self.rect.x, self.rect.y))
            self.direction = "right"
        self.previous_direction = 1
        self.change_x = 3

    def stop(self):
        if self.change_x == 3:
            self.previous_direction = 1
        elif self.change_x == -3:
            self.previous_direction = -1
        self.change_x = 0

    def shoot(self):
        if self.guns:
            if self.previous_direction == 1:
                bullet = Bullet(self.rect.x, self.rect.y, "right")
                bullet_list.add(bullet)
                all_sprite_list.add(bullet)
            elif self.previous_direction == -1:
                bullet = Bullet(self.rect.x, self.rect.y, "left")
                bullet_list.add(bullet)
                all_sprite_list.add(bullet)

class Block(pygame.sprite.Sprite):
    image = None
    @classmethod
    def load_image(cls):
        cls.image = pygame.transform.scale(images['block'], (10, 10))
        
    def __init__(self, x, y):
        super().__init__()
        if Block.image is None:
            raise ValueError("Block image not loaded. Call Block.load_image() first.")
        self.image = Block.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Lakes(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
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
        self.rect.x = x
        self.rect.y = y

class Trapeze(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coins(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen_to_draw):
        if self.color == RED:
            red_coin = pygame.image.load('pictures/red_coin.png')
            red_coin_image = pygame.transform.scale(red_coin, (20, 20))
            screen_to_draw.blit(red_coin_image, (self.x, self.y))
        elif self.color == BLUE:
            blue_coin = pygame.image.load('pictures/blue_coin.png')
            blue_coin_image = pygame.transform.scale(blue_coin, (20, 20))
            screen_to_draw.blit(blue_coin_image, (self.x, self.y))

# ------------------------
# INITIALIZATION
# ------------------------
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Fboy and Wgirl')
Block.load_image()

# ------------------------
# LEVEL MANAGEMENT VARIABLES
# ------------------------
# Start the game at Level 1.
current_level = 1
sc_map = maps.level_one_test  # Level 1 map from your maps module.
sm = sc_map

# ------------------------
# SPRITE GROUPS AND GAME STATE SETUP FUNCTIONS
# ------------------------
def create_lists():
    global all_sprite_list, all_players_list, wall_list, red_lake_list, blue_lake_list, green_lake_list
    global all_lakes_list, trapeze_list, coins_list, red_coin_list, blue_coin_list
    global all_enemy_list, all_gun_list, bullet_list, portal_list_spr, portal_list
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
    bullet_list = pygame.sprite.Group()
    portal_list_spr = pygame.sprite.Group()
    portal_list = {'purple': [], 'yellow ': [], 'orange': [], 'black': [], 'brown': []}
    portal_opener_list_spr = pygame.sprite.Group()
    portal_opener_list = {'purple': [], 'yellow ': [], 'orange': [], 'black': [], 'brown': []}
    door_list_spr = pygame.sprite.Group()
    door_list = []

create_lists()

def create_map(map_data):
    x = 0
    y = 0
    for i in map_data:
        for j in i:
            if j == 1:
                wall = Block(x, y)
                wall_list.add(wall)
                all_sprite_list.add(wall)
            elif j == 3:
                red_lake = Lakes(x, y, LIGHT_RED)
                red_lake_list.add(red_lake)    
                all_sprite_list.add(red_lake)
                all_lakes_list[RED].append(red_lake)
            elif j == 2:
                blue_lake = Lakes(x, y, LIGHT_BLUE)
                blue_lake_list.add(blue_lake)    
                all_sprite_list.add(blue_lake)
                all_lakes_list[BLUE].append(blue_lake)
            elif j == 4:
                trapeze = Trapeze(x, y)
                trapeze_list.add(trapeze)
                all_sprite_list.add(trapeze)
            elif j == 5:
                blue_door = Door(x, y, LIGHT_BLUE)
                door_list_spr.add(blue_door)
                door_list.append(blue_door)
                all_sprite_list.add(blue_door)
            elif j == 6:
                red_door = Door(x, y, LIGHT_RED)
                door_list_spr.add(red_door)
                door_list.append(red_door)
                all_sprite_list.add(red_door)
            elif j == 7:
                green_lake = Lakes(x, y, LIGHT_GREEN)
                green_lake_list.add(green_lake)
                all_sprite_list.add(green_lake)
                all_lakes_list[LIGHT_GREEN].append(green_lake)
            elif j == 8:
                red_coin = Coins(x, y, RED)
                red_coin_list.add(red_coin)
                coins_list.add(red_coin)
            elif j == 9:
                blue_coin = Coins(x, y, BLUE)
                blue_coin_list.add(blue_coin)
                coins_list.add(blue_coin)
            elif j == 'p':
                purple_portal = Portal(x, y, PURPLE)
                portal_list_spr.add(purple_portal)
                portal_list['purple'].append(purple_portal)
                all_sprite_list.add(purple_portal)
            elif j == 'P':
                purple_portal_opener = Portal_opener(x, y, PURPLE)
                portal_opener_list_spr.add(purple_portal_opener)
                portal_opener_list['purple'].append(purple_portal_opener)
                all_sprite_list.add(purple_portal_opener)
            elif j == 'b':
                brown_portal = Portal(x, y, BROWN)
                portal_list_spr.add(brown_portal)
                portal_list['brown'].append(brown_portal)
                all_sprite_list.add(brown_portal)
            elif j == 'B':
                brown_portal_opener = Portal_opener(x, y, BROWN)
                portal_opener_list_spr.add(brown_portal_opener)
                portal_opener_list['brown'].append(brown_portal_opener)
                all_sprite_list.add(brown_portal_opener)
            elif j == 'o':
                orange_portal = Portal(x, y, ORANGE)
                portal_list_spr.add(orange_portal)
                portal_list['orange'].append(orange_portal)
                all_sprite_list.add(orange_portal)
            elif j == 'O':
                orange_portal_opener = Portal_opener(x, y, ORANGE)
                portal_opener_list_spr.add(orange_portal_opener)
                portal_opener_list['orange'].append(orange_portal_opener)
                all_sprite_list.add(orange_portal_opener)
            elif j == 'F':
                fast_enemy = Enemy(x, y, 'Fast')
                all_enemy_list.add(fast_enemy)
                all_sprite_list.add(fast_enemy)
            elif j == 'T':
                tank_enemy = Enemy(x, y, 'Tank')
                all_enemy_list.add(tank_enemy)
                all_sprite_list.add(tank_enemy)
            elif j == 'G':
                gun = Gun(x, y)
                all_gun_list.add(gun)
                all_sprite_list.add(gun)
            x += 10
        x = 0
        y += 10

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
    door_list.clear()

def check_die(player, lake_list, enemies):
    for key in lake_list:
        if player.color != key:
            for lake in lake_list[key]:
                if (player.rect.x + 24 >= lake.rect.x and player.rect.x - 9 <= lake.rect.x) and (player.rect.y + 34 >= lake.rect.y and player.rect.y - 14 <= lake.rect.y):
                    player.life -= 1
            for enemy in enemies:
                if (player.rect.x + 25 >= enemy.rect.x and player.rect.x <= enemy.rect.x) and (player.rect.y + 25 >= enemy.rect.y and player.rect.y - 15 <= enemy.rect.y):
                    player.life -= 1

def high(player, list_of_trapeze):
    for trapeze in list_of_trapeze:
        if (player.rect.x >= trapeze.rect.x - 10 and player.rect.x <= trapeze.rect.x + 10) and (player.rect.y <= trapeze.rect.y and player.rect.y > trapeze.rect.y - 200):
            return 1
        elif (player.rect.x >= trapeze.rect.x - 10 and player.rect.x <= trapeze.rect.x + 10) and player.rect.y == trapeze.rect.y - 250:
            return 2

def score_total(player):
    if player.color == BLUE:
        for coin in blue_coin_list:
            if (player.rect.x + 24 >= coin.x and player.rect.x - 9 <= coin.x) and (player.rect.y + 24 >= coin.y and player.rect.y - 9 <= coin.y):
                blue_coin_list.remove(coin)
                coins_list.remove(coin)
                return 1
    elif player.color == RED:
        for coin in red_coin_list:
            if (player.rect.x + 24 >= coin.x and player.rect.x - 9 <= coin.x) and (player.rect.y + 24 >= coin.y and player.rect.y - 9 <= coin.y):
                red_coin_list.remove(coin)
                coins_list.remove(coin)
                return 1
    return 0

def create_players(x, y, color):
    player = Player(x, y, color)
    player.walls = wall_list
    player.enemies = all_enemy_list
    player.portals = portal_list_spr
    all_sprite_list.add(player)
    return player

# ------------------------
# ON-SCREEN MESSAGES
# ------------------------
def menu_screen():
    screen.fill(WHITE)
    font = pygame.font.Font('freesansbold.ttf', 82)
    text = font.render('Menu', True, GREEN, BLUE)
    textRect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    font2 = pygame.font.Font('freesansbold.ttf', 32)
    text2 = font2.render('Press B or click top right to return', True, GREEN, BLUE)
    text2Rect = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(text, textRect)
    screen.blit(text2, text2Rect)

def score(score_value):
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render(f'Score {score_value}', True, GREEN, BLUE)
    textRect = text.get_rect(center=(800, 50))
    screen.blit(text, textRect)

def lose():
    screen.fill(BLACK)
    font = pygame.font.Font('freesansbold.ttf', 82)
    lose_text = font.render('You Lost!', True, WHITE, RED)
    loseRect = lose_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(lose_text, loseRect)

def win():
    screen.fill(WHITE)
    font = pygame.font.Font('freesansbold.ttf', 82)
    win_text = font.render('You WIIIIN!', True, LIGHT_BLUE, BLUE)
    winRect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(win_text, winRect)

def return_to_menu():
    return_font = pygame.font.Font('freesansbold.ttf', 32)
    menu_text = return_font.render('Press R to restart the game!', True, WHITE, RED)
    menuRect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 300))
    screen.blit(menu_text, menuRect)

# ------------------------
# LOAD BUTTON IMAGES & CLOCK
# ------------------------
pause_img = pygame.image.load('pictures/pause_button.png')
pause_img = pygame.transform.scale(pause_img, (50, 50))
question_img = pygame.image.load('pictures/question_mark.png')
question_img = pygame.transform.scale(question_img, (50, 50))
red_gun_img = pygame.image.load('pictures/red_gun.png')
red_gun_img = pygame.transform.scale(red_gun_img, (50, 50))
blue_gun_img = pygame.image.load('pictures/blue_gun.png')
blue_gun_img = pygame.transform.scale(blue_gun_img, (50, 50))
no_gun_img = pygame.image.load('pictures/no_gun.png')
no_gun_img = pygame.transform.scale(no_gun_img, (50, 50))
play_img = pygame.image.load('pictures/play_button.png')
play_img = pygame.transform.scale(play_img, (50, 50))
clock = pygame.time.Clock()

# ------------------------
# MAIN GAME LOOP: OUTER MENU LOOP & INNER LEVEL LOOP
# ------------------------
running_game = True
while running_game:
    # Outer loop: show menu to select a level.
    sc_map = run_menu()  # This function returns a level map from your maps module.
    if sc_map is None:
        break  # Exit if menu is closed.

    # Update current_level based on the returned map.
    if sc_map == maps.level_one_test:
        current_level = 1
    elif sc_map == maps.level_two:
        current_level = 2
    elif sc_map == maps.level_three:
        current_level = 3
    elif sc_map == maps.level_four:
        current_level = 4
    elif sc_map == maps.level_five:
        current_level = 5

    # Reinitialize game state for the new level.
    create_lists()
    create_map(sc_map)
    player1 = create_players(25, 575, RED)
    player2 = create_players(25, 375, BLUE)
    start_time = pygame.time.get_ticks()
    final_score = 0
    level_running = True

    while level_running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level_running = False
                running_game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player1.go_left()
                elif event.key == pygame.K_RIGHT:
                    player1.go_right()
                elif event.key == pygame.K_UP:
                    player1.jump()
                elif event.key == pygame.K_DOWN:
                    player1.shoot()
                if event.key == pygame.K_a:
                    player2.go_left()
                elif event.key == pygame.K_d:
                    player2.go_right()
                elif event.key == pygame.K_w:
                    player2.jump()
                elif event.key == pygame.K_s:
                    player2.shoot()
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player1.stop()
                if event.key in (pygame.K_a, pygame.K_d):
                    player2.stop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos
                # For example, clicking on the pause button returns to the menu.
                if (x > 30 and x < 80) and (y > 20 and y < 70):
                    sc_map = run_menu()
                    level_running = False

        screen.fill(GREEN)

        # Update portals and enemy actions.
        p_opener_purple = portal_opener_list['purple'][0] if portal_opener_list['purple'] else None
        p_opener_brown = portal_opener_list['brown'][0] if portal_opener_list['brown'] else None
        p_opener_orange = portal_opener_list['orange'][0] if portal_opener_list['orange'] else None

        for portal in portal_list['purple']:
            if p_opener_purple:
                portal.open_portal(p_opener_purple, player1, player2, "down")
        for portal in portal_list['brown']:
            if p_opener_brown:
                portal.open_portal(p_opener_brown, player1, player2, "down")
        for portal in portal_list['orange']:
            if p_opener_orange:
                portal.open_portal(p_opener_orange, player1, player2, "up")

        for enemy in all_enemy_list:
            enemy.attack(player1)
            enemy.attack(player2)

        for coin in coins_list:
            coin.draw(screen)

        final_score += score_total(player1) + score_total(player2)

        # Handle trapeze adjustments.
        k1 = high(player1, trapeze_list)
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

        # Handle gun power-ups.
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

        screen.blit(question_img, (1200, 20))
        screen.blit(pause_img, (30, 20))

        font = pygame.font.Font('freesansbold.ttf', 30)
        text1 = font.render('Color : Red', True, RED) if player1.color == RED else font.render('Color : Green', True, GREEN)
        text1Rect = text1.get_rect(center=(SCREEN_WIDTH // 4, 40))
        screen.blit(text1, text1Rect)
        text2 = font.render('Color : Blue', True, BLUE) if player2.color == BLUE else font.render('Color : Black', True, BLACK)
        text2Rect = text2.get_rect(center=(3 * SCREEN_WIDTH // 4, 40))
        screen.blit(text2, text2Rect)

        score(final_score)

        if player1.guns:
            screen.blit(red_gun_img, (200, 20))
            remaining_time = (player1.duration - (current_time - player1.timer)) / 1000
            timer_text = font.render(str(int(remaining_time)), True, RED)
            screen.blit(timer_text, (260, 35))
            if current_time - player1.timer > player1.duration:
                player1.guns = False
                player1.timer = None
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
        else:
            screen.blit(no_gun_img, (1080, 20))

        # Display timer.
        elapsed_time = current_time - start_time
        seconds = elapsed_time // 1000
        minutes = seconds // 60
        seconds %= 60    
        time_string = f"{minutes:02}:{seconds:02}"
        timer_display = pygame.font.Font(None, 50).render(time_string, True, WHITE)
        timer_rect = timer_display.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(timer_display, timer_rect)

        all_sprite_list.update()
        for bullet in bullet_list:
            enemy_hits = pygame.sprite.spritecollide(bullet, all_enemy_list, False)
            if enemy_hits:
                bullet.kill()
                for enemy in enemy_hits:
                    if enemy.life > 1:
                        enemy.life -= 1
                    else:
                        enemy.kill()
                        final_score += 10
            block_hits = pygame.sprite.spritecollide(bullet, wall_list, False)
            if block_hits:
                bullet.kill()

        all_sprite_list.draw(screen)
        pygame.display.flip()
        clock.tick(60)

        # Check lose condition.
        check_die(player1, all_lakes_list, all_enemy_list)
        check_die(player2, all_lakes_list, all_enemy_list)
        if player1.life <= 0 or player2.life <= 0:
            delete_map()
            lose()
            pygame.display.flip()
            time.sleep(2)
            level_running = False

        # Check win condition (both doors activated).
        if len(door_list) >= 2 and door_list[0].update_door(player1) and door_list[1].update_door(player2):
            delete_map()
            win()
            pygame.display.flip()
            time.sleep(2)
            change_level(current_level, "passed")
            level_running = False

pygame.quit()
