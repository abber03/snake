from collections import deque

class Snake:
    # DIRECTIONS:
    RIGHT = (0,1)
    LEFT = (0, -1)
    UP = (-1, 0)
    DOWN = (1, 0)

    def __init__(self):
        """ Initializes the snake with a starting body. The snake is represented using:
        - a deque to maintain order (head at the right end)
        - a set for fast collision detection"""

        # Each tuple represents a (row, column) position
        self.snake_deque = deque([
            (5, 3),
            (5, 4),
            (5, 5)
        ])

        # Set version of the snake body for O(1) collision checks
        self.snake_set = set(self.snake_deque)

        # Initial direction of movement
        self.direction = Snake.RIGHT

    def move(self):
        """ Moves the snake one step in the current direction. This does not yet handle food or wall collisions."""

        head_row, head_col = self.snake_deque[-1]
        dir_row, dir_col = self.direction

        # Calculate new head position
        new_head = (head_row + dir_row, head_col + dir_col)

        # Add new head
        self.snake_deque.append(new_head)
        self.snake_set.add(new_head)

        # Remove tail (normal movement)
        tail = self.snake_deque.popleft()
        self.snake_set.remove(tail)

    def change_direction(self, new_direction):
        """ Changes the direction of the snake. This method prevents reversing directly into itself."""

        # Prevent the snake from reversing direction
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def get_snake_deque(self):
        return self.snake_deque
