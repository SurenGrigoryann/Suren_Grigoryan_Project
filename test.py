import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)

# Menu options
main_menu_options = ["Start Game", "Levels", "Settings", "Quit"]
level_options = ["Level 1", "Level 2", "Level 3", "Level 4"]
selected_option = 0
current_menu = "main"  # Tracks whether we're in the main menu or levels menu

def draw_menu(options):
    screen.fill(BLACK)
    for i, option in enumerate(options):
        if i == selected_option:
            color = GREEN
        else:
            color = WHITE
        text = small_font.render(option, True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60))
        screen.blit(text, text_rect)
    pygame.display.flip()

def main_menu():
    global selected_option, current_menu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(main_menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(main_menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        print("Starting the game...")
                        # Call your game function here
                        # game_loop()
                    elif selected_option == 1:
                        current_menu = "levels"
                        selected_option = 0
                        levels_menu()
                    elif selected_option == 2:
                        print("Opening settings...")
                        # Call your settings function here
                        # settings_menu()
                    elif selected_option == 3:
                        pygame.quit()
                        sys.exit()
        if current_menu == "main":
            draw_menu(main_menu_options)

def levels_menu():
    global selected_option, current_menu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(level_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(level_options)
                elif event.key == pygame.K_RETURN:
                    selected_level = selected_option + 1
                    print(f"Selected Level: {selected_level}")
                    # You can add logic here to load the selected level
                    # load_level(selected_level)
                elif event.key == pygame.K_ESCAPE:
                    current_menu = "main"
                    selected_option = 0
                    return  # Go back to the main menu
        draw_menu(level_options)

if __name__ == "__main__":
    main_menu()