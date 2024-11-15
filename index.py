#########################################
# File Name: index.py
# Description: Pong Game based off starter code for brick breaker game
# Author: Ari Khan
# Date: 11/14/2024
#########################################

#---------------------------------------#
# Import Dependencies                   #
#---------------------------------------#

import pygame
import random
pygame.init()
pygame.font.init()

#---------------------------------------#
# Define Constants                      #
#---------------------------------------#

# Create the Game Window
WIDTH = 800
HEIGHT= 600
gameWindow = pygame.display.set_mode((WIDTH,HEIGHT))

# Define Edges
TOP = 0  
BOTTOM = HEIGHT
LEFT = 0     
RIGHT = WIDTH 

# Define Colors
GREEN = (0,255,0)
DARK_BLUE = (0,0,64)
WHITE = (255,255,255)
BLACK = (0,0,0)

# Define Outline Constant
outline = 0

# Define Font Constant
fontSize = 25
font = pygame.font.SysFont("OCR-A Extended", fontSize)

# Define Ball Constants
ballR = 25
leftPaddleBallStartX = (WIDTH - ballR) // 2 - 300
rightPaddleBallStartX = (WIDTH - ballR) // 2 + 300
ballStartY = (HEIGHT - ballR) // 2

# Define Common Paddle Constant
paddleW = 20

# Define Left Paddle Constants
leftPaddleH = 150
leftPaddleBuffer = 40

# Define Right Paddle Constants
rightPaddleShift = 2
rightPaddleBuffer = 20

# Define Center Line Constants
centerLineThickness = 5
centerLineX = WIDTH // 2

# Define Player Points Counter Constants
player1PointsCounterX = WIDTH // 2 - 50
player2PointsCounterX = WIDTH // 2 + 30
pointsCounterY = TOP + 20
p1WinMessage = font.render("Player 1 Wins!", 1, WHITE)
p2WinMessage = font.render("Player 2 Wins!", 1, WHITE)
winMessageX = WIDTH // 2 - 95
winMessageY = HEIGHT // 2 - 20

# Define SFX Constants
popSound = pygame.mixer.Sound("blip.wav")
popSound.set_volume(1)

# Define Home Screen Constants
homeMessage1 = font.render("Welcome to Pong!", 1, WHITE)
homeMessage2 = font.render("Created by Ari Khan.", 1, WHITE)
homeMessage3 = font.render("Press SPACE to Play.", 1, WHITE)
homeMessage4 = font.render("Press SHIFT for 1.5x Speed.", 1, WHITE)
homeMessage1X = WIDTH // 2 - 125
homeMessage1Y = HEIGHT // 2 - 100

#---------------------------------------#
# Define Variables                      #
#---------------------------------------#

# Define Points Variables
player1Points = 0
player2Points = 0

# Define Player 1 Power Up Variables
leftPaddleShift = 2
player1PowerUpUsed = False

# Define Player 2 Power Up Variables
rightPaddleH = 150
player2PowerUpUsed = False

# Define Ball Speed/Position Variables
ballX = (WIDTH - ballR) // 2
ballY = (HEIGHT - ballR) // 2
speedX =  1
speedY =  1
positiveSpeed = 1
negativeSpeed = -1

# Define Left Paddle Position Variables
leftPaddleX = LEFT - paddleW // 2
leftPaddleY = (BOTTOM - leftPaddleH) // 2

# Define Right Paddle Position Variables
rightPaddleX = WIDTH - paddleW // 2
rightPaddleY = (BOTTOM - rightPaddleH) // 2

# Initiate Game Starting Variables
running = True
inPlay = False
gameFinished = False

#---------------------------------------#
# Main Program                          #
#---------------------------------------#
print("Hit ESC to end the program.")

# Begin Playing Music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(loops = -1)
pygame.time.delay(5)

# Main game loop
while running:
    pygame.event.clear()

    # Home screen Loop
    while inPlay == False and gameFinished == False:
        # Clear events
        pygame.event.clear()

        # Draw home screen elements
        gameWindow.fill(BLACK)
        pygame.draw.line(gameWindow, DARK_BLUE, (centerLineX, TOP), (centerLineX, BOTTOM), centerLineThickness)
        pygame.draw.rect(gameWindow, GREEN, (rightPaddleX, rightPaddleY, paddleW, rightPaddleH), outline)
        pygame.draw.rect(gameWindow, GREEN, (leftPaddleX, leftPaddleY, paddleW, leftPaddleH), outline)
        gameWindow.blit(homeMessage1, (homeMessage1X, homeMessage1Y))
        gameWindow.blit(homeMessage2, (homeMessage1X - 15, homeMessage1Y + 40))
        gameWindow.blit(homeMessage3, (homeMessage1X - 25, homeMessage1Y + 100))
        gameWindow.blit(homeMessage4, (homeMessage1X -75, homeMessage1Y + 140))
        pygame.display.update()
        pygame.time.delay(2)

        # Draw home screen elements
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
            inPlay = False
            gameFinished = True
        if keys[pygame.K_SPACE]:
            inPlay = True
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            inPlay = True
            speedX =  1.5
            speedY =  1.5
            positiveSpeed = 1.5
            negativeSpeed = -1.5

    # Randomly Decide Ball Starting Direction
    speedX = random.choice([positiveSpeed, negativeSpeed])
    speedY = random.choice([positiveSpeed, negativeSpeed])

    while inPlay:
        # Clear events
        pygame.event.clear()
        
        # Draw game elements
        gameWindow.fill(BLACK)
        gameWindow.blit(font.render(str(player1Points), True, WHITE), (player1PointsCounterX, pointsCounterY))
        gameWindow.blit(font.render(str(player2Points), True, WHITE), (player2PointsCounterX, pointsCounterY))
        pygame.draw.line(gameWindow, DARK_BLUE, (centerLineX, TOP), (centerLineX, BOTTOM), centerLineThickness)
        pygame.draw.rect(gameWindow, GREEN, (rightPaddleX, rightPaddleY, paddleW, rightPaddleH), outline)
        pygame.draw.rect(gameWindow, GREEN, (leftPaddleX, leftPaddleY, paddleW, leftPaddleH), outline)
        pygame.draw.circle(gameWindow, WHITE, (ballX, ballY), ballR, outline)
        pygame.display.update()
        pygame.time.delay(2)

        # Handle paddle movement and power-up buttons
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
            inPlay = False
        if keys[pygame.K_UP]:
            rightPaddleY -= rightPaddleShift
        if keys[pygame.K_DOWN]:
            rightPaddleY += rightPaddleShift
        if keys[pygame.K_w]:
            leftPaddleY -= leftPaddleShift
        if keys[pygame.K_s]:
            leftPaddleY += leftPaddleShift
        if keys[pygame.K_SLASH] and player2PowerUpUsed == False:
            rightPaddleH = 250
            player2PowerUpUsed = True
        if keys[pygame.K_e] and player1PowerUpUsed == False:
            leftPaddleShift = 3.5
            player2PowerUpUsed = True

        # Handle Ball collision with paddles
        if (leftPaddleX + leftPaddleBuffer >= ballX) and (leftPaddleY <= ballY <= leftPaddleY + leftPaddleH):
            popSound.play(loops=0)
            speedX = positiveSpeed

        elif (rightPaddleX - rightPaddleBuffer <= ballX) and (rightPaddleY <= ballY <= rightPaddleY + rightPaddleH):
            popSound.play(loops=0)
            speedX = negativeSpeed

        # Handle Ball collision with screen borders and handle points and powerups
        if ballX >= RIGHT:
            ballX = rightPaddleBallStartX
            ballY = ballStartY
            speedX = negativeSpeed
            speedY = random.choice([positiveSpeed, negativeSpeed])
            leftPaddleShift = 2
            player1Points += 1
        elif ballX <= LEFT:
            ballX = leftPaddleBallStartX
            ballY = ballStartY
            speedX = positiveSpeed
            speedY = random.choice([positiveSpeed, negativeSpeed])
            rightPaddleH = 150
            player2Points += 1
        if ballY <= TOP or ballY >= BOTTOM:
            speedY = -speedY

        # Update ball position
        ballX += speedX
        ballY += speedY

        # Check for win condition
        if player1Points == 7 or player2Points == 7:
            inPlay = False
            gameFinished = True

    # Display end game screen
    gameWindow.fill(BLACK)
    pygame.draw.line(gameWindow, DARK_BLUE, (centerLineX, TOP), (centerLineX, BOTTOM), centerLineThickness)
    pygame.draw.rect(gameWindow, GREEN, (rightPaddleX, rightPaddleY, paddleW, rightPaddleH), outline)
    pygame.draw.rect(gameWindow, GREEN, (leftPaddleX, leftPaddleY, paddleW, leftPaddleH), outline)
    gameWindow.blit(font.render(str(player1Points), True, WHITE), (player1PointsCounterX, pointsCounterY))
    gameWindow.blit(font.render(str(player2Points), True, WHITE), (player2PointsCounterX, pointsCounterY))
    
    if player1Points == 7:
        gameWindow.blit(p1WinMessage, (winMessageX, winMessageY))
    elif player2Points == 7:
        gameWindow.blit(p2WinMessage, (winMessageX, winMessageY))
    
    pygame.display.update()
    pygame.time.delay(2)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

#-----------#
pygame.quit()
