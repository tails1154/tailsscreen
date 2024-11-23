# Example file showing a basic pygame "game loop" with bouncing text
import pygame
from datetime import datetime
import pytz

print("Loading timezone...")
timezonetext = open('timezone.txt', 'rt').read().strip()
timezone = pytz.timezone(timezonetext)
current_datetime = datetime.now()

# pygame setup
pygame.init()
flags = pygame.FULLSCREEN
screen = pygame.display.set_mode((800, 600), flags)
clock = pygame.time.Clock()
running = True

# Text position and velocity
x, y = 400, 300
x_vel, y_vel = 4, 3

# Define font and size
font = pygame.font.Font(None, 50)  # None uses the default system font

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Fill the screen with a color to wipe away anything from the last frame
    screen.fill("black")

    # Update the current date and time
    current_datetime = datetime.now()
    text = timezone.localize(current_datetime).strftime("%m/%d/%Y, %I:%M:%S %p")

    # Create the text surface
    text_surface = font.render(text, True, (255, 255, 255))  # white text
    text_rect = text_surface.get_rect(center=(x, y))

    # Bounce the text off the edges
    if text_rect.left <= 0 or text_rect.right >= screen.get_width():
        x_vel = -x_vel
    if text_rect.top <= 0 or text_rect.bottom >= screen.get_height():
        y_vel = -y_vel

    # Update the text's position
    x += x_vel
    y += y_vel

    # Draw the text
    screen.blit(text_surface, text_rect)

    # Flip the display to update the screen
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)

pygame.quit()
