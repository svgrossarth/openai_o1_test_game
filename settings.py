# settings.py

import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600  # Increased size to accommodate buttons

# Grid dimensions
ROWS, COLS = 30, 30
CELL_SIZE = WIDTH // COLS

# Frame rate
FPS = 60

# Colors (RGB tuples)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (150, 0, 150)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Font settings
FONT_NAME = None  # Default font
FONT_SIZE = 24

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Roguelike")
