import random
from board import Board
from snake import Snake

def clearOutput():
    # ANSI clear; if your IDE doesn't like it, comment this out
    print("\033c", end="", flush=True)

def random_apple_not_on_snake(snake_set):
    while True:
        r = random.randint(0, 9)
        c = random.randint(0, 9)
        if (r, c) not in snake_set:
            return r, c

def main():
    snake = Snake()

    ar, ac = random_apple_not_on_snake(snake.snake_set)
    board = Board(ar, ac)

    while True:
        clearOutput()
        board.set_snake_from_deque(snake.get_snake_deque(), snake.direction)
        board.render()
        print("\nWASD to turn (Enter = keep direction). Ctrl+C to quit.")

        key = input("Move: ").strip().lower()

        if key == "w":
            snake.change_direction(Snake.UP)
        elif key == "s":
            snake.change_direction(Snake.DOWN)
        elif key == "a":
            snake.change_direction(Snake.LEFT)
        elif key == "d":
            snake.change_direction(Snake.RIGHT)

        # compute next move
        new_head = snake.next_head()
        nr, nc = new_head

        # wall collision
        if not (0 <= nr <= 9 and 0 <= nc <= 9):
            clearOutput()
            board.render()
            print("\nGame over: hit the wall.")
            return

        # self collision:
        # moving into the tail is allowed ONLY if we are not growing (because tail moves away)
        tail = snake.snake_deque[0]
        growing = (new_head == (board.apple_row, board.apple_col))
        if new_head in snake.snake_set and not (not growing and new_head == tail):
            clearOutput()
            board.render()
            print("\nGame over: ran into yourself.")
            return

        # move snake
        snake.move(grow=growing)

        # if ate apple, spawn new apple
        if growing:
            ar, ac = random_apple_not_on_snake(snake.snake_set)
            board.set_apple(ar, ac)

if __name__ == "__main__":
    main()
    
