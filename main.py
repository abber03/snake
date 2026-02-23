import time
from board import Board
from snake import Snake
import random


def clearOutput():
    print("\033c", end="", flush=True)

def main():
    # Clear output before game starts
    clearOutput()

    # Get random coordinates for first food location
    initialAppleX = random.randint(0, 9)
    initialAppleY = random.randint(0, 9)

    # Create our snake
    snake = Snake()
    snake_deque = snake.get_snake_deque()

    # Create our game board with initial apple location
    gameBoard = Board(initialAppleX, initialAppleY)

    gameBoard.set_snake_from_deque(snake_deque)

    # Game Loop: Render Board, wait for input, clear terminal
    while 1:
        gameBoard.render()
        time.sleep(1)
        clearOutput()

main()
