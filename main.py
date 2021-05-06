#Shmup game(Shoot em up)

import pygame
import random
import os

WIDTH = 480
HEIGHT = 600
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

pygame.init()
score = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup")
clock = pygame.time.Clock()

img_folder = os.path.join(os.path.dirname(__file__), "img")
enemy = pygame.image.load(os.path.join(img_folder, "meteorBrown_big4.png")).convert()
jet = pygame.image.load(os.path.join(img_folder, "playerShip1_orange.png")).convert()
laser = pygame.image.load(os.path.join(img_folder, "laserblue02.png")).convert()
background = pygame.image.load(os.path.join(img_folder, "darkPurple.png")).convert()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = jet
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.x_speed = 0

    def update(self):
        self.x_speed = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_speed = -5
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_speed = 5
        self.rect.x += self.x_speed
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)

    def update(self):
        global score
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 :
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speedx = -self.speedx


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        #Kill the bullet if it goes out of the screen
        if self.rect.bottom < 0:
            self.kill() #Kill command deletes the sprite


player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
run = True
while run:
    clock.tick(FPS)
    #Process input/ Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    #Update
    all_sprites.update()

    #Check to see if mob hit the player
    hit = pygame.sprite.spritecollide(player,mobs,False)
    if hit != []:
        print(score )
        run = False
    #Check to see if bullet hit the mob
    #Different as we are comparing group of bullets with group of mobs
    hitbul = pygame.sprite.groupcollide(bullets, mobs, True, True)
    for dead in hitbul:
        score += 1
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()