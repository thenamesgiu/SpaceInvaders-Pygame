import random
import math
import pygame

#Inicializar biblioteca pygame
pygame.init()

#Criar e definir dimensões de tela
screen = pygame.display.set_mode((800, 600))

#Carregar imagem de fundo
background = pygame.image.load('background.png')

#Definir ícone e nome
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Definir imagem do player e posições
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

#Definir imagem do inimigo, posições, frequencia de mudança e quantidade
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 12

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50,150))
    enemyY_change.append(40)
    enemyX_change.append(4)

#Definir imagem de bala, mudança, posição e condição para ser lançada
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#Pontuação
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 42)

textX = 10
testY = 10

#Encerrar jogo
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("PONTOS: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("FIM DE JOGO", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


#Loop
running = True
while running:

    #Cor da tela

    screen.fill((0, 0, 0))

    #Imagem de fundo
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Movimento do jogador
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":

                    #Localização atual do jogador
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Movimento do inimigo
    for i in range(num_of_enemies):

        #Encerrar
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        #Sistema de colisão
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    #Movimento das balas
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
