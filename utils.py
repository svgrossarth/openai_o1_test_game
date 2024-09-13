# utils.py

import pygame
from settings import WIDTH, HEIGHT, CELL_SIZE, GRAY

def draw_grid(screen):
    """Draws the grid lines on the screen."""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def remove_dead_characters(characters):
    """Removes characters with health less than or equal to zero."""
    return [char for char in characters if char.health > 0]
