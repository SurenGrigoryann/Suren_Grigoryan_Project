import pygame
import sys

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
    font = pygame.font.Font('freesansbold.ttf', 32)
    
    # Display "player info" text.
    info_text = font.render("player info", True, WHITE)
    info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(info_text, info_rect)
    
    # Create a Back button.
    back_button = Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100), 'Back', font)
    back_button.draw(screen)
    
    for event in events:
        if back_button.is_clicked(event):
            current_scene = "main"
    
    pygame.display.flip()

def enemy_info_scene(events):
    global current_scene
    screen.fill(DARK_GRAY)
    font = pygame.font.Font('freesansbold.ttf', 32)
    
    # Display "enemy info" text.
    enemy_text = font.render("enemy info", True, WHITE)
    enemy_rect = enemy_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(enemy_text, enemy_rect)
    
    # Create a Back button.
    back_button = Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100), 'Back', font)
    back_button.draw(screen)
    
    for event in events:
        if back_button.is_clicked(event):
            current_scene = "main"
    
    pygame.display.flip()

def lakes_info_scene(events):
    global current_scene
    screen.fill(DARK_GRAY)
    font = pygame.font.Font('freesansbold.ttf', 32)
    
    # Display "lakes info" text.
    lakes_text = font.render("lakes info", True, WHITE)
    lakes_rect = lakes_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(lakes_text, lakes_rect)
    
    # Create a Back button.
    back_button = Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100), 'Back', font)
    back_button.draw(screen)
    
    for event in events:
        if back_button.is_clicked(event):
            current_scene = "main"
    
    pygame.display.flip()

def portals_info_scene(events):
    global current_scene
    screen.fill(DARK_GRAY)
    font = pygame.font.Font('freesansbold.ttf', 32)
    
    # Display "portals info" text.
    portals_text = font.render("portals info", True, WHITE)
    portals_rect = portals_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(portals_text, portals_rect)
    
    # Create a Back button.
    back_button = Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100), 'Back', font)
    back_button.draw(screen)
    
    for event in events:
        if back_button.is_clicked(event):
            current_scene = "main"
    
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
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()