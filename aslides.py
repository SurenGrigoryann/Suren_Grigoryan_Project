import pygame

# initializing pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
# colors
GRAY = (100, 100, 100)
WHITE = (255,255,255) 


def main():
    # setting up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # loading slide images
    slide_one = pygame.image.load("pictures/slide_one.png")
    slide_two = pygame.image.load("pictures/slide_two.png")
    slide_three = pygame.image.load("pictures/slide_three.png")

    # changing the size of the images
    slide_one = pygame.transform.scale(slide_one, (SCREEN_WIDTH, SCREEN_HEIGHT))
    slide_two = pygame.transform.scale(slide_two, (SCREEN_WIDTH, SCREEN_HEIGHT))
    slide_three = pygame.transform.scale(slide_three, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # a list of all slides
    slides = [slide_one, slide_two, slide_three]
    
    # getting the rect of all images
    slide_one_rect = slide_one.get_rect(center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
    slide_two_rect = slide_one.get_rect(center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
    slide_three_rect = slide_one.get_rect(center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2))

    # a list of all slide rects
    slide_rects = [slide_one_rect,slide_two_rect, slide_three_rect]
    # initial index of slides 
    slide_index = 0

    # creating the next button
    next_button = pygame.image.load("pictures/back_button.png")

    # rotating the back button by 180 degrees, to get the next button
    next_button = pygame.transform.rotate(next_button, 180)
    # reducing the size of the image
    next_button = pygame.transform.scale(next_button, (150,150))
    # getting the rect of the next button
    next_button_rect = next_button.get_rect(center = (1200,600))


    # creating the font for the texts
    font = pygame.font.SysFont('DejaVu Sans', 32)    

    # texts for slide 1
    texts1 = [
        ('The crown was stolen by the witch!', (SCREEN_WIDTH//2, 600)),
    ]

    # texts for slide 2
    texts2 = [
        ('The path to the witch, to reclaim the crown,', (SCREEN_WIDTH//2, 650)),
        ('was swarming with enemies at every turn.', (SCREEN_WIDTH//2, 680))
    ]

    # texts for slide 2
    texts3 = [
        ('Only by combining their unique strengths', (SCREEN_WIDTH//2, 620)),
        ('Could Lory and Mory defeat the witch', (SCREEN_WIDTH//2, 650)),
        ('and reclaim the crown!', (SCREEN_WIDTH//2, 680)),
    ]

    texts_list = [texts1, texts2, texts3]

    running = True
    # main loop
    while running and slide_index<len(slides):

        # blitting the slide images
        screen.blit(slides[slide_index], slide_rects[slide_index])

        for message, pos in texts_list[slide_index]:
            text_surface = font.render(message, True, WHITE)
            text_rect = text_surface.get_rect(center=pos)
            # blitting the texts
            screen.blit(text_surface, text_rect)
        # next message,pos

        # blitting the next button
        screen.blit(next_button, next_button_rect)
        # flipping the screen
        pygame.display.flip()


        # Event processing
        button_clicked = False
        while not button_clicked and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    button_clicked = True  # to break the inner loop
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if next_button_rect.collidepoint(event.pos):
                        button_clicked = True
                    # end if
                # end if
            # next event
        # end while


        # Move to the next slide once the button is clicked

        slide_index += 1
            
    # end if
if __name__ == '__main__':
    main()