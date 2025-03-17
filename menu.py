import pygame
import maps  # This module should define functions like level_one(), level_two(), etc.

pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Scene Switch Demo')

# Define colors
WHITE     = (255, 255, 255)
DARK_GRAY = (70, 70, 70)

# Level status: each key is a level number and value is the condition.
levels_data = {1: "unlocked", 2: "locked", 3: "locked", 4: "locked", 5: "locked"}

class Level(pygame.sprite.Sprite):
    def __init__(self, x, y, text, font_1, font_2, condition, number):
        super().__init__()
        self.text = text
        self.font_1 = font_1
        self.font_2 = font_2
        self.condition = condition
        self.number = number

        # Load the appropriate image based on the condition.
        if self.condition == "passed":
            self.image = pygame.transform.scale(
                pygame.image.load("pictures/level_passed.png"), (100, 100)
            )
        elif self.condition == "locked":
            self.image = pygame.transform.scale(
                pygame.image.load("pictures/level_locked.png"), (100, 100)
            )
        elif self.condition == "unlocked":
            self.image = pygame.transform.scale(
                pygame.image.load("pictures/level_unlocked.png"), (100, 100)
            )

        # Create a rectangle for collision detection.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x




    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        level_text = self.font_1.render(f'Level {str(self.number)}', True, WHITE)
        level_text_Rect = level_text.get_rect()
        level_text_Rect.center = (self.rect.x + 50, self.rect.y+120)
        surface.blit(level_text, level_text_Rect)
        if self.condition == "unlocked":
            level_text_2 = self.font_2.render(f'1', True, WHITE)
            level_text_2_Rect = level_text_2.get_rect()
            level_text_2_Rect.center = (self.rect.x + 50, self.rect.y+50)
            surface.blit(level_text_2, level_text_2_Rect)


# Create level objects in a row.
levels_objs = pygame.sprite.Group()
font_one = pygame.font.Font('freesansbold.ttf',25)
font_two = pygame.font.Font('freesansbold.ttf', 40)
level_one = Level(SCREEN_WIDTH // 4.5, SCREEN_HEIGHT // 2 - 100, "Level 1", font_one, font_two, levels_data[1], 1)
levels_objs.add(level_one)
level_two = Level(SCREEN_WIDTH // 4.5 + 150, SCREEN_HEIGHT // 2 - 100, "Level 2", font_one, font_two, levels_data[2], 2)
levels_objs.add(level_two)
level_three = Level(SCREEN_WIDTH // 4.5 + 300, SCREEN_HEIGHT // 2 - 100, "Level 3", font_one, font_two, levels_data[3], 3)
levels_objs.add(level_three)
level_four = Level(SCREEN_WIDTH // 4.5 + 450, SCREEN_HEIGHT // 2 - 100, "Level 4", font_one, font_two, levels_data[4], 4)
levels_objs.add(level_four)
level_five = Level(SCREEN_WIDTH // 4.5 + 600, SCREEN_HEIGHT // 2 - 100, "Level 5", font_one, font_two, levels_data[5], 5)            
levels_objs.add(level_five)


font = pygame.font.SysFont(None, 30)
start_x = 50  # Starting x position
start_y = 50  # Starting y position for all icons
spacing = 150  # Horizontal space between each level icon


def change_level(level, passed_not_passed):
    if passed_not_passed == "passed":
        levels_data[level] = "passed"
        levels_data[level + 1] = "unlocked"


def run_menu():

    running = True
    while running:
        screen.fill(DARK_GRAY)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for level in levels_objs:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        x,y = pos[0],pos[1]          
                        if x >= level.rect.x and x <= level.rect.x + 100 and y >= level.rect.y and y <= level.rect.y + 100:
                            if level.condition == "unlocked":
                                if level.number == 1:
                                    return maps.level_one_test
                                elif level.number == 2:
                                    return maps.level_two
                                elif level.number == 3:
                                    return maps.level_three
                                elif level.number == 4:
                                    return maps.level_four
                                elif level.number == 5:
                                    return maps.level_five 
        # Draw all level icons.
        for level in levels_objs:
            level.draw(screen)
        pygame.display.flip()

    pygame.quit()


