from utils import *


def main():
    input, output = init()

    setAllCells(OFF, output)

    initGame(output)

    game = Thread(target=threadGame, args=(output, ))
    inputs = Thread(target=threadInputs, args=(input, ))
    print = Thread(target=threadPrint, args=(output, ))

    inputs.start()
    game.start()
    print.start()

    inputs.join()
    game.join()
    print.join()

    setAllCells(OFF, output)
    setCell(8, 3, GREEN, output)  # play button
    setCell(8, 4, RED, output)  # quit button

    # Waits for the player to quit or relaunch the game
    exitProgram = False
    while(not exitProgram):
        event = pollEvent(input)
        if (event and event.down):
            if(event.x == 8 and event.y == 3):
                # relaunches the program entirely
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif(event.x == 8 and event.y == 4):
                exitProgram = True

    setAllCells(OFF, output)
    exit()


if __name__ == "__main__":
    main()
