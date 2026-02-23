class Board:
    # TODO: Handle snake head using direction (^, <, >, v) instead of an S
    # Board is a 10 x 10 array of ints, 0 = Empty space, 1 = Apple, 2 = Snake body
    def __init__(self, appleX, appleY):
        self.appleX = appleX
        self.appleY = appleY
        # Initialize our grid
        self.grid = [[0 for _ in range(10)] for _ in range(10)]
        # Set our apple
        self.grid[appleX][appleY] = 1

    def render(self):
        EMPTY, APPLE, SNAKE, RIGHT = 0, 1, 2, 3
        for row in self.grid:
            for point in row:
                if point == EMPTY:
                    print(" . ", end='')
                if point == APPLE:
                    print(" A ", end='')
                if point == SNAKE:
                    print(" S ", end='')
                if point == RIGHT:
                    print(" > ", end='')

            print()


    # TODO: Perhaps take direction in as an argument? Right now we are just setting to right
    def set_snake_from_deque(self, snake_deque):
        for i in range(len(snake_deque) - 1):
            x, y = snake_deque[i]
            self.grid[x][y] = 2

        # Now Set Head
        i, j = snake_deque[-1]
        self.grid[i][j] = 3
