import pygame
import numpy as np
from moviepy.editor import VideoFileClip

# Initialize Pygame
pygame.init()
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Video Background")
clock = pygame.time.Clock()

# Load your video clip using MoviePy (replace with your video file path)
video_path = "path_to_your_video.mp4"
clip = VideoFileClip(video_path)
fps = clip.fps  # Use the video's FPS for smooth playback

# Create an iterator for video frames
frame_generator = clip.iter_frames()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        frame = next(frame_generator)
    except StopIteration:
        # Restart video playback when the video ends
        frame_generator = clip.iter_frames()
        frame = next(frame_generator)

    # Convert the video frame (a NumPy array) to a Pygame surface.
    # MoviePy returns frames in (height, width, channels), but Pygame expects (width, height, channels),
    # so we swap the axes.
    frame_surface = pygame.surfarray.make_surface(np.swapaxes(frame, 0, 1))

    # Optionally, scale the frame to the screen size
    frame_surface = pygame.transform.scale(frame_surface, (screen_width, screen_height))

    # Blit the frame as the background
    screen.blit(frame_surface, (0, 0))
    
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
