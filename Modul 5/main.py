# Pygame initialisering og skærmopsætning
import pygame
import os

# Sti til denne fil
STI = os.path.dirname(__file__)

pygame.init()
SCREE_WIDTH = 800
SCREE_HEIGHT = 600
screen = pygame.display.set_mode((SCREE_WIDTH, SCREE_HEIGHT))

# OPGAVE 2 - SÆT TILEMAP KLASSEN IND - OG LOAD ET MAP - HUSK AT TEGNE I GAMELOOP
# kode her

# Spillerkarakter klasse der håndterer visning og bevægelse
class Link(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(STI + "./player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (400, 550)


    # Opdater Link i hver iteration af hovedløkke
    def update(self) -> None:
        # Bevægelseshåndtering baseret på piletaster
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            self.rect.left -= 2
        if key[pygame.K_RIGHT]:
            self.rect.left += 2
        if key[pygame.K_UP]:
            self.rect.top -= 2
        if key[pygame.K_DOWN]:
            self.rect.top += 2


# Sprite initialisering og gruppering
link = Link()
player_group = pygame.sprite.Group()
player_group.add(link)

# Baggrundsgrafik indlæsning og skalering
bg = pygame.image.load(STI + "./baggrund.png")
bg = pygame.transform.scale(bg, (SCREE_WIDTH, SCREE_HEIGHT))

# Framerate håndtering
clock = pygame.time.Clock()

# Gameloop - hovedløkke der kører indtil spillet afsluttes
run = True
while run:
    clock.tick(60) # Sætter frames per sekund til 60
    
    # Tegning af baggrund og karakterer
    screen.blit(bg, (0,0))
    player_group.update()
    player_group.draw(screen)
    
    # Håndtering af spilafslutning
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
