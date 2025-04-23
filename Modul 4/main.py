import pygame

pygame.init()

SCREE_WIDTH = 800
SCREE_HEIGHT = 600

screen = pygame.display.set_mode((SCREE_WIDTH, SCREE_HEIGHT))

# Step 1 - Klasse til din Sprite - her en "Link"
class Link(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (400, 550)


    # Step 1 - overskriv "update" metoden her
    def update(self) -> None:
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            self.rect.left -= 2
        if key[pygame.K_RIGHT]:
            self.rect.left += 2
        if key[pygame.K_UP]:
            self.rect.top -= 2
        if key[pygame.K_DOWN]:
            self.rect.top += 2


# Step 2 - Initialiser Sprite og Sprite Group
link = Link()

player_group = pygame.sprite.Group()

# Step 3 - Tilføj Sprite til Sprite Group
player_group.add(link)

bg = pygame.image.load("./baggrund.png")
bg = pygame.transform.scale(bg, (SCREE_WIDTH, SCREE_HEIGHT))

# Initialiser "klokken" til at sætte frames per sekund
clock = pygame.time.Clock()


run = True
while run:
    clock.tick(60) # Sætter frames per sekund til 60
    

    screen.blit(bg, (0,0))

    player_group.update()

    # Step 4 - kald "draw" metoden på din Sprite gruppe
    player_group.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
