from utils import *


def main():
    input, output = init()

    setAllCells(OFF, output)

    initGame(output)

    game = Thread(target=threadGame, args=(output, ))
    inputs = Thread(target=threadInputs, args=(input, output))
    print = Thread(target=threadPrint, args=(output, ))

    inputs.start()
    game.start()
    print.start()

    inputs.join()
    game.join()
    print.join()

    setAllCells(OFF, output)
    exit(1)


if __name__ == "__main__":
    main()
