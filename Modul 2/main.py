import pygame

pygame.init()

SCREE_WIDTH = 800
SCREE_HEIGHT = 600

screen = pygame.display.set_mode((SCREE_WIDTH, SCREE_HEIGHT))

rectangle = pygame.Rect((300, 250, 50, 50))

run = True
while run:

    # Opdater "Game Window" korrekt
    screen.fill((0, 255, 0))

    pygame.draw.rect(screen, (255, 0, 0), rectangle)
    pygame.draw.circle(screen, (0,0,255), (30,30), 20)

    key = pygame.key.get_pressed()

    if key[pygame.K_UP]:
        rectangle.move_ip(0, -1)
    elif key[pygame.K_DOWN]:
        rectangle.move_ip(0, 1)
    elif key[pygame.K_LEFT]:
        rectangle.move_ip(-1, 0)
    elif key[pygame.K_RIGHT]:
        rectangle.move_ip(1, 0)

    elif key[pygame.K_d]:
        rectangle.width += 1

    elif key[pygame.K_a]:
        rectangle.width += -1

    elif key[pygame.K_w]:
        rectangle.height += -1

    elif key[pygame.K_s]:
        rectangle.height += 1
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
