import pygame
import os
import random

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
pygame.display.set_caption("Tilfældig Tilemap Generator")

# Indlæs tileset
file = STI + '/32x32_map_tile.png'
tileset_image = pygame.image.load(file)
tileset_rect = tileset_image.get_rect()

# Beregn hvor mange fliser der er i tileset
tileset_width = tileset_rect.width // TILE_SIZE
tileset_height = tileset_rect.height // TILE_SIZE
total_tiles = tileset_width * tileset_height

# Udtræk individuelle fliser fra tileset
tiles = []
for y in range(0, tileset_rect.height, TILE_SIZE):
    for x in range(0, tileset_rect.width, TILE_SIZE):
        tile_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        tile = tileset_image.subsurface(tile_rect)
        tiles.append(tile)

# Generer en tilfældig tilemap
tilemap = []
for y in range(MAP_HEIGHT):
    row = []
    for x in range(MAP_WIDTH):
        # Choose a random tile index
        tile_index = random.randint(0, len(tiles) - 1)
        row.append(tile_index)
    tilemap.append(row)

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
            # Press 'r' to regenerate the tilemap
            elif event.key == pygame.K_r:
                # Generate new random tilemap
                for y in range(MAP_HEIGHT):
                    for x in range(MAP_WIDTH):
                        tilemap[y][x] = random.randint(0, len(tiles) - 1)
    
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the tilemap
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile_index = tilemap[y][x]
            screen.blit(tiles[tile_index], 
                        (x * TILE_SIZE, y * TILE_SIZE))
    
    # Update the display
    pygame.display.update()
    clock.tick(60)

# Quit pygame
pygame.quit()