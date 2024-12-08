#!.venv/bin/python3.12

##################################
### Python TicTacToe by Tobian ###
##################################

# based on: https://pythongeeks.org/python-tic-tac-toe-game/
# please report any bug on github: 

# Imports
from config import *
import numpy
import pygame
import math

# Variables
Player = 0
Gameover = False
Inmenu = True

# Functions
# Game itself
def PrintBoard():
    flippedboard = numpy.flip(Board, 0)
    print(flippedboard)
    print("")

def DrawBoard():
    DrawLines()
    DrawFigures()

def DrawLines():
    for i in range(BoardSize):
        if i == 0: continue
        Axis = SquareSize * i
        pygame.draw.line(Screen, LineColor, (0, Axis), (ScreenSize, Axis), 10)
        pygame.draw.line(Screen, LineColor, (Axis, 0), (Axis, ScreenSize), 10)

def DrawFigures():
    for col in range(BoardSize):
        for row in range(BoardSize):
            if Board[row][col] == 1:
                pygame.draw.circle(Screen, CircleColor, (int(col * SquareSize + SquareSize / 2), int(row * SquareSize + SquareSize / 2)), CircleRadius, LineWidth)
            elif Board[row][col] == 2:
                pygame.draw.line(Screen, XColor, (col * SquareSize + offset, row * SquareSize + offset), (col * SquareSize + SquareSize - offset, row * SquareSize + SquareSize - offset), LineWidth)
                pygame.draw.line(Screen, XColor, (col * SquareSize + offset, row * SquareSize + SquareSize - offset), (col * SquareSize + SquareSize - offset, row * SquareSize + offset), LineWidth)

def FullBoard():
    for col in range(BoardSize):
        for row in range(BoardSize):
            if Board[row][col] == 0:
                return False
    return True

def AvailableSquare(row, col):
    is_available = Board[row][col] == 0
    return is_available

def MarkSquare(row, col, Player):
    Board[row][col] = Player    

# Win Checking
def Win(Player): 
    BoardDR = numpy.array(Board)
    BoardDL = numpy.array(Board)
    for i in range(BoardSize): BoardDR[i] = numpy.roll(Board[i], i * -1)
    for i in range(BoardSize): BoardDL[i] = numpy.roll(Board[i], i * 1)

    StreakH = 0
    StreakV = 0
    StreakDR = 0
    StreakDL = 0
    
    # Win detection
    for foo in range(BoardSize): # foo = Y (column)
        StreakH = 0
        StreakV = 0 
        StreakDR = 0
        StreakDL = 0
        for moo in range(BoardSize): # moo = x (row)
            # Horizontal
            if Board[foo][moo] == Player:
                StreakH += 1
            else: StreakH = 0
            # Vertical
            if Board[moo][foo] == Player:
                StreakV += 1
            else: StreakV = 0
            # Diagonal (Same as Vertical but the Board is shifted)
            if BoardDR[moo][foo] == Player:
                StreakDR += 1
            else: StreakDR = 0
            if BoardDL[moo][foo] == Player:
                StreakDL += 1
            else: StreakDL = 0

            # Check if the Player won
            if StreakH >= WinSize:
                DrawHorizontalLine(foo, Player)
                return True
            if StreakV >= WinSize:
                DrawVerticalLine(foo, Player)
                return True
            if StreakDR >= WinSize:
                if DrawDiagonalLine(moo, foo, Player, WinSize, Direction = "Right"):
                    return True
            elif StreakDL >= WinSize:
                if DrawDiagonalLine(moo, foo, Player, WinSize, Direction = "Left"):
                    return True

    return False

# Mark Win
def DrawVerticalLine(col, Player):
    posX = col * SquareSize + SquareSize / 2
    if Player == 1:
        pygame.draw.line(Screen, CircleColor, (posX, 10), (posX, ScreenSize - 10), LineWidth)
    else:
        pygame.draw.line(Screen, XColor, (posX, 10), (posX, ScreenSize - 10), LineWidth)
        
def DrawHorizontalLine(row, Player):
    posY = row * SquareSize + SquareSize / 2
    if Player == 1:
        pygame.draw.line(Screen, CircleColor, (10, posY), (ScreenSize - 10, posY), LineWidth)
    else:
        pygame.draw.line(Screen, XColor, (10, posY), (ScreenSize - 10, posY), LineWidth)

def DrawDiagonalLine(row, col, Player, WinSize, Direction):
    # Calculate from which squares the line has to be drawn
    if Direction == "Right":
        for i in range(row):
            if col == BoardSize:
                col = 0
            col += 1
        Scol = col - (WinSize - 1)
    elif Direction == "Left":
        for i in range(row):
            if col == 0:
                col = BoardSize
            col -= 1
        Scol = col + (WinSize - 1)
    Srow = row - (WinSize - 1)
    # Check if calculated squares are inside the board
    if col >= BoardSize or row >= BoardSize: return False
    if Scol >= BoardSize or row >= BoardSize: return False
    # Calculate the positions
    if Direction == "Right":
        X1 = col * SquareSize + (SquareSize * 0.9)
        Y1 = row * SquareSize + (SquareSize * 0.9)
        X2 = Scol * SquareSize + (SquareSize * 0.1)
        Y2 = Srow * SquareSize + (SquareSize * 0.1)
    elif Direction == "Left":
        X1 = col * SquareSize + (SquareSize * 0.1)
        Y1 = row * SquareSize + (SquareSize * 0.9)
        X2 = Scol * SquareSize + (SquareSize * 0.9)
        Y2 = Srow * SquareSize + (SquareSize * 0.1)

    # Draw the line
    if Player == 1:
        pygame.draw.line(Screen, CircleColor, (X1, Y1), (X2, Y2), LineWidth)
    else:
        pygame.draw.line(Screen, XColor, (X1, Y1), (X2, Y2), LineWidth)
    return True
            
# PyGame window
Board = numpy.zeros((BoardSize, BoardSize))
pygame.init()
pygame.display.set_caption("TicTacToe by Tobian")
Screen = pygame.display.set_mode((ScreenSize, ScreenSize))
Screen.fill(BackgroundColor)
pygame.display.update()
DrawLines()

# The Game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and not Gameover:
            yPosition = event.pos[1]
            row = int(math.floor(yPosition / SquareSize))
            xPosition = event.pos[0]
            col = int(math.floor(xPosition / SquareSize))
            if Player % 2 == 0:
                if AvailableSquare(row, col):
                    MarkSquare(row, col, 1)
                    if Win(1):
                        Gameover = True
                    Player += 1
            else:
                if AvailableSquare(row, col):
                    MarkSquare(row, col, 2)
                    if Win(2):
                        Gameover = True
                    Player += 1
            if FullBoard():
                Gameover = True
    DrawFigures()
    pygame.display.update()

# Can be removed if wished
print("Have fun playing! :)")
