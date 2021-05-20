import pygame
import random

WIDTH = 460
HEIGHT = 480
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame")
player_img = pygame.image.load('Images/357-3576986_2d-spaceship-png-clipart.png')
ball_img = pygame.image.load('Images/Meteor.jpg')
ball_img = pygame.transform.rotate(ball_img, 60)
shootling = pygame.image.load('Images/29779-8-circle-file.png')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 20)

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rect.x -= 10
        elif key[pygame.K_d]:
            self.rect.x += 10
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        for side in ['mid', 'left', 'right']:
            piy = Piy(self.rect.centerx, self.rect.top, side)
            piys.add(piy)

class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ball_img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = -40
        self.speed_y = random.randint(3, 5)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH)
            self.rect.y = -40
        if score >= 500:
            self.speed_y = random.random() * 20
        elif score >= 1000:
            self.speed_y = random.random() * 30

class Piy(pygame.sprite.Sprite):
    def __init__(self, x, y, side):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(shootling, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_bull = -15
        self.side = side

    def update(self):
        self.rect.y += self.speed_bull
        if self.side == 'left':
            self.rect.x -= -self.speed_bull - 14
        if self.side == 'right':
            self.rect.x += -self.speed_bull - 14

        if self.rect.bottom < 0:
            self.kill()

score = 0
font1 = pygame.font.match_font('Comic Sans MS')

def scores(screen, size, text, x, y):
    font = pygame.font.Font(font1, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def draw_hp_bar(screen, x, y, hp):
    lenght = 150
    height = 15
    fill = hp * 30
    outline = pygame.Rect(x, y, lenght, height)
    pygame.draw.rect(screen, (100, 100, 100), outline, 2)
    fill_rect = pygame.Rect(x, y, fill, height)
    pygame.draw.rect(screen, RED, fill_rect)

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()  # Группа спрайтов
player = Player()
all_sprites.add(player)

piys = pygame.sprite.Group()
enemies = pygame.sprite.Group()

for i in range(5):
    enemy = Enemies()
    enemies.add(enemy)

running = True
flags = 0
while running:
    sc.fill(BLACK)
    clock.tick(FPS)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                player.shoot()
    hit = pygame.sprite.spritecollide(player, enemies, True)

    if hit:
        flags += 1
        enemy = Enemies()
        enemies.add(enemy)
    if flags == 5:
        running = False
    if score == 1200:
        running = False

    hits = pygame.sprite.groupcollide(piys, enemies, False, True)

    for i in hits:
        score += 10
        enemy = Enemies()
        enemies.add(enemy)

    all_sprites.update()
    enemies.update()
    piys.update()
    enemies.draw(sc)
    piys.draw(sc)
    all_sprites.draw(sc)
    draw_hp_bar(sc, 40, 40, 5 - flags)
    scores(sc, 24, f"Score: {score}", 400, 40)
    pygame.display.update()
pygame.quit()
