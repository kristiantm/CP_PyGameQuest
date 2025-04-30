import pygame
import random

pygame.init()

clock = pygame.time.Clock()

SCREE_WIDTH = 800
SCREE_HEIGHT = 600
BG = pygame.image.load("./gfx/bg.png")
BG = pygame.transform.scale(BG, (SCREE_WIDTH, SCREE_HEIGHT))

LINK = pygame.image.load("./gfx/player.png")
LINK = pygame.transform.scale(LINK, (50, 50))

MONSTER_1_A = pygame.image.load("./gfx/monster/Idle/frame-1.png")
MONSTER_1_A = pygame.transform.scale(MONSTER_1_A, (50, 50))
# MONSTER_1_B = pygame.image.load("./gfx/monster/Idle/frame-2.png")
# MONSTER_1_B = pygame.transform.scale(MONSTER_1_B, (50, 50))

screen = pygame.display.set_mode((SCREE_WIDTH, SCREE_HEIGHT))

def randomCoordinate():
    x = random.randint(0, SCREE_WIDTH)
    y = random.randint(0, SCREE_HEIGHT)
    return (x, y)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = MONSTER_1_A
        self.rect = self.image.get_rect()
        self.rect.center = randomCoordinate()

    def update(self) -> None:
        pass
        # if self.image == MONSTER_1_A:
        #     self.image = MONSTER_1_B
        # else:
        #     self.image = MONSTER_1_A

# Step 1 - Klasse til din Sprite - her et "Spaceship"
class Link(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = LINK
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

        collide_with = pygame.sprite.spritecollide(self, enemy_group, False)
        if collide_with != []:
            for enemy in collide_with:
                enemy.rect.center = randomCoordinate()

        


# Step 2 - Initialiser Sprite og Sprite Group
link = Link()

player_group = pygame.sprite.Group()

# Step 3 - Tilføj Sprite til Sprite Group
player_group.add(link)

enemy_group = pygame.sprite.Group()
for i in range(4):
    enemy = Enemy()
    enemy_group.add(enemy)

run = True
while run:

    screen.blit(BG, (0,0) )
    
    clock.tick(60)

    player_group.update()
    enemy_group.update()

    # Step 4 - kald "draw" metoden på din Sprite gruppe
    player_group.draw(screen)
    enemy_group.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
