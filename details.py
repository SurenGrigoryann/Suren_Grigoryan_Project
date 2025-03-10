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



class Button:
    def __init__(self, center, text, font, padding=20, min_radius=50,
                 bg_color=GRAY, text_color=WHITE, hover_color=DARK_GRAY):
        self.center = center
        self.text = text
        self.font = font
        self.padding = padding
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color

        # Render the text and determine its rectangle.
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=center)
        computed_radius = max(self.text_rect.width, self.text_rect.height) // 2 + self.padding
        self.radius = max(computed_radius, min_radius)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovered(mouse_pos):
            color = self.hover_color
        else:
            color = self.bg_color
            
        pygame.draw.circle(surface, color, self.center, self.radius)
        # Re-center text in case the button is moved.
        self.text_rect = self.text_surface.get_rect(center=self.center)
        surface.blit(self.text_surface, self.text_rect)
        
    def is_hovered(self, pos):
        return ((pos[0] - self.center[0]) ** 2 + (pos[1] - self.center[1]) ** 2) <= self.radius ** 2
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered(event.pos):
                return True
        return False

# Global variable to manage the current scene
current_scene = "main"

# Load the back button image and scale it to 50x50 pixels.
back_button_img = pygame.image.load("back_button.png")
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


def main_scene(events):
    global current_scene
    screen.fill(BROWN)
    font = pygame.font.Font('freesansbold.ttf', 32)
    
    # Define buttons for the main scene.
    buttons = [
        Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200), 'Controls', font),
        Button((SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 100), 'Enemies', font),
        Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100), '  Lakes  ', font),
        Button((SCREEN_WIDTH  * 3 // 4, SCREEN_HEIGHT // 2 + 100), ' Portals ', font)
    ]
    
    # Draw buttons.
    for button in buttons:
        button.draw(screen)
    
    # Check for clicks on buttons.
    for event in events:
        if buttons[0].is_clicked(event):
            current_scene = "player_info"
        if buttons[1].is_clicked(event):
            current_scene = "enemy_info"
        if buttons[2].is_clicked(event):
            current_scene = "lakes_info"
        if buttons[3].is_clicked(event):
            current_scene = "portals_info"

    
    pygame.display.flip()

def player_info_scene(events):
    global current_scene
    screen.fill(DARK_GRAY)
    
    # Use a large font for the heading
    title_font = pygame.font.Font('freesansbold.ttf', 36)
    # Use a smaller font for the enemy details
    info_font = pygame.font.SysFont('DejaVu Sans', 24)

    # Display "enemy info" text at the top
    enemy_text = title_font.render("Control Info", True, (255, 220, 0))  # Gold-like color
    enemy_rect = enemy_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(enemy_text, enemy_rect)




    player1_image = pygame.image.load("red_player.png").convert_alpha()
    player2_image = pygame.image.load("blue_player.png").convert_alpha()

    player1_image = pygame.transform.scale(player1_image, (60, 100))
    player2_image = pygame.transform.scale(player2_image, (60, 100))
    player1_rect = player1_image.get_rect(center=(SCREEN_WIDTH //5, SCREEN_HEIGHT // 3))
    player2_rect = player2_image.get_rect(center=((SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))

    screen.blit(player1_image, player1_rect)
    screen.blit(player2_image, player2_rect)

    # --- Add text for health and speed under each image ---
    # Tank enemy stats
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

    # Loop through and render each text
    for message, pos in texts1:
        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)


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
    
    # Loop through and render each text
    for message, pos in texts2:

        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)




    draw_back_button(events)

    pygame.display.flip()




def enemy_info_scene(events):
    global current_scene
    screen.fill(DARK_GRAY)
    
    # Use a large font for the heading
    title_font = pygame.font.Font('freesansbold.ttf', 36)
    # Use a smaller font for the enemy details
    info_font = pygame.font.Font('freesansbold.ttf', 24)

    # Display "enemy info" text at the top
    enemy_text = title_font.render("Enemy Info", True, (255, 220, 0))  # Gold-like color
    enemy_rect = enemy_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(enemy_text, enemy_rect)

    # --- Load and optionally scale images ---
    tank_image = pygame.image.load("tank.png").convert_alpha()
    fast_image = pygame.image.load("fast_enemy.png").convert_alpha()

    tank_image = pygame.transform.scale(tank_image, (100, 100))
    fast_image = pygame.transform.scale(fast_image, (100, 100))

    # Position each image
    tank_rect = tank_image.get_rect(center=(SCREEN_WIDTH //5, SCREEN_HEIGHT // 3))
    fast_rect = fast_image.get_rect(center=((SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))

    # Blit (draw) the images to the screen
    screen.blit(tank_image, tank_rect)
    screen.blit(fast_image, fast_rect)

    # --- Add text for health and speed under each image ---
    # Tank enemy stats
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

    # Loop through and render each text
    for message, pos in texts:
        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)




    texts = [
        ('Mini-Witch', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 80)),
        ('Health: 5 | Speed: 2', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 80)),
        ('Description:', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 120)),
        ('Witch created milions of copies herself', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 160)),
        ('but smaller and weaker.They are pretty', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 190)),
        ('fast so be ready to fight back!', (SCREEN_WIDTH // 5 + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 220)),
    ]
    
    # Loop through and render each text
    for message, pos in texts:

        text_surface = info_font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)


    # Fast enemy stats
    #fast_stats = "Mini-Witch.\nWitch created milions of copies herself - only smaller and weaker.\nThey are pretty fast so be ready to fight back! \n Health: 5 | Speed: 2"
    #fast_text = info_font.render(fast_stats, True, (230, 230, 230))
    #fast_text_rect = fast_text.get_rect(midtop=(fast_rect.centerx, fast_rect.bottom + 10))
    #screen.blit(fast_text, fast_text_rect)

    # Draw the back button image (replace draw_back_button with your own function)
    draw_back_button(events)

    pygame.display.flip()








def lakes_info_scene(events):
    global current_scene
    screen.fill(DARK_GRAY)
    font = pygame.font.Font('freesansbold.ttf', 32)
    
    # Display "lakes info" text.
    lakes_text = font.render("lakes info", True, WHITE)
    lakes_rect = lakes_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(lakes_text, lakes_rect)
    
    draw_back_button(events)
    
    pygame.display.flip()

def portals_info_scene(events):
    global current_scene
    screen.fill(DARK_GRAY)
    font = pygame.font.Font('freesansbold.ttf', 32)
    info_font = pygame.font.Font('freesansbold.ttf', 24)
    
    # Display "portals info" text.
    portals_text = font.render("portals info", True, WHITE)
    portals_rect = portals_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(portals_text, portals_rect)

    portal_opener_details = ".Oblivion - K17\n One of the favourite robots of the witch. She created them \nto be strong and brutal!\n Do not go head to head with them they will kill you! They are not that fast so you may consider running!\n Health: 10 | Speed: 0.75"
    portal_opener_text = info_font.render(portal_opener_details, True, (230, 230, 230))  # Light gray text
    portal_opener_text = info_font.render(portal_opener_details, True, (230, 230, 230))
    portal_opener_text_rect = portal_opener_text.get_rect(midtop=(portal_opener_text.centerx, portal_opener_text.bottom + 10))
    screen.blit(portal_opener_text, portal_opener_text_rect)




    
    draw_back_button(events)
    
    pygame.display.flip()

def main():
    global current_scene
    clock = pygame.time.Clock()
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                return quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
        # Route to the correct scene based on current_scene.
        if current_scene == "main":
            main_scene(events)
        elif current_scene == "player_info":
            player_info_scene(events)
        elif current_scene == "enemy_info":
            enemy_info_scene(events)
        elif current_scene == "lakes_info":
            lakes_info_scene(events)
        elif current_scene == "portals_info":
            portals_info_scene(events)
        clock.tick(60)
    
    return

if __name__ == '__main__':
    main()



