import os
import pygame

# Intialize the pygame
pygame.init()

# Get the center of the position of the windows video
os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (0,0)
os.environ['SDL_VIDEO_CENTERED'] = '0'

# create the screen
screen = pygame.display.set_mode((800, 600))

player = pygame.sprite.Sprite()
player.rect = pygame.Rect(0,0,64,64)
player.image = pygame.image.load('spaceship.png')

enemy = pygame.sprite.Sprite()
enemy.rect = pygame.Rect(736,0,64,64)
enemy.image = pygame.image.load('enemy.png')


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.rect.x += 2
    enemy.rect.x -= 2
    if pygame.sprite.collide_rect(player, enemy):
        player.rect.x = 0
        enemy.rect.x = 736
    screen.blit(player.image, player.rect)
    screen.blit(enemy.image, enemy.rect)
    pygame.display.update()
    pygame.time.Clock().tick(50)