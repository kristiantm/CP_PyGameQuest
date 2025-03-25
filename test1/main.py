import pygame
import sys
import random

# Skærmens størrelse og spillets hastighed
WIDTH, HEIGHT = 800, 600
FPS = 60

# Størrelse på figurerne
PLAYER_SIZE = 40
NPC_SIZE = 40

# Farver (bruges til NPC’er, questmarkør, baggrund og tekst)
NPC_COLOR = (255, 0, 0)         # Rød
MARKER_COLOR = (255, 255, 0)    # Gul
BACKGROUND_COLOR = (50, 150, 50)  # Grøn
TEXT_COLOR = (255, 255, 255)    # Hvid

# Hvor langt fra kanten quests må placeres
MARGIN = 50

# Spilleren – den figur, du styrer med pilene
class Player:
    def __init__(self, x, y):
        # Indlæs billede til spilleren
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

    def move(self):
        # Flyt spilleren med pil-tasterne
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Sørg for, at spilleren ikke forlader skærmen
        self.rect.x = max(0, min(WIDTH - PLAYER_SIZE, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - PLAYER_SIZE, self.rect.y))

# Quest-objektet – en opgave som spilleren skal fuldføre
class Quest:
    def __init__(self, text, x, y):
        self.text = text
        # En lille gul firkant, som markerer hvor opgaven skal udføres
        self.marker = pygame.Rect(x - 10, y - 10, 20, 20)
        self.completed = False

# NPC – en ven, som giver en quest
class NPC:
    def __init__(self, x, y, id):
        self.rect = pygame.Rect(x, y, NPC_SIZE, NPC_SIZE)
        self.id = id
        self.has_given_quest = False
        self.quest = None

    def give_quest(self):
        if not self.has_given_quest:
            # Vælg et tilfældigt sted til questen
            target_x = random.randint(MARGIN, WIDTH - MARGIN)
            target_y = random.randint(MARGIN, HEIGHT - MARGIN)
            # Vælg en af de fire simple opgave-tekster
            texts = [
                "Find den forsvundne skat",
                "Hent den magiske krystal",
                "Beskyt landsbyen",
                "Find den skjulte dør"
            ]
            text = f"NPC {self.id}: {random.choice(texts)} ved ({target_x}, {target_y})!"
            self.quest = Quest(text, target_x, target_y)
            self.has_given_quest = True
            return self.quest
        return None

# Hoveddelen af spillet
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Eventyrspil")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # Indlæs baggrundsbillede
    background_image = pygame.image.load("background.png").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Opret spilleren i midten af skærmen
    player = Player(WIDTH // 2, HEIGHT // 2)

    # Opret 4 NPC’er på bestemte steder
    npc_positions = [
        (100, 100),
        (WIDTH - 140, 100),
        (100, HEIGHT - 140),
        (WIDTH - 140, HEIGHT - 140)
    ]
    
    # Lav en liste af NPC-objekter, hvor hvert NPC-objekt har en position fra npc_positions og et unikt ID fra enumerate() (fx fra 0 til 3)
    npcs = [NPC(x, y, i) for i, (x, y) in enumerate(npc_positions)]

    current_quest = None  # Den aktive opgave
    quests_done = 0       # Antal opgaver fuldført

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Når SPACE trykkes, kan spilleren snakke med en NPC
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_quest is None:
                        for npc in npcs:
                            # Hvis spilleren er tæt på en NPC, og NPC’en ikke har givet en quest endnu
                            if player.rect.colliderect(npc.rect.inflate(50, 50)) and not npc.has_given_quest:
                                current_quest = npc.give_quest()
                                break

        # Flyt spilleren
        player.move()

        # Tegn baggrunden
        screen.blit(background_image, (0, 0))
                        
        # Tegn spilleren med billedet
        screen.blit(player.image, player.rect)
        # Tegn NPC’erne som røde firkanter
        for npc in npcs:
            pygame.draw.rect(screen, NPC_COLOR, npc.rect)
            # Hvis spilleren er tæt på en NPC, vis en besked "Tryk SPACE"
            if player.rect.colliderect(npc.rect.inflate(50, 50)) and not npc.has_given_quest:
                prompt = font.render("Tryk SPACE", True, TEXT_COLOR)
                screen.blit(prompt, (npc.rect.x, npc.rect.y - 25))

        # Tegn quest-markøren og vis quest-teksten
        if current_quest:
            pygame.draw.rect(screen, MARKER_COLOR, current_quest.marker)
            quest_text = font.render(current_quest.text, True, TEXT_COLOR)
            screen.blit(quest_text, (10, 10))
            
            # Tjek om spilleren kolliderer med quest-markøren
            if player.rect.colliderect(current_quest.marker):
                current_quest.completed = True
                current_quest = None
                quests_done += 1

        # Vis hvor mange quests der er fuldført
        status = font.render(f"Quests: {quests_done}/4", True, TEXT_COLOR)
        screen.blit(status, (10, 40))

        # Hvis alle quests er fuldførte, vis en vinderbesked
        if quests_done >= 4:
            win = font.render("Du vandt!", True, TEXT_COLOR)
            screen.blit(win, (WIDTH // 2 - win.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
