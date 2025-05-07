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
    image = pygame.transform.scale(image, (32, 32))  # Skalerer billedet til 32x32 pixels
    return image
    #return image.convert_alpha()  # Konverterer billedet til en Surface med alpha-kanal

pygame.init()

# Opsæt tilemap parametre
TILE_SIZE = 32
MAP_WIDTH = 30
MAP_HEIGHT = 20
SCREEN_WIDTH = TILE_SIZE * MAP_WIDTH
SCREEN_HEIGHT = TILE_SIZE * MAP_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def randomCoordinate():
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    return (x, y)

def moveEntity(entity, x, y):
    entity.rect.left += x
    if tiled_map.check_collision(entity.rect):
        entity.rect.left -= x
    entity.rect.top += y
    if tiled_map.check_collision(entity.rect):
        entity.rect.top -= y

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(STI + "./gfx/monster/Idle/frame-1.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = randomCoordinate()
        while tiled_map.check_collision(self.rect):
            self.rect.center = randomCoordinate()

    def update(self) -> None:
        # Fjende bevægelse
        moveEntity(self, random.randint(-2, 2), random.randint(-2, 2))
        if link.rect.left < self.rect.left:
            moveEntity(self, -2, 0)
        if link.rect.left > self.rect.left:
            moveEntity(self, 2, 0)
        if link.rect.top < self.rect.top:
            moveEntity(self, 0, -2)
        if link.rect.top > self.rect.top:
            moveEntity(self, 0, 2)


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
            if tiled_map.check_collision(self.rect):
                self.rect.left += 2
        if key[pygame.K_RIGHT]:
            self.rect.left += 2
            if tiled_map.check_collision(self.rect):
                self.rect.left -= 2
        if key[pygame.K_UP]:
            self.rect.top -= 2
            if tiled_map.check_collision(self.rect):
                self.rect.top += 2
        if key[pygame.K_DOWN]:
            self.rect.top += 2
            if tiled_map.check_collision(self.rect):
                self.rect.top -= 2


        collide_with = pygame.sprite.spritecollide(self, enemy_group, False)
        if collide_with != []:
            for enemy in collide_with:
                enemy_group.remove(enemy)
                enemy.kill()
                enemy_group.add(Enemy())

# TiledMap klasse til at håndtere TMX maps
class TiledMap:
    def __init__(self, tmx_path, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height
        self.tile_size = TILE_SIZE
        self.tmx_data = self.load_tmx_map(tmx_path)
        self.wall_rects = self.get_wall_rects()
    
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
    
    def get_wall_rects(self):
        """
        Extracts wall objects from the 'Walls' layer in the TMX map
        and converts them to pygame.Rect objects for collision detection
        """
        wall_rects = []
        
        # Look for a layer named "Walls"
        for layer in self.tmx_data.layers:
            if layer.name == "Walls":
                # Extract all objects from the Walls layer
                for obj in layer:
                    # Create a pygame.Rect from the object properties
                    rect = pygame.Rect(
                        obj.x, obj.y,
                        obj.width, obj.height
                    )
                    wall_rects.append(rect)
                
                print(f"Loaded {len(wall_rects)} wall objects for collision")
                break
        
        return wall_rects
    
    def check_collision(self, sprite_rect):
        """
        Checks if the provided sprite rectangle collides with any walls
        Returns True if collision detected, False otherwise
        """
        for wall_rect in self.wall_rects:
            if sprite_rect.colliderect(wall_rect):
                return True
        return False
    
# Opret en TiledMap instans
tiled_map = TiledMap(STI + '\\maps\\level1.tmx', MAP_WIDTH, MAP_HEIGHT)

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
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

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
