import pygame
# importing the necessary libraries


# The dimensions of the screen held as constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720


# colors
WHITE     = (255, 255, 255)
BROWN     = (139, 69, 19)
GRAY      = (100, 100, 100)
DARK_GRAY = (70, 70, 70)


# initializing the pygame
pygame.init()

# setting up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Button:
    # defining the button class
    # the construtcor
    def __init__(self, center, text, font, radius=100,
                 bg_color=GRAY, text_color=WHITE, hover_color=DARK_GRAY):
        # initializing the button attributes

        self.center = center # center of the button
        self.text = text # text to be displayed on the button
        self.font = font # font of the text
        self.bg_color = bg_color # background color of the button(default color)
        self.text_color = text_color # text color of the button
        self.hover_color = hover_color # hover color of the button

        self.text_surface = self.font.render(self.text, True, self.text_color)

        # Get the rectangle (bounding box) of the text and center it at the button's position.
        self.text_rect = self.text_surface.get_rect(center=center)

        # Set the radius of the circular button (already provided as a value).
        self.radius = radius
    # end constructor
    def draw(self, surface):

        mouse_pos = pygame.mouse.get_pos()
        if ((mouse_pos[0] - self.center[0]) ** 2 + (mouse_pos[1] - self.center[1]) ** 2) <= self.radius ** 2:
            # x^2 + y^2 <= radius^2 (inside the circle)
            color = self.hover_color
        else:
            color = self.bg_color
        # end if
        # Draw the button as a circle with the specified color.
        pygame.draw.circle(surface, color, self.center, self.radius)

        self.text_rect = self.text_surface.get_rect(center=self.center)
        # Draw the text on top of the button.
        surface.blit(self.text_surface, self.text_rect)
    # end method
    def is_clicked(self, event):
        # Check if the mouse is clicked and if the click is inside the button's area.
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if ((mouse_pos[0] - self.center[0]) ** 2 + (mouse_pos[1] - self.center[1]) ** 2) <= self.radius ** 2:
                # x^2 + y^2 <= radius^2 (inside the circle)
                # Check if the button is clicked.
                return True
            # end if
        # end if
        # If the button is not clicked, return False.
        return False
    # end method
# end class


# creatung the global variable current_scene
current_scene = "main"

def main_scene(events):
    global current_scene
    screen.fill(BROWN)
    font = pygame.font.Font('freesansbold.ttf', 32)
    
    # define all the buttons for the main scene.
    buttons = [
        Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200), 'Controls', font),
        Button((SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 100), 'Enemies', font),
        Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100), '  Lakes  ', font),
        Button((SCREEN_WIDTH  * 3 // 4, SCREEN_HEIGHT // 2 + 100), ' Other ', font)
    ]
    
    # draw buttons.
    for button in buttons:
        button.draw(screen)
    # next button


    back_button_img = pygame.image.load('pictures/back_button.png')
    back_button_img = pygame.transform.scale(back_button_img, (100, 100))
    back_button_rect = back_button_img.get_rect(center=(60, 60))
    screen.blit(back_button_img, back_button_rect)
    # Check for clicks on buttons.
    # changing the current_scene based on the button clicked.
    for event in events:
        if buttons[0].is_clicked(event):
            current_scene = "player_info"
        if buttons[1].is_clicked(event):
            current_scene = "enemy_info"
        if buttons[2].is_clicked(event):
            current_scene = "lakes_info"
        if buttons[3].is_clicked(event):
            current_scene = "portals_info"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if back_button_rect.collidepoint(pos):
                return 'back'
        # end if
    # next event


    # flip the display to show the drawn buttons
    pygame.display.flip()
# end procedure


def player_info_scene(events):

    global current_scene
    # filling the screen with a color
    screen.fill(DARK_GRAY)
    
    # Use a large font for the heading
    title_font = pygame.font.Font('freesansbold.ttf', 36)
    # Use a smaller font for the enemy details
    info_font = pygame.font.SysFont('DejaVu Sans', 24)

    # Display "enemy info" text at the top
    title_text = title_font.render("Control Info", True, (255, 220, 0))  # Gold-like color
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    # blitting the text on the screen
    screen.blit(title_text, title_rect)



    # loading the images for the players
    player1_image = pygame.image.load("pictures/red_player.png")
    player2_image = pygame.image.load("pictures/blue_player.png")
    # reducing the size of the images
    player1_image = pygame.transform.scale(player1_image, (60, 100))
    player2_image = pygame.transform.scale(player2_image, (60, 100))
    # getting the rect of the images
    player1_rect = player1_image.get_rect(center=(SCREEN_WIDTH //5, SCREEN_HEIGHT // 3))
    player2_rect = player2_image.get_rect(center=((SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))
    # blitting the images on the screen
    screen.blit(player1_image, player1_rect)
    screen.blit(player2_image, player2_rect)

    # all the texts for Lory are stored in a list of tuples
    texts1 = [
        ('Lory', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 - 80)),
        ('Health: 1 | Speed: 3', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 80)),
        ('Description:', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 120)),
        ('Lory is the red magic twin. He is able to  ', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 160)),
        ('go through red lakes, and can collect red  ', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 190)),
        ('coins. He is here to return the crown! ', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 220)),
    

        ('Controls:', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 260)),
        ('\u2190 to go left', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 290)),
        ('  \u2192 to go right', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 320)),
        ('\u2191 to jump', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 350)),
        (' \u2193 to shoot', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 380)),
        ('(only if you have a gun)', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 410))
        ]

    # loop through and blit all the texts on the screen
    for message, pos in texts1:
        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)
    # next message, pos


    # all the texts for Mory are stored in a list of tuples
    texts2 = [
        ('Mory', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 80)),
        ('Health: 1 | Speed: 3', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 80)),
        ('Description:', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 120)),
        ('Mory is the blue magic twin. He is able to ', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 160)),
        ('fo through blue lakes and can collect blue ', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 190)),
        ('coins. He is here to have some fun and help Lory!', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 220)),
        
        ('Controls:', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 260)),
        ('z   to go left', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 290)),
        ('d  to go right', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 320)),
        ('w      to jump', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 350)),
        ('s     to shoot', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 380)),
        ('(only if you have a gun)', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 410))
    ]
    
    # loop through and blit all the texts on the screen
    for message, pos in texts2:

        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)
    # next message,pos


    draw_back_button(events)
    # loading the image for the back button

    # flipping the display to show the drawn texts and images
    pygame.display.flip()
# end procedure


def enemy_info_scene(events):
    global current_scene
    # filling the screen with a color
    screen.fill(DARK_GRAY)
    
    # Use a large font for the heading
    title_font = pygame.font.Font('freesansbold.ttf', 36)
    # Use a smaller font for the enemy details
    info_font = pygame.font.SysFont('DejaVu Sans', 24)

    # Display "enemy info" text at the top
    enemy_text = title_font.render("Enemy Info", True, (255, 220, 0))  # Gold-like color
    enemy_rect = enemy_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    # blitting the text on the screen
    screen.blit(enemy_text, enemy_rect)

    # loading the images for the enemies
    tank_image = pygame.image.load("pictures/Tank.png")
    fast_image = pygame.image.load("pictures/fast_enemy.png")
    # reducing the size of the images
    tank_image = pygame.transform.scale(tank_image, (100, 100))
    fast_image = pygame.transform.scale(fast_image, (100, 100))
    # getting the rect of the images
    tank_rect = tank_image.get_rect(center=(SCREEN_WIDTH //5, SCREEN_HEIGHT // 3))
    fast_rect = fast_image.get_rect(center=((SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))

    # blitting the images on the screen
    screen.blit(tank_image, tank_rect)
    screen.blit(fast_image, fast_rect)

    # all the texts for the tank are stored in a list of tuples
    texts = [
        ('Oblivion - K17', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 - 80)),
        ('Health: 10 | Speed: 0.8', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 80)),
        ('Description:', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 120)),
        ('One of the favourite robots of the witch!', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 160)),
        ('She created them to be strong and brutal!', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 190)),
        ('Do not go head to head with them they', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 220)),
        ('will kill you! They are not that fast ', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 250)),
        ('so you may consider running! ', (SCREEN_WIDTH //5, SCREEN_HEIGHT // 3 + 280))
    ]

    # loop through and blit all the texts on the screen
    for message, pos in texts:
        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)
    # next message, pos


    # all the texts for the mini-witch are stored in a list of tuples
    texts = [
        ('Mini-Witch', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 80)),
        ('Health: 5 | Speed: 2', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 80)),
        ('Description:', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 120)),
        ('Witch created milions of copies herself', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 160)),
        ('but smaller and weaker.They are pretty', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 190)),
        ('fast so be ready to fight back!', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 220)),
    ]
    
    # loop through and blit all the texts on the screen
    for message, pos in texts:
        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)
    # next message,pos

    draw_back_button(events)
    # loading the image for the back button

    # flipping the display to show the drawn texts and images
    pygame.display.flip()
# end procedure


def lakes_info_scene(events):
    global current_scene
    # filling the screen with a color
    screen.fill(DARK_GRAY)
    
    # Use a large font for the heading
    title_font = pygame.font.Font('freesansbold.ttf', 36)
    # Use a smaller font for the lake details
    info_font = pygame.font.SysFont('DejaVu Sans', 24)

    # Display "Lake Info" text at the top
    lake_text = title_font.render("Lake Info", True, (255, 220, 0))  # Gold-like color
    lake_rect = lake_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    # blitting the text on the screen
    screen.blit(lake_text, lake_rect)

    # loading the images for the lakes
    red_lake_image = pygame.image.load("pictures/red_lake.png")
    blue_lake_image = pygame.image.load("pictures/blue_lake.png")
    black_lake_image = pygame.image.load("pictures/black_lake.png")

    # reducing the size of the images
    red_lake_image = pygame.transform.scale(red_lake_image, (100, 100))
    blue_lake_image = pygame.transform.scale(blue_lake_image, (100, 100))
    black_lake_image = pygame.transform.scale(black_lake_image, (100, 100))

    # getting the rect of the images
    red_lake_rect = red_lake_image.get_rect(center=(SCREEN_WIDTH - 1080, SCREEN_HEIGHT // 3))
    blue_lake_rect = blue_lake_image.get_rect(center=(SCREEN_WIDTH - ((1080 + 200) // 2), SCREEN_HEIGHT // 3))
    black_lake_rect = black_lake_image.get_rect(center=(SCREEN_WIDTH - 200 , SCREEN_HEIGHT // 3))

    # blitting the images on the screen
    screen.blit(red_lake_image, red_lake_rect)
    screen.blit(blue_lake_image, blue_lake_rect)
    screen.blit(black_lake_image, black_lake_rect)

    # all the texts for the red lake are stored in a list of tuples
    texts1 = [
        ('Red Lake', (SCREEN_WIDTH - 1080, SCREEN_HEIGHT // 3 - 80)),
        ('Lory was born with fire in his ', (SCREEN_WIDTH - 1080, SCREEN_HEIGHT // 3 + 80)),
        ('veins - this lake recognizes his', (SCREEN_WIDTH - 1080, SCREEN_HEIGHT // 3 + 120)),
        ('power. However, Mory will be', (SCREEN_WIDTH - 1080, SCREEN_HEIGHT // 3 + 160)),
        ('burned instantly if he touches it!', (SCREEN_WIDTH - 1080, SCREEN_HEIGHT // 3 + 200))
    ]

    # loop through and blit all the texts on the screen
    for message, pos in texts1:
        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)
    # next message, pos

    # all the texts for the blue lake are stored in a list of tuples
    texts2 = [
        ('Blue Lake', (SCREEN_WIDTH - ((1080 + 200) // 2), SCREEN_HEIGHT // 3 - 80)),
        ('This lake flows with the calm ', (SCREEN_WIDTH - ((1080 + 200) // 2), SCREEN_HEIGHT // 3 + 80)),
        ('and focused energy of Mory\'s blue', (SCREEN_WIDTH - ((1080 + 200) // 2), SCREEN_HEIGHT // 3 + 120)),
        ('magic. Lory does not belong here -', (SCREEN_WIDTH - ((1080 + 200) // 2), SCREEN_HEIGHT // 3 + 160)),
        ('it will instantly kill him!', (SCREEN_WIDTH - ((1080 + 200) // 2), SCREEN_HEIGHT // 3 + 200))
    ]

    # loop through and blit all the texts on the screen
    for message, pos in texts2:
        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)
    # next message, pos

    # all the texts for the black lake are stored in a list of tuples
    texts3 = [
        ('The black spell lake.', (SCREEN_WIDTH - 200 , SCREEN_HEIGHT // 3 - 80)),
        ('Neither twin dares to cross it.', (SCREEN_WIDTH - 200 , SCREEN_HEIGHT // 3 + 80)),
        ('It belongs to no one and shows', (SCREEN_WIDTH - 200, SCREEN_HEIGHT // 3 + 120)),
        ('no mercy! Lory and Mory will die', (SCREEN_WIDTH - 200, SCREEN_HEIGHT // 3 + 160)),
        ('instantly if they touch it!', (SCREEN_WIDTH - 200, SCREEN_HEIGHT // 3 + 200))
    ]

    # loop through and blit all the texts on the screen
    for message, pos in texts3:
        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)
    # next message, pos

    # loop through and blit all the texts on the screen
    for message, pos in texts1:
        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)
    # next message, pos

    # all the texts for the blue lake are stored in a list of tuples
    texts2 = [
        ('Blue Lake', (SCREEN_WIDTH - ((1080+200)//2), SCREEN_HEIGHT // 3 - 80)),
        ('This lake flows with the calm ', (SCREEN_WIDTH - ((1080+200)//2), SCREEN_HEIGHT // 3 + 80)),
        ('and focused energy of Mory\'s blue', (SCREEN_WIDTH - ((1080+200)//2), SCREEN_HEIGHT // 3 + 120)),
        ('magic. Lory does not belong here -', (SCREEN_WIDTH - ((1080+200)//2), SCREEN_HEIGHT // 3 + 160)),
        ('it will instantly kill him!', (SCREEN_WIDTH - ((1080+200)//2), SCREEN_HEIGHT // 3 + 200))
    ]
    # loop through and blit all the texts on the screen
    for message, pos in texts2:
        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)
    # next message,pos

    texts3 = [
        ('The black spell lake.', (SCREEN_WIDTH - 200 , SCREEN_HEIGHT // 3 - 80)),
        ('Neither twin dares to cross it.', (SCREEN_WIDTH - 200 , SCREEN_HEIGHT // 3 + 80)),
        ('It belongs to no one and shows', (SCREEN_WIDTH - 200, SCREEN_HEIGHT // 3 + 120)),
        ('no mercy! Lory and Mory will die', (SCREEN_WIDTH - 200, SCREEN_HEIGHT // 3 + 160)),
        ('instantly if they touch it!', (SCREEN_WIDTH - 200, SCREEN_HEIGHT // 3 + 200))

    ]
    
    
    # loop through and blit all the texts on the screen
    for message, pos in texts3:
        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)
    # next message,pos

    draw_back_button(events)
    # loading the image for the back button


    # flipping the display to show the drawn texts and images
    pygame.display.flip()
# end procedure



def other_info_scene(events):
    global current_scene
    # filling the screen with a color
    screen.fill(DARK_GRAY)
    
    # Use a large font for the heading
    title_font = pygame.font.Font('freesansbold.ttf', 36)
    # Use a smaller font for the lake details
    info_font = pygame.font.SysFont('DejaVu Sans', 24)

    # Display "other info" text at the top
    title_text = title_font.render("Other info", True, (255, 220, 0))  # Gold-like color
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    # blitting the text on the screen
    screen.blit(title_text, title_rect)

    # loading the images for the red door and blue door
    red_door_image = pygame.image.load("pictures/red_door.png")
    blue_door_image = pygame.image.load("pictures/blue_door.png")
    # reducing the size of the images
    red_door_image = pygame.transform.scale(red_door_image, (100, 100))
    blue_door_image = pygame.transform.scale(blue_door_image, (100, 100))
    # getting the rect of the images
    red_door_rect = red_door_image.get_rect(center=(SCREEN_WIDTH - 1130, SCREEN_HEIGHT // 3))
    blue_door_rect = blue_door_image.get_rect(center=(SCREEN_WIDTH - 1030, SCREEN_HEIGHT // 3))
    # blitting the images on the screen
    screen.blit(red_door_image, red_door_rect)
    screen.blit(blue_door_image, blue_door_rect)

    # all the texts for the red and blue doors are stored in a list of tuples
    texts1 = [
        ('The Red door opens only for Lory', (SCREEN_WIDTH - 1080, SCREEN_HEIGHT // 3 - 80)),
        ('The Red door opens only for Lory', (SCREEN_WIDTH - 1080, SCREEN_HEIGHT // 3 + 80)),
        ('While the Blue door responds only', (SCREEN_WIDTH - 1080, SCREEN_HEIGHT // 3 + 120)),
        ('to Mory. No matter how hard they', (SCREEN_WIDTH - 1080, SCREEN_HEIGHT // 3 + 160)),
        ('try, neither twin can open the ', (SCREEN_WIDTH - 1080, SCREEN_HEIGHT // 3 + 200)),
        ('other\'s door - the magic simply', (SCREEN_WIDTH - 1080, SCREEN_HEIGHT // 3 + 240)),
        ('will not allow it!', (SCREEN_WIDTH - 1080, SCREEN_HEIGHT // 3 + 280))
    ]

    # loop through and blit all the texts on the screen
    for message, pos in texts1:
        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)
    # next message, pos

    # loading the images for the orange portal and portal_opener 
    orange_portal_image = pygame.image.load("pictures/orange_portal.png")
    orange_portal_opener_image = pygame.image.load("pictures/orange_portal_opener.png")
    # reducing the size of the images
    orange_portal_image = pygame.transform.scale(orange_portal_image, (100, 30))
    orange_portal_opener_image = pygame.transform.scale(orange_portal_opener_image, (40, 40))
    # getting the rect of the images
    orange_portal_rect = orange_portal_image.get_rect(center=(SCREEN_WIDTH - 680, SCREEN_HEIGHT // 3 - 50))
    orange_portal_opener_rect = orange_portal_opener_image.get_rect(center=(SCREEN_WIDTH - 680, SCREEN_HEIGHT // 3 + 30))

    # blitting the images on the screen
    screen.blit(orange_portal_image, orange_portal_rect)
    screen.blit(orange_portal_opener_image, orange_portal_opener_rect)


    # all the texts for the portal and portal openers are stored in a list of tuples
    texts2 = [
        ('Portal', (SCREEN_WIDTH - 680, SCREEN_HEIGHT // 3 - 80)),
        ('Portal opener', (SCREEN_WIDTH - 680, SCREEN_HEIGHT // 3 -10)),
        ('Portals act like magical doors', (SCREEN_WIDTH - 680, SCREEN_HEIGHT // 3 + 80)),
        ('that can open in specific directions.', (SCREEN_WIDTH - 680, SCREEN_HEIGHT // 3 + 120)),
        ('When a player collides with a  ', (SCREEN_WIDTH - 680, SCREEN_HEIGHT // 3 + 160)),
        ('portal opener, it triggers the ', (SCREEN_WIDTH - 680, SCREEN_HEIGHT // 3 + 200)),
        ('portal to open towards a certain', (SCREEN_WIDTH - 680, SCREEN_HEIGHT // 3 + 240)),
        ('direction. They can be orange,', (SCREEN_WIDTH - 680, SCREEN_HEIGHT // 3 + 280)),
        ('brown, cyan and purple.', (SCREEN_WIDTH - 680, SCREEN_HEIGHT // 3 + 320))
    ]

    # loop through and blit all the texts on the screen
    for message, pos in texts2:
        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)
    # next message, pos

    # loading the image for the color changing spell
    spell_image = pygame.image.load("pictures/color_changin_spell.png")
    # reducing the size of the image
    spell_image = pygame.transform.scale(spell_image, (100, 100))
    # getting the rect of the image
    spell_rect = spell_image.get_rect(center=(SCREEN_WIDTH - 380, SCREEN_HEIGHT // 3))
    # blitting the image on the screen
    screen.blit(spell_image, spell_rect)

    # all the texts for the color changing spell are stored in a list of tuples
    texts3 = [
        ('Color changing spell', (SCREEN_WIDTH - 380, SCREEN_HEIGHT // 3 - 80)),
        ('Touching the', (SCREEN_WIDTH - 380, SCREEN_HEIGHT // 3 + 80)),
        ('spell swaps the', (SCREEN_WIDTH - 380, SCREEN_HEIGHT // 3 + 120)),
        ('twin\'s magical', (SCREEN_WIDTH - 380, SCREEN_HEIGHT // 3 + 160)),
        ('powers and abilities', (SCREEN_WIDTH - 380, SCREEN_HEIGHT // 3 + 200)),
        ('for a limited time', (SCREEN_WIDTH - 380, SCREEN_HEIGHT // 3 + 240))

    ]

    # loop through and blit all the texts on the screen
    for message, pos in texts3:
        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)
    # next message, pos

    # loading the image for the gun
    gun_image = pygame.image.load("pictures/no_gun.png")
    # reducing the size of the image
    gun_image = pygame.transform.scale(gun_image, (100, 100))
    # getting the rect of the image
    gun_rect = gun_image.get_rect(center=(SCREEN_WIDTH - 130, SCREEN_HEIGHT // 3))
    # blitting the image on the screen
    screen.blit(gun_image, gun_rect)
    # all the texts for the gun are stored in a list of tuples
    texts4 = [
        ('Gun', (SCREEN_WIDTH - 130, SCREEN_HEIGHT // 3 - 80)),
        ('The only way to defeat', (SCREEN_WIDTH - 130, SCREEN_HEIGHT // 3 + 80)),
        ('the enemies. Once', (SCREEN_WIDTH - 130, SCREEN_HEIGHT // 3 + 120)),
        ('collected, shooting', (SCREEN_WIDTH - 130, SCREEN_HEIGHT // 3 + 160)),
        ('becomes available', (SCREEN_WIDTH - 130, SCREEN_HEIGHT // 3 + 200)),
        ('for a limited.', (SCREEN_WIDTH - 130, SCREEN_HEIGHT // 3 + 240)),
        ('amount of time.', (SCREEN_WIDTH - 130, SCREEN_HEIGHT // 3 + 280))

    ]

    # loop through and blit all the texts on the screen
    for message, pos in texts4:
        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)
    # next message, pos
    
    draw_back_button(events)
    # loading the image for the back button


    # flipping the display to show the drawn texts and images
    pygame.display.flip()
# end procedure


# Load the back button image and scale it to 50x50 pixels.
back_button_img = pygame.image.load("pictures/Back_button.png")
back_button_img = pygame.transform.scale(back_button_img, (100, 100))


def draw_back_button(events):

    global current_scene
    # Create a rect for the back button image at the desired position.
    screen.blit(back_button_img, (10, 10))
    # Check for clicks on the image.
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x,y = pos[0],pos[1]
  
            if (x > 30 and x < 80) and (y > 20 and y < 70):
                current_scene = "main"
            # end if
        # end if
    # next event
# end prodeure



def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                return quit()
            # end if
        # next event
        

        if current_scene == "main":
            if main_scene(events) == 'back':
                return 'back'
            # end if
            main_scene(events)
        elif current_scene == "player_info":
            player_info_scene(events)
        elif current_scene == "enemy_info":
            enemy_info_scene(events)
        elif current_scene == "lakes_info":
            lakes_info_scene(events)
        elif current_scene == "portals_info":
            other_info_scene(events)
        # end if

        clock.tick(60)

    
    return 
            # end if
    # end while
# end procedure




if __name__ == '__main__':
    main()