# Step 1
import pygame

pygame.init()

# Step 2
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Step 3
run = True
while run:

    # Step 4
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
