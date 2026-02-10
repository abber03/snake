from collections import deque

class Snake:
    def __init__(self):
        self.snake_deque = deque([5, 5], [5, 4], [5, 3])
        self.snake_set = set(self.snake_deque)
    
    # DIRECTIONS:
    RIGHT = (0,1)
    
