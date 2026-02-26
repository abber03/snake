class Board:
    EMPTY, APPLE, BODY, HEAD_UP, HEAD_LEFT, HEAD_RIGHT, HEAD_DOWN = 0, 1, 2, 3, 4, 5, 6

    def __init__(self, apple_row, apple_col):
        self.apple_row = apple_row
        self.apple_col = apple_col
        self.grid = [[self.EMPTY for _ in range(10)] for _ in range(10)]
        self.grid[self.apple_row][self.apple_col] = self.APPLE

    def set_apple(self, r, c):
        self.apple_row, self.apple_col = r, c

    def clear_snake(self):
        for r in range(10):
            for c in range(10):
                if self.grid[r][c] in (self.BODY, self.HEAD_UP, self.HEAD_LEFT, self.HEAD_RIGHT, self.HEAD_DOWN):
                    self.grid[r][c] = self.EMPTY
        # put apple back
        self.grid[self.apple_row][self.apple_col] = self.APPLE

    def set_snake_from_deque(self, snake_deque, direction):
        """
        snake_deque holds (row, col) pairs, tail at index 0, head at -1
        direction is a tuple: (dr, dc)
        """
        self.clear_snake()

        # body (everything except head)
        for (r, c) in list(snake_deque)[:-1]:
            self.grid[r][c] = self.BODY

        # head
        hr, hc = snake_deque[-1]
        head_code = {
            (-1, 0): self.HEAD_UP,
            (1, 0):  self.HEAD_DOWN,
            (0, -1): self.HEAD_LEFT,
            (0, 1):  self.HEAD_RIGHT,
        }.get(direction, self.HEAD_RIGHT)

        self.grid[hr][hc] = head_code

        # ensure apple still visible
        self.grid[self.apple_row][self.apple_col] = self.APPLE

    def render(self):
        symbols = {
            self.EMPTY:     " . ",
            self.APPLE:     " A ",
            self.BODY:      " o ",
            self.HEAD_UP:   " ^ ",
            self.HEAD_LEFT: " < ",
            self.HEAD_RIGHT:" > ",
            self.HEAD_DOWN: " v ",
        }
        for row in self.grid:
            for cell in row:
                print(symbols.get(cell, " ? "), end="")
            print()
            
