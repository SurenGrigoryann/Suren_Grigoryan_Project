import pygame

pygame.init()
# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Scene Switch Demo')

# Define colors
WHITE     = (255, 255, 255)
BROWN     = (139, 69, 19)
GRAY      = (100, 100, 100)
DARK_GRAY = (70, 70, 70)
YELLOW   = (255, 255, 0)


levels = {1: "unlocked", 2: "locked", 3: "locked", 4: "locked", 5: "locked"}

class Level:
    def __init__(self, x,y, text, font, condition, number):
        self.text = text
        self.font = font

        self.condition = condition

        if self.condition == "passed":
            self.image = pygame.transform.scale(pygame.image.load("pictures/level_passed.png"), (100, 100))
        elif self.condition == "locked":            
            self.image = pygame.transform.scale(pygame.image.load("pictures/level_locked.png"), (100, 100))
        elif self.condition == "unlocked":
            self.image = pygame.transform.scale(pygame.image.load("pictures/level_unlocked.png"), (100, 100))

        # Render the text and determine its rectangle.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.x = x
        self.y = y
        self.number = number
    def draw(self, surface):
        # Draw the level icon.
        surface.blit(self.image, (self.x, self.y))
        # Optionally, render and draw text below the icon.
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.x + 50, self.y + 120))
        surface.blit(text_surface, text_rect)

# Create level objects and position them on screen.
levels_objs = []
font = pygame.font.SysFont(None, 30)
start_x = 50
start_y = 50
spacing = 150

for level_number, condition in levels_data.items():
    level_text = "Level " + str(level_number)
    level_obj = Level(start_x, start_y, level_text, font, condition, level_number)
    levels_objs.append(level_obj)
    start_x += spacing  # Move to the right for the next level icon

running = True
while running:
    screen.fill(DARK_GRAY)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for level in levels_objs:
                if level.rect.collidepoint(pos):
                    # Only allow switching if the level is unlocked or already passed.
                    if level.condition in ["unlocked", "passed"]:
                        if level.number == 1:
                            maps.level_one()
                        elif level.number == 2:
                            maps.level_two()
                        elif level.number == 3:
                            maps.level_three()
                        elif level.number == 4:
                            maps.level_four()
                        elif level.number == 5:
                            maps.level_five()
    
    # Draw all level icons.
    for level in levels_objs:
        level.draw(screen)
    
    pygame.display.update()

pygame.quit()
    



