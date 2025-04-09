import pygame
import sys


def main():
    pygame.init()
# Set up display
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Slide Presentation")

# Load slides and next button image (replace paths with your image files)
slide_one = pygame.image.load("pictures/slide_one.png")
slide_two = pygame.image.load("pictures/slide_two.png")
slide_three = pygame.image.load("pictures/slide_three.png")
slides = [slide_one, slide_two, slide_three]

# Example texts for each slide
font = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
texts1 = [("Slide 1 Text", (320, 240))]
texts2 = [("Slide 2 Text", (320, 240))]
texts3 = [("Slide 3 Text", (320, 240))]
texts_list = [texts1, texts2, texts3]

# Load next button and set its position
next_button = pygame.image.load("pictures/back_button.png")
next_button_rect = next_button.get_rect(topleft=(550, 420))  # adjust coordinates if needed

slide_index = 0
running = True

while running and slide_index < len(slides):
    # Draw the current slide and its text
    screen.blit(slides[slide_index], (0, 0))
    for message, pos in texts_list[slide_index]:
        text_surface = font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)
    pygame.display.flip()

    # Pause for 2 seconds before revealing the next button
    pygame.time.delay(2000)

    # Show the next button and wait for it to be clicked
    button_clicked = False
    while not button_clicked and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                button_clicked = True  # to break out of the inner loop
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if next_button_rect.collidepoint(event.pos):
                    button_clicked = True

        # Draw the slide again so the next button appears on top
        screen.blit(slides[slide_index], (0, 0))
        # Re-draw texts as well
        for message, pos in texts_list[slide_index]:
            text_surface = font.render(message, True, WHITE)
            text_rect = text_surface.get_rect(center=pos)
            screen.blit(text_surface, text_rect)
        # Draw the next button
        screen.blit(next_button, next_button_rect)
        pygame.display.flip()

    # Move to the next slide once the button is clicked
    slide_index += 1

pygame.quit()
sys.exit()






































    # Clear out the current level sprites and lists
    
    previous_map.pop() # getting rid of the pause map
    delete_map()
     
    # Reset the score
    score = 0

    # Reset the timer
    start_time = pygame.time.get_ticks()    
    levels = ['level_one', 'level_two', 'level_three', 'level_four', 'level_five']
    while previous_map.peek() not in levels:
        previous_map.pop
    # Set the current map back to level one so the game resumes there
    return previous_map.pop()
# end procedure
