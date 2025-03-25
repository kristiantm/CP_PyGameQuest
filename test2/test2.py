import pygame

# Initialize PyGame
pygame.init()
pygame.mixer.init() # Initialize sound

# Window settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zelda Adventure")

# --- Asset Loading ---
try:
    player_img = pygame.image.load("player.png").convert_alpha()
    grass_tile_img = pygame.image.load("grass_tile.png").convert()
    block_tile_img = pygame.image.load("block_tile.png").convert()
    water_tile_img = pygame.image.load("water_tile.png").convert()
    npc_img = pygame.image.load("npc.png").convert_alpha()
    item_img = pygame.image.load("item.png").convert_alpha()
    enemy_img = pygame.image.load("enemy.png").convert_alpha()
    sword_sound = pygame.mixer.Sound("sword.mp3")  # Load sound file.  Replace with your sound file.
except pygame.error as e:
    print(f"Error loading assets: {e}")
    pygame.quit()
    import sys
    sys.exit()

# --- Game Variables ---
# Player
player_x, player_y = 100, 100
player_speed = 5
player_direction = 0  # 0: right, 1: down, 2: left, 3: up
player_frame = 0

# Map
WATER_TILE = 0
GRASS_TILE = 1
BLOCK_TILE = 2
map_data = [
    [WATER_TILE, WATER_TILE, WATER_TILE, WATER_TILE, WATER_TILE, WATER_TILE, WATER_TILE, WATER_TILE, WATER_TILE, WATER_TILE],
    [WATER_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, WATER_TILE],
    [WATER_TILE, GRASS_TILE, BLOCK_TILE, BLOCK_TILE, GRASS_TILE, GRASS_TILE, BLOCK_TILE, BLOCK_TILE, GRASS_TILE, WATER_TILE],
    [WATER_TILE, GRASS_TILE, BLOCK_TILE, BLOCK_TILE, GRASS_TILE, GRASS_TILE, BLOCK_TILE, BLOCK_TILE, GRASS_TILE, WATER_TILE],
    [WATER_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, WATER_TILE],
    [WATER_TILE, GRASS_TILE, BLOCK_TILE, BLOCK_TILE, GRASS_TILE, GRASS_TILE, BLOCK_TILE, BLOCK_TILE, GRASS_TILE, WATER_TILE],
    [WATER_TILE, GRASS_TILE, BLOCK_TILE, BLOCK_TILE, GRASS_TILE, GRASS_TILE, BLOCK_TILE, BLOCK_TILE, GRASS_TILE, WATER_TILE],
    [WATER_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, GRASS_TILE, WATER_TILE],
    [WATER_TILE, WATER_TILE, WATER_TILE, WATER_TILE, WATER_TILE, WATER_TILE, WATER_TILE, WATER_TILE, WATER_TILE, WATER_TILE],
]
tile_size = 50

# NPC
npc_x, npc_y = 300, 300
npc_rect = npc_img.get_rect(topleft=(npc_x, npc_y))
dialogue = ["Hello, adventurer!", "Can you find my lost item?", "It's somewhere in the forest.", "Thanks!"]
dialogue_index = 0
show_dialogue = False
interaction_distance = 50

# Quest
item_x, item_y = 550, 250
item_rect = item_img.get_rect(topleft=(item_x, item_y))
item_collected = False
quest_active = False
quest_completed = False

# Enemy
enemy_x, enemy_y = 600, 400
enemy_rect = enemy_img.get_rect(topleft=(enemy_x, enemy_y))
enemy_health = 100
player_attack_damage = 20
enemy_attack_damage = 10
attacking = False
attack_timer = 0
attack_cooldown = 30
ENEMY_SPEED = 2

# Font
font = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)

# --- Helper Functions ---
def draw_map():
    for row_index, row in enumerate(map_data):
        for col_index, tile_value in enumerate(row):
            if tile_value == GRASS_TILE:
                screen.blit(grass_tile_img, (col_index * tile_size, row_index * tile_size))
            elif tile_value == BLOCK_TILE:
                screen.blit(block_tile_img, (col_index * tile_size, row_index * tile_size))
            elif tile_value == WATER_TILE:
                screen.blit(water_tile_img, (col_index * tile_size, row_index * tile_size))

def check_collision(rect):
    tile_row = rect.y // tile_size
    tile_col = rect.x // tile_size
    if 0 <= tile_row < len(map_data) and 0 <= tile_col < len(map_data[0]):
        return map_data[tile_row][tile_col] == BLOCK_TILE
    return False

def draw_text(text, x, y):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x, y))

def draw_health_bar(health, x, y):
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 100, 10))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, health, 10))

# --- Main Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Player Movement ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        player_direction = 2
        player_frame += 0.1
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        player_direction = 0
        player_frame += 0.1
    if keys[pygame.K_UP]:
        player_y -= player_speed
        player_direction = 3
        player_frame += 0.1
    if keys[pygame.K_DOWN]:
        player_y += player_speed
        player_direction = 1
        player_frame += 0.1

    # Keep player on screen
    player_x = max(0, min(player_x, WIDTH - player_img.get_width()))
    player_y = max(0, min(player_y, HEIGHT - player_img.get_height()))

    # --- Collision Detection ---
    player_rect = player_img.get_rect(topleft=(player_x, player_y))
    if check_collision(player_rect):
        if keys[pygame.K_LEFT]:
            player_x += player_speed
        if keys[pygame.K_RIGHT]:
            player_x -= player_speed
        if keys[pygame.K_UP]:
            player_y += player_speed
        if keys[pygame.K_DOWN]:
            player_y -= player_speed

    # --- NPC Interaction ---
    distance_to_npc = ((player_x - npc_x) ** 2 + (player_y - npc_y) ** 2) ** 0.5
    if distance_to_npc < interaction_distance and keys[pygame.K_SPACE]:
        show_dialogue = True

    # --- Quest System ---
    if dialogue_index == 2 and distance_to_npc < interaction_distance and keys[pygame.K_SPACE]:
        quest_active = True
        dialogue_index = 3

    if quest_active and not item_collected:
        if player_rect.colliderect(item_rect):
            item_collected = True
            quest_active = False

    if item_collected and not quest_completed:
        draw_text("Item collected! Return to NPC.", 100, 550)
        if distance_to_npc < interaction_distance and keys[pygame.K_SPACE]:
            quest_completed = True
            item_collected = False

    # --- Enemy AI ---
    if not attacking:
        if enemy_x < player_x:
            enemy_x += ENEMY_SPEED
        elif enemy_x > player_x:
            enemy_x -= ENEMY_SPEED
        if enemy_y < player_y:
            enemy_y += ENEMY_SPEED
        elif enemy_y > player_y:
            enemy_y -= ENEMY_SPEED
        enemy_rect.topleft = (enemy_x, enemy_y)

    # --- Player Attack ---
    if keys[pygame.K_a] and not attacking:
        attacking = True
        attack_timer = attack_cooldown
        pygame.mixer.Sound.play(sword_sound)
        if player_rect.colliderect(enemy_rect):
            enemy_health -= player_attack_damage
            if enemy_health <= 0:
                enemy_x = -100
                enemy_y = -100
                enemy_health = 0

    if attacking:
        attack_timer -= 1
        if attack_timer <= 0:
            attacking = False

    # --- Enemy Attack ---
    if enemy_rect.colliderect(player_rect) and not attacking:
        print("Player hit by enemy!")

    # --- Drawing ---
    screen.fill((0, 0, 0))
    draw_map()
    screen.blit(player_img, (player_x, player_y))
    screen.blit(npc_img, (npc_x, npc_y))
    if quest_active and not item_collected:
        screen.blit(item_img, (item_x, item_y))
    screen.blit(enemy_img, (enemy_x, enemy_y))
    draw_health_bar(enemy_health, enemy_x, enemy_y - 20)
    if show_dialogue:
        draw_text(dialogue[dialogue_index], 100, 500)
    if quest_completed:
        draw_text("Quest complete!", 100, 550)

    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Cap frame rate

pygame.quit()
