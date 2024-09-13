# effects.py

import pygame
from settings import PURPLE, CYAN, CELL_SIZE

class SpellEffect:
    """Represents the visual effect of a spell being cast."""

    def __init__(self, x, y, radius, duration=30):
        self.x = x
        self.y = y
        self.radius = radius
        self.duration = duration

    def update(self):
        """Update the effect's duration."""
        self.duration -= 1

    def draw(self, screen):
        """Draw the spell effect on the screen."""
        if self.duration > 0:
            pygame.draw.circle(screen, PURPLE, (self.x, self.y), self.radius, 1)

    def is_finished(self):
        """Check if the effect has finished displaying."""
        return self.duration <= 0

class LaserEffect:
    """Represents the visual effect of a laser being fired."""

    def __init__(self, paths, duration=10):
        self.paths = paths
        self.duration = duration

    def update(self):
        """Update the effect's duration."""
        self.duration -= 1

    def draw(self, screen):
        """Draw the laser effect on the screen."""
        if self.duration > 0:
            for path in self.paths:
                for x, y in path:
                    rect = pygame.Rect(
                        x * CELL_SIZE + CELL_SIZE // 3,
                        y * CELL_SIZE + CELL_SIZE // 3,
                        CELL_SIZE // 3,
                        CELL_SIZE // 3
                    )
                    pygame.draw.rect(screen, CYAN, rect)

    def is_finished(self):
        """Check if the effect has finished displaying."""
        return self.duration <= 0
