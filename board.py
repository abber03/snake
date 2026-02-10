class Board:
    # Board is a 10 x 10 array of ints, 0 = Empty space, 1 = Apple, 2 = Snake body
    def __init__(self, appleX, appleY):
        self.appleX = appleX
        self.appleY = appleY
        # Initialize our grid
        self.grid = [[0 for _ in range(10)] for _ in range(10)]
        # Set our apple
        self.grid[appleX][appleY] = 1

    def render(self):
        EMPTY, APPLE, SNAKE = 0, 1, 2
        for row in self.grid:
            for point in row:
                if point == EMPTY:
                    print(" . ", end='')
                if point == APPLE:
                    print(" A ", end='')
                if point == SNAKE:
                    print(" S ", end='')

            print()