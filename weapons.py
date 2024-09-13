# weapons.py

import pygame
import math
from settings import CELL_SIZE, COLS, ROWS, YELLOW, WHITE, ORANGE, CYAN

class Bullet:
    """Represents a bullet fired from the gun."""

    def __init__(self, start_x, start_y, target_x, target_y, speed=5):
        self.path = self.get_line(start_x, start_y, target_x, target_y)
        self.current_step = 0
        self.finished = False
        self.speed = speed
        self.frame_count = 0

    def get_line(self, x0, y0, x1, y1):
        """Calculate the path using Bresenham's Line Algorithm."""
        points = []
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        x, y = x0, y0
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        if dx >= dy:
            err = dx / 2.0
            while x != x1:
                points.append((x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
            points.append((x, y))
        else:
            err = dy / 2.0
            while y != y1:
                points.append((x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
            points.append((x, y))
        return points

    def update(self, enemies):
        """Update the bullet's position and check for collisions."""
        if self.finished:
            return
        self.frame_count += 1
        if self.frame_count >= self.speed:
            self.frame_count = 0
            self.move(enemies)

    def move(self, enemies):
        """Move the bullet along its path."""
        if self.current_step < len(self.path):
            x, y = self.path[self.current_step]
            if self.check_collision(x, y, enemies):
                self.finished = True
                return
            self.current_step += 1
        else:
            self.finished = True

    def check_collision(self, x, y, enemies):
        """Check for collision with enemies."""
        for enemy in enemies:
            if enemy.is_at(x, y):
                enemy.health -= 2  # Bullet damage
                print(f"Bullet hit! {enemy} loses 2 health.")
                return True
        return False

    def draw(self, screen):
        """Draw the bullet on the screen."""
        if self.current_step < len(self.path) and not self.finished:
            x, y = self.path[self.current_step]
            rect = pygame.Rect(
                x * CELL_SIZE + CELL_SIZE // 4,
                y * CELL_SIZE + CELL_SIZE // 4,
                CELL_SIZE // 2,
                CELL_SIZE // 2
            )
            pygame.draw.rect(screen, YELLOW, rect)

    def is_finished(self):
        """Check if the bullet has finished moving."""
        return self.finished

class Arrow:
    """Represents an arrow fired from the bow."""

    def __init__(self, start_x, start_y, direction, speed=3, range_limit=15):
        self.x = start_x
        self.y = start_y
        self.dx, self.dy = direction
        self.speed = speed
        self.frame_count = 0
        self.finished = False
        self.range_limit = range_limit
        self.distance_traveled = 0

    def update(self, enemies):
        """Update the arrow's position and check for collisions."""
        if self.finished:
            return
        self.frame_count += 1
        if self.frame_count >= self.speed:
            self.frame_count = 0
            self.move(enemies)

    def move(self, enemies):
        """Move the arrow in its direction."""
        if self.distance_traveled >= self.range_limit:
            self.finished = True
            return
        new_x, new_y = self.x + self.dx, self.y + self.dy
        if 0 <= new_x < COLS and 0 <= new_y < ROWS:
            self.x, self.y = new_x, new_y
            self.distance_traveled += 1
            self.check_collision(enemies)
        else:
            self.finished = True

    def check_collision(self, enemies):
        """Check for collision with enemies."""
        for enemy in enemies:
            if enemy.is_at(self.x, self.y):
                enemy.health -= 1  # Arrow damage
                print(f"Arrow hit! {enemy} loses 1 health.")

    def draw(self, screen):
        """Draw the arrow on the screen."""
        if not self.finished:
            rect = pygame.Rect(
                self.x * CELL_SIZE + CELL_SIZE // 3,
                self.y * CELL_SIZE + CELL_SIZE // 3,
                CELL_SIZE // 3,
                CELL_SIZE // 3
            )
            pygame.draw.rect(screen, WHITE, rect)

    def is_finished(self):
        """Check if the arrow has finished moving."""
        return self.finished

def cast_spell(target_x, target_y, enemies):
    """Casts a spell to damage enemies within a radius."""
    spell_radius = 2
    spell_damage = 2
    for enemy in enemies:
        distance = math.hypot(enemy.x - target_x, enemy.y - target_y)
        if distance <= spell_radius:
            enemy.health -= spell_damage
            print(f"Spell hit! {enemy} loses {spell_damage} health.")

def place_mine(x, y, mines):
    """Places a mine at the specified location."""
    mine = {'x': x, 'y': y, 'active': True}
    mines.append(mine)
    print("Mine placed at ({}, {})".format(x, y))

def check_mines(mines, enemies):
    """Checks if any enemies step on a mine."""
    for mine in mines[:]:
        if not mine['active']:
            mines.remove(mine)
            continue
        for enemy in enemies:
            if enemy.is_at(mine['x'], mine['y']):
                enemy.health -= 3  # Mine damage
                print(f"Mine exploded! {enemy} loses 3 health.")
                mine['active'] = False

def draw_mines(screen, mines):
    """Draws active mines on the screen."""
    for mine in mines:
        if mine['active']:
            rect = pygame.Rect(
                mine['x'] * CELL_SIZE + CELL_SIZE // 4,
                mine['y'] * CELL_SIZE + CELL_SIZE // 4,
                CELL_SIZE // 2,
                CELL_SIZE // 2
            )
            pygame.draw.rect(screen, ORANGE, rect)

def fire_laser(player, enemies, laser_paths):
    """Fires a laser in all four directions."""
    laser_damage = 2
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    for dx, dy in directions:
        path = []
        x, y = player.x + dx, player.y + dy
        while 0 <= x < COLS and 0 <= y < ROWS:
            path.append((x, y))
            for enemy in enemies:
                if enemy.is_at(x, y):
                    enemy.health -= laser_damage
                    print(f"Laser hit! {enemy} loses {laser_damage} health.")
            x += dx
            y += dy
        laser_paths.append(path)
