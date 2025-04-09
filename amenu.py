import pygame

# colors
WHITE     = (255, 255, 255)
DARK_GRAY = (70, 70, 70)



# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT =  720
class Level(pygame.sprite.Sprite):
    # creating level class
    # constructor
    def __init__(self, x, y, text, font_1, font_2, condition, number):
        super().__init__()
        self.text = text
        self.font_1 = font_1 # font for "Level X" text
        self.font_2 = font_2 # font for level number inside icon
        self.condition = condition # locked, unlocked, or passed
        self.number = number
        self.rect = pygame.Rect(x, y, 100, 100)  # using a rect for positioning
        self.set_condition(condition)

        # loading the appropriate image based on the condition
    # end constructor

    def set_condition(self, condition):
        # checking the condition and loading the appropriate image
        self.condition = condition
        if self.condition == "passed":
            image = pygame.image.load("pictures/level_passed.png")
            self.image = pygame.transform.scale(image, (100, 100))
        elif self.condition == "locked":
            image = pygame.image.load("pictures/level_locked.png")
            self.image = pygame.transform.scale(image, (100, 100))
        elif self.condition == "unlocked":
            image = pygame.image.load("pictures/level_unlocked.png")
            self.image = pygame.transform.scale(image, (100, 100))
        # end if
    # end method

    def draw(self, surface):
        # blitting the image on the screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
        # getting the number of the level 
        level_text = self.font_1.render(f'Level {str(self.number)}', True, WHITE)
        level_text_Rect = level_text.get_rect()
        level_text_Rect.center = (self.rect.x + 50, self.rect.y+120)
        # blitting underneath the icon the level
        surface.blit(level_text, level_text_Rect)
        if self.condition == "unlocked":
            # if the level is unlocked also blitting the number inside the icon
            level_text_2 = self.font_2.render(f'{self.number}', True, WHITE)
            level_text_2_Rect = level_text_2.get_rect()
            level_text_2_Rect.center = (self.rect.x + 50, self.rect.y+50)
            surface.blit(level_text_2, level_text_2_Rect)
        # end if
    # end method
# end class



# initializing pygame
pygame.init()
# setting up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# create level objects in a row
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
                if question_rect.collidepoint(pos):
                    return 'controls'
                elif back_button_rect.collidepoint(pos):
                    return 'back'
                # end if

                for level in levels_objs:
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
                            # end if
                        # end if
                    # end if
                # next level

            # end if
        # next event

        # loading the image for the lhe back button
        back_button_img = pygame.image.load("pictures/Back_button.png")
        # reducing the size of the image
        back_button_img = pygame.transform.scale(back_button_img, (150, 150))
        # getting the rect of the image
        back_button_rect = back_button_img.get_rect(center=(100,100))
        # blitting the image on the screen
        screen.blit(back_button_img, back_button_rect)

        # loading the image for the question button
        question_img = pygame.image.load('pictures/question_button.png')
        # reducing the size of the image
        question_img = pygame.transform.scale(question_img, (150, 150))
        # getting the rect of the image
        question_rect = question_img.get_rect(center=(1200,100))
        # blitting the imageon the screen
        screen.blit(question_img, question_rect)

        # drawing the level buttons one by one
        for level in levels_objs:
            level.draw(screen)
        # end if

        pygame.display.flip()    
    # end while
# end main procedure

if __name__ == '__main__':
    main()

