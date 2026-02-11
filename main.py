import time
from board import Board
import random


def clearOutput():
    print("\033c", end="", flush=True)

def main():
    # Clear output before game starts
    clearOutput()

    # Get random coordinates for first food location
    initialAppleX = random.randint(0, 9)
    initialAppleY = random.randint(0, 9)

    # Create our game board with initial apple location
    gameBoard = Board(initialAppleX, initialAppleY)

    # Game Loop: Render Board, wait for input, clear terminal
    while 1:
        gameBoard.render()
        time.sleep(1)
        clearOutput()

main()