import pygame.midi as midi
from launchpadbridge.launchpad import *
import sys
from threading import Thread
from queue import Queue
from time import sleep
from random import randint
from enum import Enum


"""
Return a random cell on the grid
(allows to place the ball at the begining of the game)
@param int minX minimum value for x
@param int minX maximum value for x
@param int minY minimum value for y
@param int minY maximum value for y
"""


def getRandomCell(minX: int, maxX: int, minY: int, maxY: int):
    x = randint(minX, maxX)
    y = randint(minY, maxY)
    return x, y


"""
Turns on and off all LEDs quickly to produce a flashing effect
@param Color color color to light the LEDs with
@param int delay delay after wich the LEDs are turned on are off
@param int repeat number of times to flash the LEDs
"""


def flashBoard(out: midi.Output, color: Color, delay: int = 0.5, repeat: int = 1):
    for _ in range(repeat):
        setAllCells(color, out)
        sleep(delay)
        setAllCells(OFF, out)
        sleep(delay)


"""
Initializes all variables to their default values
@param int initialSpeed initial speed of the ball
"""


def initGame(out: midi.Output):
    global play
    global quit
    global winner

    play = False
    quit = False
    winner = "NONE"

    setCell(8, 3, GREEN, out)  # play button
    setCell(8, 4, RED, out)  # quit button


"""
Lights on LEDs according to the current game state
"""


def showGame(out: midi.Output):
    pass


"""
Thread that monitors player inputs while the game is running
"""


def threadInputs(inp: midi.Input, out: midi.Output):
    global barLeft
    global barRight
    global ball
    global play
    global quit

    while(not quit):
        event = pollEvent(inp)
        if (event):
            if (event.down):
                if(event.x == 8 and event.y == 3):
                    if(not play):
                        play = True
                elif(event.x == 8 and event.y == 4):
                    quit = True


def threadPrint(out: midi.Output):
    global quit

    while(not quit):
        showGame(out)

    if(winner == "RED"):
        flashBoard(out, RED, 2, 1)
    elif(winner == "ORANGE"):
        flashBoard(out, ORANGE, 2, 1)
    elif(winner == "NONE"):
        pass
    else:
        print("[ERROR] Winner has an unknown value: " + winner)
        exit(-1)


def threadGame(out: midi.Output, speedDrop: int, speedMin: int):
    global barLeft
    global barRight
    global ball
    global play
    global quit
    global winner

    # Wait for the player to press the play or exit buttons
    while(not play and not quit):
        pass

    setCell(8, 3, OFF, out)  # play button

    while(not quit):
        pass


'''
Global variables that need to be accessed by all threads
'''
play = None
quit = None
winner = None
