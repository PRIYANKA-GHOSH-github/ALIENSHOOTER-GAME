import pygame
from pygame import mixer
import math
import random

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((1300, 900))

# Load background images
background = pygame.image.load("back.jpg")
welcome_page = pygame.image.load("s.png")

# Load and play background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Set the title and icon for the game window
pygame.display.set_caption("Alien Shooter")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player settings
playerimg = pygame.image.load("spaceship.png")
playerx = 630
playery = 800
playerx_change = 0

# Alien settings
alienimg = []
alienx = []
alieny = []
alienx_change = []
alieny_change = []
num_of_aliens = 10

# Initialize multiple aliens
for i in range(num_of_aliens):
    alienimg.append(pygame.image.load("alien.png"))
    alienx.append(random.randint(0, 1300))
    alieny.append(random.randint(40, 150))
    alienx_change.append(2)
    alieny_change.append(50)

# Bullet settings
bulletimg = pygame.image.load("bullet.png")
bulletx = 630
bullety = 800
bulletx_change = 0
bullety_change = 8
bullet_state = "ready"  # "ready" - bullet is not visible, "fire" - bullet is moving

# Score settings
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textx = 10
texty = 10

# Game over text settings
over_font = pygame.font.Font("freesansbold.ttf", 80)
exit_font = pygame.font.Font("freesansbold.ttf", 50)

# Welcome screen text settings
welcome_font = pygame.font.Font("freesansbold.ttf", 80)
instructions_font = pygame.font.Font("freesansbold.ttf", 50)

# Function to show score on the screen
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Function to display game over text
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (405, 400))
    exit_text = exit_font.render("PRESS ENTER TO EXIT THE GAME AND RERUN IT !!", True, (255, 255, 255))
    screen.blit(exit_text, (40, 500))

# Function to fire a bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

# Function to check for collision between bullet and alien
def iscollision(alienx, alieny, bulletx, bullety):
    distance = math.sqrt((math.pow(alienx - bulletx, 2)) + (math.pow(alieny - bullety, 2)))
    return distance < 57

# Function to draw the player on the screen
def player(x, y):
    screen.blit(playerimg, (x, y))

# Function to draw an alien on the screen
def alien(x, y, i):
    screen.blit(alienimg[i], (x, y))

# Function to display the welcome screen
def welcome_screen():
    screen.fill((60, 179, 113))
    screen.blit(welcome_page, (0, 0))
    welcome_text = welcome_font.render("ALIEN SHOOTER", True, (255, 255, 255))
    instructions_text = instructions_font.render("PRESS SPACE TO START", True, (255, 255, 255))
    screen.blit(welcome_text, (300, 300))
    screen.blit(instructions_text, (280, 400))
    pygame.display.update()

# Main game loop
running = False  # Game running state
welcome = True  # Welcome screen state

# Display the welcome screen
while welcome:
    welcome_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            welcome = False
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                welcome = False
                running = True

# Game loop
while running:
    # Fill screen with black color and draw background
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change -= 2
            if event.key == pygame.K_RIGHT:
                playerx_change = +2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
                  #cheat code(by pressing q it automatically increase the value of score +5)   
            if event.key == pygame.K_q:
                score_value += 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # Update player position
    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    elif playerx >= 1236:
        playerx = 1236

    # Alien movement and collision detection
    for i in range(num_of_aliens):
        if alieny[i] > 780:
            for j in range(num_of_aliens):
                alieny[j] = 2000
            game_over_text()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
            break

        alienx[i] += alienx_change[i]
        if alienx[i] <= 0:
            alienx_change[i] = 2
            alieny[i] += alieny_change[i]
        elif alienx[i] >= 1236:
            alienx_change[i] = -2
            alieny[i] += alieny_change[i]

        collision = iscollision(alienx[i], alieny[i], bulletx, bullety)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullety = 800
            bullet_state = "ready"
            score_value += 5
            alienx[i] = random.randint(0, 1235)
            alieny[i] = random.randint(40, 150)

        alien(alienx[i], alieny[i], i)

    # Bullet movement
    if bullety <= 0:
        bullety = 800
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    # Draw player and score on the screen
    player(playerx, playery)
    show_score(textx, texty)
    pygame.display.update()

# Quit Pygame
pygame.quit()
