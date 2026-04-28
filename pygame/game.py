import random
import sys
import pygame
import math

# ---------------------------
# Config
# ---------------------------
# Initialize our cell size to 24
CELL_SIZE = 24
# Initialize our grid width to 25 and our grid width to 20
GRID_W, GRID_H = 25, 20
# Multiply grid width and grid height to get the total width and height of our board
WIDTH, HEIGHT = GRID_W * CELL_SIZE, GRID_H * CELL_SIZE
# Set FPS to 12
FPS = 12

# These are tuples of RGB Colors that help pygame draw the correct color in each cell
BG = (18, 18, 22)  # black
GRID = (35, 35, 45)  # blue-gray
SNAKE = (80, 220, 120)  # medium green
SNAKE_HEAD = (40, 255, 140)  # bright green
FOOD = (255, 90, 90)  # red
PORTAL = (120, 120, 255)  # blue
TEXT = (230, 230, 240)  # white

# Our directions:
# Board is a 2 dimensional array
# Coordinates are (x, y), with x being horizontal postion and y being vertial position
# All directions correspond to an arrow key which can be pressed by the user
DIRS = {
    # Modifying y changes vertical position
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    # Modifying x changes horizontal position
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


# ---------------------------
# Helpers
# ---------------------------


# Given a list of "occupied" cells:
# Choose a random cell
# If it is not in the "occupied" list, return that cell
# If the cell is occupied, loop repeats and we test a different cell
# Repeat until we find a cell that is not in "occupied" list
def random_empty_cell(occupied):
    while True:
        cell = (random.randrange(GRID_W), random.randrange(GRID_H))
        if cell not in occupied:
            return cell


# Given a pygame screen, draw a grid
def draw_grid(screen):
    # Draw a vertical line for every cell
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT), 1)
    # Draw a horizontal line for every cell
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y), 1)


# Given a screen, a tuple of coordinates called "cell", a color
# And an inset (default = 2)
def draw_cell(screen, cell, color, inset=2):
    # Unpack tuple "cell" to get coordinates of cell
    x, y = cell
    # Create a rectangle with calculated lengths
    r = pygame.Rect(
        x * CELL_SIZE + inset,
        y * CELL_SIZE + inset,
        CELL_SIZE - 2 * inset,
        CELL_SIZE - 2 * inset,
    )
    # Draw rectangle on the screen
    pygame.draw.rect(screen, color, r, border_radius=6)


# Simply displays "msg" in "font" at x and y coordinate on "screen"
def render_text(screen, font, msg, x, y):
    surf = font.render(msg, True, TEXT)
    screen.blit(surf, (x, y))


# ---------------------------
# Game
# ---------------------------
class SnakeGame:
    # __init__ runs when we create an instance of SnakeGame in main function
    # It basically just sets the default values for a new game
    def __init__(self):
        # Start in menu
        self.state = "menu"
        # Initalize snake as empty list
        self.snake = []
        # Initialize snake direction as right
        self.dir = (1, 0)
        # Next dir will be the same
        self.pending_dir = self.dir
        # Initialize score to zero
        self.score = 0
        # Initialize food to None
        self.food = None
        # Initialize portals as an empty list
        self.portals = []

    def reset(self):
        # cx and cy refer to coordinates at middle of board
        cx, cy = GRID_W // 2, GRID_H // 2
        # Snake is set to middle of the board with two trailing "snake" pieces to the left
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        # Initial direction set to right
        self.dir = (1, 0)
        # Keep going same direction
        self.pending_dir = self.dir
        # Initialize score to 0
        self.score = 0
        # We create a set of "occupied" cells (will contain current snake, food cells, and portal cells)
        # When we want to create a new portal or food cell, we pass this set to
        # the funciton "random_empty_cell" line ~40, which will return a cell that is
        # NOT occupied
        # THIS IS HOW WE MAKE SURE THE PORTALS DONT SPAWN ON TOP OF SNAKE, FOOD, OTHER PORTAL, etc.
        occupied = set(self.snake)

        # Get a random empty cell and put food there
        self.food = random_empty_cell(occupied)
        # Add food to occupied cells
        occupied.add(self.food)

        # create 3 portals
        self.portals = []
        for _ in range(3):
            # Get a random empty cell
            p = random_empty_cell(occupied)
            # Add portal to portals list
            self.portals.append(p)
            # Add portal to occupied cells
            occupied.add(p)

        # Set gamestate to playing
        self.state = "playing"

    # Set the new direction of the snake
    # new_dir is a tuple containing coordinates
    def set_dir(self, new_dir):
        # unpack new_dir to get our change in x and change in y
        dx, dy = new_dir
        # Unpack old direction
        cdx, cdy = self.dir
        # If player tries to go backwards, we fail and exit this function
        # (Snake continues in same direction)
        if (dx, dy) == (-cdx, -cdy):
            return
        # Otherwise, we update pending direction with the new direction
        self.pending_dir = (dx, dy)

    def step(self):
        # Stop if user is not actively playing
        if self.state != "playing":
            return

        # Update direction
        self.dir = self.pending_dir
        # Get current head (first element of snake list)
        hx, hy = self.snake[0]
        # Unpack direction
        dx, dy = self.dir

        # Create new head by adding our change in x and change in y to the current head
        new_head = (hx + dx, hy + dy)

        # If the player hits a wall, the game ends, head must be in range of 0 <-> width and 0 <-> height
        if not (0 <= new_head[0] < GRID_W and 0 <= new_head[1] < GRID_H):
            self.state = "game_over"
            return

        # If the new head is a portal:
        if new_head in self.portals:
            # We create a DIFFERENT set "occupied" that ONLY contains the snake
            occupied = set(self.snake)
            # Then, we pass this "occupied" set to random_empty_cell
            # to make sure the snake doesn't teleport on top of itself
            new_head = random_empty_cell(occupied)

        # If the new head is in the snake "set" (body collision) the game is over
        if new_head in set(self.snake[:-1]):
            self.state = "game_over"
            return

        # Add new head to the snake set
        self.snake.insert(0, new_head)

        # If the new head is a food cell
        if new_head == self.food:
            # Update the score
            self.score += 1
            # Create a DIFFERENT set "occupied" that ONLY contains the snake
            occupied = set(self.snake)
            # Get a random_empty_cell and set that cell to be the new food cell
            self.food = random_empty_cell(occupied)
            # Add that cell to our occupied set
            occupied.add(self.food)

            # Reset portals list
            # (Consuming food will regenerate the portals)
            self.portals = []
            for _ in range(3):
                # Get random empty cell
                p = random_empty_cell(occupied)
                # Add new cell to portals list
                self.portals.append(p)
                # Add new cell to occupied cells set
                occupied.add(p)
        # If the new head is not food, the snake does not grow,
        # so we remove the last snake cell from the snake list
        else:
            self.snake.pop()

    # Draws the screen based on the current game state
    def draw(self, screen, font):
        screen.fill(BG)
        current_time = pygame.time.get_ticks()

        # MENU
        if self.state == "menu":
            # Create fonts "big" and "small"
            big = pygame.font.SysFont("menlo", 56, bold=True)
            small = pygame.font.SysFont("menlo", 20)

            float_offset = int(math.sin(current_time * 0.005) * 10)

            # Draw the title "Snake Game"
            title = big.render("Snake Game", True, TEXT)
            screen.blit(
                title,
                (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100 + float_offset),
            )

            # Draw the start game message
            if (current_time // 500) % 2 == 0:
                msg = small.render("Press SPACE to Start", True, TEXT)
                screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

            # Draw instructions for player
            controls = small.render("Arrow Keys to Move", True, TEXT)
            screen.blit(
                controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT // 2 + 40)
            )
            return

        # If not in menu, draw screen
        draw_grid(screen)

        # Draw food
        draw_cell(screen, self.food, FOOD, inset=4)

        # Draw portals
        for p in self.portals:
            draw_cell(screen, p, PORTAL, inset=4)

        # Draw snake by iterating over all snake coordinates with index i
        for i, cell in enumerate(self.snake):
            # Draw snake head if we are on the first iteration (i==0), otherwise we draw regular snake cell
            draw_cell(screen, cell, SNAKE_HEAD if i == 0 else SNAKE, inset=3)

        # Draw score on the screen
        render_text(screen, font, f"Score: {self.score}", 10, 8)

        # GAME OVER
        # This branch simply displays the game over screen
        if self.state == "game_over":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))

            big = pygame.font.SysFont("menlo", 44, bold=True)
            small = pygame.font.SysFont("menlo", 18)

            s1 = big.render("Game Over", True, TEXT)
            s2 = small.render("Press R to Restart", True, TEXT)

            screen.blit(s1, (WIDTH // 2 - s1.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(s2, (WIDTH // 2 - s2.get_width() // 2, HEIGHT // 2 + 10))


# ---------------------------
# Main
# ---------------------------
def main():
    # Initialize pygame
    pygame.init()
    # Set caption
    pygame.display.set_caption("Snake Final Project")
    # Set our screen that we will draw the game on
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("menlo", 20)

    # Create new snake game instance
    # This will call __init__, which will set default values for the game
    # and set the current game state to "menu"
    game = SnakeGame()

    # Duration of one game step in milliseconds
    tick_ms = int(1000 / FPS)
    # Accumulator tracking elapsed time in milliseconds between game steps
    acc = 0
    # Get last time
    last_time = pygame.time.get_ticks()

    # MAIN GAME LOOP
    while True:
        # Get current time in milliseconds
        now = pygame.time.get_ticks()
        # Calculate the change in time
        dt = now - last_time
        # Update last time
        last_time = now
        # Add elapsed time to the accumulator
        acc += dt

        # For every event that pygame detects on this iteration
        for event in pygame.event.get():
            # If the user quits the game, exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If the user has pressed a key
            if event.type == pygame.KEYDOWN:
                # Start the game if we're in menu and user presses space
                if game.state == "menu":
                    if event.key == pygame.K_SPACE:
                        game.reset()

                # If the gamestate is playing
                elif game.state == "playing":
                    # If the user presses a direction key, then we attempt to update the snake's direction based on the key they pressed
                    if event.key in DIRS:
                        game.set_dir(DIRS[event.key])
                    # If the user pressed the reset button, we reset the game
                    elif event.key == pygame.K_r:
                        game.reset()

                # If the gamestate is gameover
                elif game.state == "game_over":
                    # We listen for the user to press teh reset game
                    if event.key == pygame.K_r:
                        game.reset()

                # We always listen for esacpe key, which will cause the game to exit
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Step the game at a fixed rate; if a frame took longer than one tick,
        # we step multiple times to catch up
        while acc >= tick_ms:
            game.step()
            acc -= tick_ms

        # Then we draw the screen
        game.draw(screen, font)
        # Display the screen
        pygame.display.flip()
        # Cap frame rate at 60 FPS
        clock.tick(60)


if __name__ == "__main__":
    main()
