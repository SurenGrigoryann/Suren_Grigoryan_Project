import pygame



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
        self.rect = pygame.Rect(x, y, 100, 100)  # Using a rect for positioning
        self.set_condition(condition)

        # Load the appropriate image based on the condition.
        

    def set_condition(self, condition):
        self.condition = condition
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




    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        level_text = self.font_1.render(f'Level {str(self.number)}', True, WHITE)
        level_text_Rect = level_text.get_rect()
        level_text_Rect.center = (self.rect.x + 50, self.rect.y+120)
        surface.blit(level_text, level_text_Rect)
        if self.condition == "unlocked":
            level_text_2 = self.font_2.render(f'{self.number}', True, WHITE)
            level_text_2_Rect = level_text_2.get_rect()
            level_text_2_Rect.center = (self.rect.x + 50, self.rect.y+50)
            surface.blit(level_text_2, level_text_2_Rect)


# Create level objects in a row.
levels_objs = pygame.sprite.Group()
font_one = pygame.font.Font('freesansbold.ttf',25)
font_two = pygame.font.Font('freesansbold.ttf', 40)
level_one = Level(SCREEN_WIDTH // 4.5, SCREEN_HEIGHT // 2 - 100, "Level 1", font_one, font_two, "unlocked", 1)
levels_objs.add(level_one)
level_two = Level(SCREEN_WIDTH // 4.5 + 150, SCREEN_HEIGHT // 2 - 100, "Level 2", font_one, font_two, "locked", 2)
levels_objs.add(level_two)
level_three = Level(SCREEN_WIDTH // 4.5 + 300, SCREEN_HEIGHT // 2 - 100, "Level 3", font_one, font_two, "locked", 3)
levels_objs.add(level_three)
level_four = Level(SCREEN_WIDTH // 4.5 + 450, SCREEN_HEIGHT // 2 - 100, "Level 4", font_one, font_two, "locked", 4)
levels_objs.add(level_four)
level_five = Level(SCREEN_WIDTH // 4.5 + 600, SCREEN_HEIGHT // 2 - 100, "Level 5", font_one, font_two, "locked", 5)            
levels_objs.add(level_five)


#font = pygame.font.SysFont(None, 30)
start_x = 50  # Starting x position
start_y = 50  # Starting y position for all icons
spacing = 150  # Horizontal space between each level icon




def main():
    running = True
    # main loop
    while running:
        # filling the screen with color
        screen.fill(DARK_GRAY)
        events = pygame.event.get()
        # checking the events
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                return quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Check if the back button was clicked (positioned at (10,10), size 100x100)
                if 10 <= pos[0] <= 110 and 10 <= pos[1] <= 110:
                    return 'back'
                elif question_rect.collidepoint(pos):
                    return 'controls'

                for level in levels_objs:
                    #if event.type == pygame.MOUSEBUTTONDOWN:
                     #   pos = pygame.mouse.get_pos()
                        x,y = pos[0],pos[1]          
                        if x >= level.rect.x and x <= level.rect.x + 100 and y >= level.rect.y and y <= level.rect.y + 100:
                            if level.condition == "unlocked" or level.condition == 'passed':
                                if level.number == 1:
                                    return 'level_one'
                                elif level.number == 2:
                                    return 'level_two'
                                elif level.number == 3:
                                    return 'level_three'
                                elif level.number == 4:
                                    return 'level_four'
                                elif level.number == 5:
                                    return 'level_five'
        # Draw all level icons.
        back_button_img = pygame.image.load("pictures/Back_button.png")
        back_button_img = pygame.transform.scale(back_button_img, (100, 100))
        screen.blit(back_button_img, (10, 10))
        question_img = pygame.image.load('pictures/question_button.png')
        question_img = pygame.transform.scale(question_img, (150, 150))
        question_rect = question_img.get_rect(center=(1200,100))
        screen.blit(question_img, question_rect)


        for level in levels_objs:
            level.draw(screen)
        pygame.display.flip()    

    #return

if __name__ == '__main__':
    main()
