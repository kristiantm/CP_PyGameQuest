# Pygame initialisering og skærmopsætning
import pygame
import os
import pytmx
import random

# Sti til denne fil
STI = os.path.dirname(__file__)

def load_image(filename: str) -> pygame.Surface:
    """
    Indlæser et billede fra den angivne sti og returnerer det som en pygame Surface.
    """
    image = pygame.image.load(os.path.join(STI, filename))
    return image
    #return image.convert_alpha()  # Konverterer billedet til en Surface med alpha-kanal

pygame.init()

# Opsæt tilemap parametre
TILE_SIZE = 32
MAP_WIDTH = 30
MAP_HEIGHT = 20
SCREEN_WIDTH = TILE_SIZE * MAP_WIDTH
SCREEN_HEIGHT = TILE_SIZE * MAP_HEIGHT

SCREE_WIDTH = 800
SCREE_HEIGHT = 600
screen = pygame.display.set_mode((SCREE_WIDTH, SCREE_HEIGHT))

screen = pygame.display.set_mode((SCREE_WIDTH, SCREE_HEIGHT))

def randomCoordinate():
    x = random.randint(0, SCREE_WIDTH)
    y = random.randint(0, SCREE_HEIGHT)
    return (x, y)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(STI + "./gfx/monster/Idle/frame-1.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = randomCoordinate()

    def update(self) -> None:
        pass
        # if self.image == MONSTER_1_A:
        #     self.image = MONSTER_1_B
        # else:
        #     self.image = MONSTER_1_A

# Spillerkarakter klasse der håndterer visning og bevægelse
class Link(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("gfx/player.png")
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


        collide_with = pygame.sprite.spritecollide(self, enemy_group, False)
        if collide_with != []:
            for enemy in collide_with:
                enemy.rect.center = randomCoordinate()

# TiledMap klasse til at håndtere TMX maps
class TiledMap:
    def __init__(self, tmx_path, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height
        self.tile_size = TILE_SIZE
        self.tmx_data = self.load_tmx_map(tmx_path)
    
    def load_tmx_map(self, tmx_path):
        tmx_data = pytmx.load_pygame(tmx_path)
        print(f"Loaded TMX map with {len(tmx_data.layers)} layers")
        return tmx_data
    
    def draw(self, surface):
        # Loop through all tile layers (skip object layers)
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    # Get the tile image using gid
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tile_size, y * self.tile_size))

# Opret en TiledMap instans
tiled_map = TiledMap(STI + '\\tiles\\testmap.tmx', MAP_WIDTH, MAP_HEIGHT)

# Sprite initialisering og gruppering
link = Link()
player_group = pygame.sprite.Group()
player_group.add(link)

# Sprite gruppe til fjender
enemy_group = pygame.sprite.Group()
for i in range(4):
    enemy = Enemy()
    enemy_group.add(enemy)

# Baggrundsgrafik indlæsning og skalering
bg = load_image("gfx/baggrund.png")
bg = pygame.transform.scale(bg, (SCREE_WIDTH, SCREE_HEIGHT))

# Framerate håndtering
clock = pygame.time.Clock()

# Gameloop - hovedløkke der kører indtil spillet afsluttes
run = True
while run:
    # Sætter frames per sekund til 60
    clock.tick(60) 

    # Rensning af skærmen ved at farve den sort
    screen.blit(bg, (0,0))

   # Tegning af tilemap (baggrund)
    tiled_map.draw(screen)

    # Opdatering af sprites for spiller og fjender (bevægelse og kollision)
    player_group.update()
    enemy_group.update()

    # Tegning af sprites for spiller og fjender
    player_group.draw(screen)
    enemy_group.draw(screen)


    # Håndtering af spilafslutning
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Opdatering af skærmen for at vise ændringerne
    pygame.display.update()


# Afslut pygame og ryd op
pygame.quit()
