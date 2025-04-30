import pygame
import os
import random
import pytmx

# Initialize pygame
pygame.init()

# Get the directory path
STI = os.path.dirname(__file__)

# Opsæt tilemap parametre
TILE_SIZE = 32
MAP_WIDTH = 30
MAP_HEIGHT = 20
SCREEN_WIDTH = TILE_SIZE * MAP_WIDTH
SCREEN_HEIGHT = TILE_SIZE * MAP_HEIGHT

# Opret skærm med de beregnede dimensioner
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sej Tilemap Viser")

# TiledMap klasse til at håndtere TMX maps
class TiledMap:
    def __init__(self, tmx_path, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height
        self.tile_size = TILE_SIZE
        self.tmx_data = self.load_tmx_map(tmx_path)
    
    def load_tmx_map(self, tmx_path):
        try:
            tmx_data = pytmx.load_pygame(tmx_path)
            print(f"Loaded TMX map with {len(tmx_data.layers)} layers")
            return tmx_data
        except Exception as e:
            print(f"Fejl ved indlæsning af TMX fil: {e}")
            return None
    
    def draw(self, surface):
        if not self.tmx_data:
            return
            
        # Loop through all tile layers (skip object layers)
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    # Make sure we're within our map bounds
                    if x < self.map_width and y < self.map_height:
                        # Get the tile image using gid
                        tile = self.tmx_data.get_tile_image_by_gid(gid)
                        if tile:
                            surface.blit(tile, (x * self.tile_size, y * self.tile_size))

# Opret en TiledMap instans
tiled_map = TiledMap(STI + '\\testmap.tmx', MAP_WIDTH, MAP_HEIGHT)

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the tilemap using our class
    tiled_map.draw(screen)
    
    # Update the display
    pygame.display.update()
    clock.tick(60)

# Quit pygame
pygame.quit()