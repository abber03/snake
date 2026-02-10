import time
from board import Board
import random

def main():
    initialAppleX = random.randint(0, 9)
    initialAppleY = random.randint(0, 9)
    gameBoard = Board(initialAppleX, initialAppleY, 10)

    while 1:
        gameBoard.render()
        time.sleep(1)
        print("\033c", end="", flush=True)

main()