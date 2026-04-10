
A classic Snake game built with Python and Pygame, with a twist! Featuring portal teleportation for Intro to Programming by Abigail Arnold and Maggie Woywod

## Features

- Smooth snake movement with arrow key controls
- **Portal system** — 3 portals on the grid teleport the snake to a random location; portals regenerate after each food pickup
- Score tracking
- Menu screen with animated title
- Game over overlay with restart option

## Requirements

- Python 3.x

## How to Run

 Open terminal in project folder.
1. Download "game.py"
2. Run "python3 -m pip install pygame-ce" in the TERMINAL section, not in the code.
3. Run the code

3. Use:
   Up Arrow = Up
   Left Arrow = Left
   Down Arrow = Down
   Right Arrow = Right


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
