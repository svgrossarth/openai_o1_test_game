# buttons.py

import pygame
from settings import WHITE, BLACK, LIGHT_GRAY, FONT_NAME, FONT_SIZE

class Button:
    """Represents a clickable button in the game UI."""

    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.selected = False
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

    def draw(self, surface):
        """Draw the button on the given surface."""
        color = LIGHT_GRAY if self.selected else WHITE
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        """Check if the button was clicked."""
        return self.rect.collidepoint(pos)
