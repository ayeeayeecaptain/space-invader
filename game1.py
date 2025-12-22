import pygame as pyg
import random
import math
import os
import sys

pyg.init()

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS  # PyInstaller creates a temp folder with this attribute
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load images using resource_path
bg = pyg.image.load(resource_path('b.jpeg'))
bg2 = pyg.image.load(resource_path('5466730.jpg'))
screen = pyg.display.set_mode((800,600))
pyg.display.set_caption('space invaders')
icon = pyg.image.load(resource_path('ufo.png'))
pyg.display.set_icon(icon)
playerimg = pyg.image.load(resource_path('spaceship.png'))
bulletimg = pyg.image.load(resource_path('bullet.png'))

font = pyg.font.Font(None, 36)
Font = pyg.font.Font(None, 60)

playerx = 370
playery = 480
bulletx = 0
bullety = playery
bullet_change = "ready"

enemyimg1 = [
    pyg.image.load(resource_path('1.png')),
    pyg.image.load(resource_path('2.png')),
    pyg.image.load(resource_path('3.png')),
    pyg.image.load(resource_path('alien.png'))
]
enemy1x = []
enemy1y = []
enemychange = [1.5, 1.5, 1.5, 0.5]
enemychangey = [38, 42, 46, 44]
scores = [1, 2, 2, 1]

num = 4
for i in range(num):
    enemy1x.append(random.randint(0,768))
    enemy1y.append(random.randint(50,150))

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg1[i], (x, y))

def bullet(x, y):
    screen.blit(bulletimg, (x, y + 10))

def is_collisionplayer(x1, y1, x2, y2):
    dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return dist < 36

def is_collision(x1, y1, x2, y2):
    dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return dist < 36

score = 0
game_over = False
running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(text, (20, 20))

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False

    if not game_over:
        player(playerx, playery)
        keys = pyg.key.get_pressed()
        if keys[pyg.K_LEFT] and playerx > 0:
            playerx -= 1
        if keys[pyg.K_RIGHT] and playerx < 736:
            playerx += 1
        if keys[pyg.K_SPACE] and bullet_change == "ready":
            bulletx = playerx
            bullety = playery
            bullet_change = "fire"

        if bullet_change == "fire":
            bullet(bulletx, bullety)
            bullety -= 3
            if bullety <= 0:
                bullet_change = "ready"

        for i in range(num):
            enemy(enemy1x[i], enemy1y[i], i)

            if is_collisionplayer(playerx, playery, enemy1x[i], enemy1y[i]):
                game_over = True

            if is_collision(bulletx, bullety, enemy1x[i], enemy1y[i]) and bullet_change == "fire":
                bullet_change = "ready"
                enemy1x[i] = random.randint(0, 768)
                enemy1y[i] = random.randint(50, 150)
                score += scores[i]

            enemy1x[i] += enemychange[i]
            if enemy1x[i] >= 736:
                enemychange[i] = -abs(enemychange[i])
                enemy1y[i] += enemychangey[i]
            elif enemy1x[i] <= 0:
                enemychange[i] = abs(enemychange[i])
                enemy1y[i] += enemychangey[i]

    else:
        screen.blit(bg2, (0, 0))
        gameover = Font.render("Game Over", True, (255, 255, 255))
        screen.blit(gameover, (300, 250))
        final = Font.render(f'Final Score: {score}', True, (255, 255, 255))
        screen.blit(final, (280, 320))

    pyg.display.update()
