# character.py

import pygame
from settings import CELL_SIZE, RED, GREEN, COLS, ROWS

class Character:
    """Represents a character in the game, such as the player or an enemy."""

    def __init__(self, x, y, color, health):
        """Initialize the character with position, color, and health."""
        self.x = x
        self.y = y
        self.color = color
        self.health = health
        self.max_health = health
        self.current_weapon = 'sword'  # Default weapon

    def draw(self, screen):
        """Draw the character and its health bar on the screen."""
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, self.color, rect)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        """Draw the health bar above the character."""
        health_ratio = self.health / self.max_health
        bar_width = int(CELL_SIZE * health_ratio)
        bar_height = max(3, CELL_SIZE // 10)
        bar_x = self.x * CELL_SIZE
        bar_y = self.y * CELL_SIZE - bar_height - 2
        background_rect = pygame.Rect(bar_x, bar_y, CELL_SIZE, bar_height)
        health_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, RED, background_rect)
        pygame.draw.rect(screen, GREEN, health_rect)

    def move(self, dx, dy, others):
        """Move the character if possible, checking for collisions."""
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < COLS and 0 <= new_y < ROWS:
            if not self.check_collision(new_x, new_y, others):
                self.x = new_x
                self.y = new_y

    def check_collision(self, new_x, new_y, others):
        """Check for collision with other characters."""
        for other in others:
            if other.is_at(new_x, new_y):
                self.health -= 1
                other.health -= 1
                print(f"Collision! {self} and {other} lose 1 health.")
                return True
        return False

    def is_at(self, x, y):
        """Check if the character is at a specific grid position."""
        return self.x == x and self.y == y

    def attack_with_sword(self, enemies):
        """Attack adjacent enemies with the sword."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            if self.attack_direction(dx, dy, enemies):
                return True
        print("No enemy adjacent to attack.")
        return False

    def attack_direction(self, dx, dy, enemies):
        """Attack in a specific direction."""
        target_x = self.x + dx
        target_y = self.y + dy
        for enemy in enemies:
            if enemy.is_at(target_x, target_y):
                enemy.health -= 2  # Sword damage
                print(f"Sword attack! {enemy} loses 2 health.")
                return True
        return False

    def __repr__(self):
        """String representation of the character."""
        return f"Character(Color: {self.color}, Health: {self.health})"
