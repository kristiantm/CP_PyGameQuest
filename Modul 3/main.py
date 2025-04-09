import pygame

pygame.init()

SCREE_WIDTH = 800
SCREE_HEIGHT = 600

screen = pygame.display.set_mode((SCREE_WIDTH, SCREE_HEIGHT))


# Step 1 - lav en Python klasse til din Sprite

# Step 2 - Initialiser Sprite og Sprite Group

# Step 3 - Tilføj Sprite til Sprite Group

run = True
while run:

    screen.fill((0, 0, 0))

    # Step 4 - kald "draw" metoden på din Sprite gruppe

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
