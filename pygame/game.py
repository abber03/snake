import random
import sys
import pygame
import math

# ---------------------------
# Config
# ---------------------------
CELL_SIZE = 24
GRID_W, GRID_H = 25, 20
WIDTH, HEIGHT = GRID_W * CELL_SIZE, GRID_H * CELL_SIZE
FPS = 12

BG = (18, 18, 22)
GRID = (35, 35, 45)
SNAKE = (80, 220, 120)
SNAKE_HEAD = (40, 255, 140)
FOOD = (255, 90, 90)
PORTAL = (120, 120, 255)
TEXT = (230, 230, 240)

DIRS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}

# ---------------------------
# Helpers
# ---------------------------
def random_empty_cell(occupied):
    while True:
        cell = (random.randrange(GRID_W), random.randrange(GRID_H))
        if cell not in occupied:
            return cell

def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y), 1)

def draw_cell(screen, cell, color, inset=2):
    x, y = cell
    r = pygame.Rect(
        x * CELL_SIZE + inset,
        y * CELL_SIZE + inset,
        CELL_SIZE - 2 * inset,
        CELL_SIZE - 2 * inset,
    )
    pygame.draw.rect(screen, color, r, border_radius=6)

def render_text(screen, font, msg, x, y):
    surf = font.render(msg, True, TEXT)
    screen.blit(surf, (x, y))

# ---------------------------
# Game
# ---------------------------
class SnakeGame:
    def __init__(self):
        self.state = "menu"
        self.snake = []
        self.dir = (1, 0)
        self.pending_dir = self.dir
        self.score = 0
        self.food = None
        self.portals = []

    def reset(self):
        cx, cy = GRID_W // 2, GRID_H // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.dir = (1, 0)
        self.pending_dir = self.dir
        self.score = 0

        occupied = set(self.snake)

        self.food = random_empty_cell(occupied)
        occupied.add(self.food)

        # create 3 portals
        self.portals = []
        for _ in range(3):
            p = random_empty_cell(occupied)
            self.portals.append(p)
            occupied.add(p)

        self.state = "playing"

    def set_dir(self, new_dir):
        dx, dy = new_dir
        cdx, cdy = self.dir
        if (dx, dy) == (-cdx, -cdy):
            return
        self.pending_dir = (dx, dy)

    def step(self):
        if self.state != "playing":
            return

        self.dir = self.pending_dir
        hx, hy = self.snake[0]
        dx, dy = self.dir

        new_head = (hx + dx, hy + dy)

        # wall collision
        if not (0 <= new_head[0] < GRID_W and 0 <= new_head[1] < GRID_H):
            self.state = "game_over"
            return

        # portal teleport (ANY portal)
        if new_head in self.portals:
            occupied = set(self.snake)
            new_head = random_empty_cell(occupied)

        # body collision
        if new_head in set(self.snake[:-1]):
            self.state = "game_over"
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            occupied = set(self.snake)

            self.food = random_empty_cell(occupied)
            occupied.add(self.food)

            # regenerate portals
            self.portals = []
            for _ in range(3):
                p = random_empty_cell(occupied)
                self.portals.append(p)
                occupied.add(p)
        else:
            self.snake.pop()

    def draw(self, screen, font):
        screen.fill(BG)
        current_time = pygame.time.get_ticks()

        # MENU
        if self.state == "menu":
            big = pygame.font.SysFont("menlo", 56, bold=True)
            small = pygame.font.SysFont("menlo", 20)

            float_offset = int(math.sin(current_time * 0.005) * 10)

            title = big.render("Snake Game", True, TEXT)
            screen.blit(title,
                        (WIDTH // 2 - title.get_width() // 2,
                         HEIGHT // 2 - 100 + float_offset))

            if (current_time // 500) % 2 == 0:
                msg = small.render("Press SPACE to Start", True, TEXT)
                screen.blit(msg,
                            (WIDTH // 2 - msg.get_width() // 2,
                             HEIGHT // 2))

            controls = small.render("Arrow Keys to Move", True, TEXT)
            screen.blit(controls,
                        (WIDTH // 2 - controls.get_width() // 2,
                         HEIGHT // 2 + 40))
            return

        draw_grid(screen)

        # food
        draw_cell(screen, self.food, FOOD, inset=4)

        # portals
        for p in self.portals:
            draw_cell(screen, p, PORTAL, inset=4)

        # snake
        for i, cell in enumerate(self.snake):
            draw_cell(screen, cell, SNAKE_HEAD if i == 0 else SNAKE, inset=3)

        render_text(screen, font, f"Score: {self.score}", 10, 8)

        # GAME OVER
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
    pygame.init()
    pygame.display.set_caption("Snake Final Project")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("menlo", 20)

    game = SnakeGame()

    tick_ms = int(1000 / FPS)
    acc = 0
    last_time = pygame.time.get_ticks()

    while True:
        now = pygame.time.get_ticks()
        dt = now - last_time
        last_time = now
        acc += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game.state == "menu":
                    if event.key == pygame.K_SPACE:
                        game.reset()

                elif game.state == "playing":
                    if event.key in DIRS:
                        game.set_dir(DIRS[event.key])
                    elif event.key == pygame.K_r:
                        game.reset()

                elif game.state == "game_over":
                    if event.key == pygame.K_r:
                        game.reset()

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        while acc >= tick_ms:
            game.step()
            acc -= tick_ms

        game.draw(screen, font)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
