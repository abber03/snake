. By Abigail and Maggie.

A classic Snake game built with Python and Pygame, featuring portal teleportation for Intro to Programming by Abigail Arnold and Maggie Woywod

## Features

- Smooth snake movement with arrow key controls
- **Portal system** — 3 portals on the grid teleport the snake to a random location; portals regenerate after each food pickup
- Score tracking
- Menu screen with animated title
- Game over overlay with restart option

## Requirements

- Python 3.x

## How to Run

1. Open terminal in project folder.
2. Run:

python main.py

3. Use:
   W = Up
   A = Left
   S = Down
   D = Right

Press Ctrl+C to quit.

## Project Structure

```
game.py       # Main game file (all logic and rendering)
README.md      # This file
```

## Configuration

At the top of `game.py` you can tweak these constants:

| Constant | Default | Description |
|----------|---------|-------------|
| `CELL_SIZE` | `24` | Size of each grid cell in pixels |
| `GRID_W` | `25` | Grid width (columns) |
| `GRID_H` | `20` | Grid height (rows) |
| `FPS` | `12` | Snake movement speed |

All tests should pass.
