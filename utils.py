import pygame.midi as midi
from launchpadbridge.launchpad import *
from threading import Thread
from time import sleep
from random import randint


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
    global boxes
    global turn
    global end
    global winner
    global play
    global quit

    boxes = ["N", "N", "N", "N", "N", "N", "N", "N", "N"]
    turn = "G"

    end = False
    winner = "N"
    play = False
    quit = False

    setCell(8, 3, GREEN, out)  # play button
    setCell(8, 4, RED, out)  # quit button

    lightOnGrid(out)


def lightOnGrid(out: midi.Output):
    for i in [2, 5]:
        for j in range(8):
            setCell(i, j, ORANGE_LIGHT, out)
            setCell(j, i, ORANGE_LIGHT, out)


"""
Lights on LEDs according to the current game state
"""


def showGame(out: midi.Output):
    global boxes

    for i in range(len(boxes)):
        if(boxes[i] == "R"):
            turnOnBox(out, i, True)
        elif(boxes[i] == "G"):
            turnOnBox(out, i, False)


"""
Turns on the LEDs in the corresponding box
@param int boxNumber number of the box to light on
@param bool redPlayer if the LEDs need to be light on red, green otherwise

   0  |  1  |  2
   -------------
   3  |  4  |  5
   -------------
   6  |  7  |  8

  0 1 2 3 4 5 6 7
0 * * | * * | * *
1 * * | * * | * *
2 ---------------
3 * * | * * | * *
4 * * | * * | * *
5 ---------------
6 * * | * * | * *
7 * * | * * | * *
"""


def turnOnBox(output: midi.Output, boxNumber: int, redPlayer: bool):
    if(boxNumber == 0):
        setCell(0, 0, RED if(redPlayer) else GREEN, output)
        setCell(0, 1, RED if(redPlayer) else GREEN, output)
        setCell(1, 0, RED if(redPlayer) else GREEN, output)
        setCell(1, 1, RED if(redPlayer) else GREEN, output)
    elif(boxNumber == 1):
        setCell(3, 0, RED if(redPlayer) else GREEN, output)
        setCell(4, 0, RED if(redPlayer) else GREEN, output)
        setCell(3, 1, RED if(redPlayer) else GREEN, output)
        setCell(4, 1, RED if(redPlayer) else GREEN, output)
    elif(boxNumber == 2):
        setCell(6, 0, RED if(redPlayer) else GREEN, output)
        setCell(7, 0, RED if(redPlayer) else GREEN, output)
        setCell(6, 1, RED if(redPlayer) else GREEN, output)
        setCell(7, 1, RED if(redPlayer) else GREEN, output)
    elif(boxNumber == 3):
        setCell(0, 3, RED if(redPlayer) else GREEN, output)
        setCell(1, 3, RED if(redPlayer) else GREEN, output)
        setCell(0, 4, RED if(redPlayer) else GREEN, output)
        setCell(1, 4, RED if(redPlayer) else GREEN, output)
    elif(boxNumber == 4):
        setCell(3, 3, RED if(redPlayer) else GREEN, output)
        setCell(4, 3, RED if(redPlayer) else GREEN, output)
        setCell(3, 4, RED if(redPlayer) else GREEN, output)
        setCell(4, 4, RED if(redPlayer) else GREEN, output)
    elif(boxNumber == 5):
        setCell(6, 3, RED if(redPlayer) else GREEN, output)
        setCell(7, 3, RED if(redPlayer) else GREEN, output)
        setCell(6, 4, RED if(redPlayer) else GREEN, output)
        setCell(7, 4, RED if(redPlayer) else GREEN, output)
    elif(boxNumber == 6):
        setCell(0, 6, RED if(redPlayer) else GREEN, output)
        setCell(1, 6, RED if(redPlayer) else GREEN, output)
        setCell(0, 7, RED if(redPlayer) else GREEN, output)
        setCell(1, 7, RED if(redPlayer) else GREEN, output)
    elif(boxNumber == 7):
        setCell(3, 6, RED if(redPlayer) else GREEN, output)
        setCell(4, 6, RED if(redPlayer) else GREEN, output)
        setCell(3, 7, RED if(redPlayer) else GREEN, output)
        setCell(4, 7, RED if(redPlayer) else GREEN, output)
    elif(boxNumber == 8):
        setCell(6, 6, RED if(redPlayer) else GREEN, output)
        setCell(7, 6, RED if(redPlayer) else GREEN, output)
        setCell(6, 7, RED if(redPlayer) else GREEN, output)
        setCell(7, 7, RED if(redPlayer) else GREEN, output)
    else:
        print("[ERROR] Unknon box was turned on: " + boxNumber)
        exit(-1)


"""
Returns the box number corresponding to the coordinates
@param int x x coordinate
@param int y y coordinate

   0  |  1  |  2
   -------------
   3  |  4  |  5
   -------------
   6  |  7  |  8

  0 1 2 3 4 5 6 7
0 * * | * * | * *
1 * * | * * | * *
2 ---------------
3 * * | * * | * *
4 * * | * * | * *
5 ---------------
6 * * | * * | * *
7 * * | * * | * *
"""


def coordinatesToBox(x: int, y: int):
    if((x == 0 and y == 0) or (x == 0 and y == 1) or (x == 1 and y == 0) or (x == 1 and y == 1)):
        return 0
    elif((x == 3 and y == 0) or (x == 4 and y == 0) or (x == 3 and y == 1) or (x == 4 and y == 1)):
        return 1
    elif((x == 6 and y == 0) or (x == 7 and y == 0) or (x == 6 and y == 1) or (x == 7 and y == 1)):
        return 2
    elif((x == 0 and y == 3) or (x == 1 and y == 3) or (x == 0 and y == 4) or (x == 1 and y == 4)):
        return 3
    elif((x == 3 and y == 3) or (x == 4 and y == 3) or (x == 3 and y == 4) or (x == 4 and y == 4)):
        return 4
    elif((x == 6 and y == 3) or (x == 7 and y == 3) or (x == 6 and y == 4) or (x == 7 and y == 4)):
        return 5
    elif((x == 0 and y == 6) or (x == 1 and y == 6) or (x == 0 and y == 7) or (x == 1 and y == 7)):
        return 6
    elif((x == 3 and y == 6) or (x == 4 and y == 6) or (x == 3 and y == 7) or (x == 4 and y == 7)):
        return 7
    elif((x == 6 and y == 6) or (x == 7 and y == 6) or (x == 6 and y == 7) or (x == 7 and y == 7)):
        return 8
    else:
        return -1


"""
Checks if all the boxes have been filled by the players, meaning that the game is over
"""


def boxesFull():
    global boxes

    for i in range(len(boxes)):
        if(boxes[i] == "N"):
            return False
    return True


"""
Checks if one of the players won the game
by checking all possibilities, including the board beeing full

0  |  1  |  2
-------------
3  |  4  |  5
-------------
6  |  7  |  8
"""


def checkWin():
    global boxes
    global end
    global winner

    if(boxes[0] != "N" and boxes[0] == boxes[1] and boxes[1] == boxes[2]):
        winner = boxes[0]
        end = True
    elif(boxes[3] != "N" and boxes[3] == boxes[4] and boxes[4] == boxes[5]):
        winner = boxes[3]
        end = True
    elif(boxes[6] != "N" and boxes[6] == boxes[7] and boxes[7] == boxes[8]):
        winner = boxes[6]
        end = True
    elif(boxes[0] != "N" and boxes[0] == boxes[3] and boxes[3] == boxes[6]):
        winner = boxes[0]
        end = True
    elif(boxes[1] != "N" and boxes[1] == boxes[4] and boxes[4] == boxes[7]):
        winner = boxes[1]
        end = True
    elif(boxes[2] != "N" and boxes[2] == boxes[5] and boxes[5] == boxes[8]):
        winner = boxes[2]
        end = True
    elif(boxes[0] != "N" and boxes[0] == boxes[4] and boxes[4] == boxes[8]):
        winner = boxes[0]
        end = True
    elif(boxes[2] != "N" and boxes[2] == boxes[4] and boxes[4] == boxes[6]):
        winner = boxes[2]
        end = True
    elif(boxesFull()):
        winner = "E"
        end = True


"""
Thread that monitors player inputs while the game is running
"""


def threadInputs(inp: midi.Input):
    global boxes
    global turn
    global winner
    global play
    global quit

    while(not end and not quit):
        event = pollEvent(inp)
        if (event and event.down):
            if(event.x == 8 and event.y == 3):
                if(not play):
                    play = True
            elif(event.x == 8 and event.y == 4):
                winner = "Q"
                quit = True
            elif(play):
                boxNumber = coordinatesToBox(event.x, event.y)
                if(boxNumber != -1 and boxes[boxNumber] == "N"):
                    boxes[boxNumber] = turn
                    turn = "R" if(turn == "G") else "G"


"""
Thread that prints informations while the game is running
"""


def threadPrint(out: midi.Output):
    global quit

    while(not end and not quit):
        showGame(out)

    if(winner == "R"):
        flashBoard(out, RED, 2, 1)
    elif(winner == "G"):
        flashBoard(out, GREEN, 2, 1)
    elif(winner == "E"):
        flashBoard(out, ORANGE, 2, 1)
    elif(winner != "Q" and winner != "N"):
        print("[ERROR] Winner has an unknown value: ", winner)
        exit(-1)


"""
Thread that handles the game
"""


def threadGame(out: midi.Output):
    global boxes
    global turn
    global end
    global winner
    global play
    global quit

    # Wait for the player to press the play or exit buttons
    while(not play and not quit):
        pass

    setCell(8, 3, OFF, out)  # play button

    while(not end and not quit):
        checkWin()


"""
Global variables that need to be accessed by all threads
"""
boxes = None
turn = None
end = None
winner = None
play = None
quit = None
