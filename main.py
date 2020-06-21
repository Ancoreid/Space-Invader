import pygame
import os
import random
import math

# Inicialize the pygame
pygame.init()

# Get the center of the position of the windows video
os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (0,0)
os.environ['SDL_VIDEO_CENTERED'] = '0'

# Create the screen
width = 900
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.flip()

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_YELLOW = (255, 204, 0)

#Player
playerX = 418
playerY = 500
playerX_change = 0
playerImg = pygame.image.load('spaceship.png')

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyNumber = 6

for i in range(enemyNumber):
    enemyX.append(random.randint(0,836))
    enemyY.append(random.randint(50,100))
    enemyX_change.append(3)
    enemyY_change.append(60)
    enemyImg.append(pygame.image.load('enemy.png'))

# Background Image and Sound
background = pygame.image.load('background.jpg')
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 7
bullet_state = 'ready'
"""READY - You can't seethe bullet on the screen
   FIRE - The bullet is currently moving"""

# Score
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 32)
scoreTextX = 10
scoreTextY = 10

# Game Over Text
gameOverFont = pygame.font.Font("freesansbold.ttf", 64)

#######################################################
def playerDesign(x, y):
    screen.blit(playerImg, (x, y))

def enemyDesign(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 10, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2))) #distance calculation
    if distance < 27:
        return True
    else:
        return False

def showScore(x,y):
    score = font.render("Score: " + str(scoreValue), True, GREEN)
    screen.blit(score, (x,y))

def showGameOverText():
    gameOverText = gameOverFont.render("GAME OVER", True, WHITE)
    screen.blit(gameOverText, (200,250))
#######################################################

# Screen Loop
running = True

while running:
    screen.fill(BLACK)
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement Player
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -3
        elif event.key == pygame.K_RIGHT:
            playerX_change = 3
        if event.key == pygame.K_SPACE:
            bulletSound = pygame.mixer.Sound("laser.wav")
            bulletSound.play()
            bulletX = playerX
            fire_bullet(bulletX, bulletY)
    playerX += playerX_change

    # Player border limits
    if playerX <= 0:
        playerX = 0
    elif playerX >= 836:
        playerX = 836

    # Enemy Loop
    for i in range(enemyNumber):
        # Game Over
        if enemyY[i] > 500:
            for j in range(enemyNumber):
                enemyY[j] = 2000
            showGameOverText()
            break

        # Movement and boundary
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = pygame.mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            scoreValue += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemyDesign(enemyX[i], enemyY[i], i)

    # Movement Bullet
    if bulletY <= 0:
        bulletY = 500
        bullet_state = 'ready'

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    playerDesign(playerX, playerY)
    showScore(scoreTextX, scoreTextY)
    pygame.display.update()