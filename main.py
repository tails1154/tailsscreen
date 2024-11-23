# Example file showing a basic pygame "game loop"
import pygame
from datetime import datetime

# getting the current date and time
current_datetime = datetime.now()
# pygame setup
pygame.init()
flags=pygame.FULLSCREEN
screen = pygame.display.set_mode((800, 600), flags)
clock = pygame.time.Clock()
running = True
# Define font and size
font = pygame.font.Font(None, 50)  # None uses the default system font
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running=False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    current_datetime = datetime.now()
    # Create the text surface
    text_surface = font.render(str(current_datetime.strftime("%m/%d/%Y, %H:%M:%S")), True, (255, 255, 255))  # white text

    # Position to display the text
    text_rect = text_surface.get_rect(center=(400, 300))  # center the text
    screen.blit(text_surface, text_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
