import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("5 Levels - Click to Unblock")
SQUARE_SIZE = 100
PADDING = 20

# Calculate starting x so that 5 squares are centered horizontally
TOTAL_WIDTH = 5 * SQUARE_SIZE + 4 * PADDING
start_x = (WIDTH - TOTAL_WIDTH) // 2
y_position = (HEIGHT - SQUARE_SIZE) // 2

# Create 5 level squares, each with a "blocked" state
levels = []
for i in range(5):
    rect = pygame.Rect(start_x + i * (SQUARE_SIZE + PADDING), y_position, SQUARE_SIZE, SQUARE_SIZE)
    levels.append({"rect": rect, "blocked": True})

clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Check each level square for click collision
            for level in levels:
                if level["rect"].collidepoint(pos):
                    level["blocked"] = False

    # Draw background
    SCREEN.fill((30, 30, 30))

    # Draw each level square
    for level in levels:
        # Color changes based on blocked status:
        # Red if blocked, Green if unblocked.
        color = (200, 0, 0) if level["blocked"] else (0, 200, 0)
        pygame.draw.rect(SCREEN, color, level["rect"])
        # Draw a white border around each square
        pygame.draw.rect(SCREEN, (255, 255, 255), level["rect"], 2)

    pygame.display.flip()
    clock.tick(60)