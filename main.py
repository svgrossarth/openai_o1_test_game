# main.py

import pygame
import sys
import random
from settings import *
from character import Character
from weapons import (
    Bullet, Arrow, cast_spell, place_mine, check_mines, draw_mines, fire_laser
)
from buttons import Button
from effects import SpellEffect, LaserEffect
from utils import draw_grid, remove_dead_characters

def main():
    """Main function to run the game."""
    clock = pygame.time.Clock()
    game_state = 'tutorial'
    while True:
        if game_state == 'tutorial':
            game_state = tutorial_screen(clock)
        elif game_state == 'playing':
            play_game(clock)
            break
        else:
            break

def tutorial_screen(clock):
    """Displays the tutorial screen."""
    font = pygame.font.SysFont(FONT_NAME, 18)
    start_button = Button(WIDTH//2 - 50, HEIGHT - 70, 100, 40, "Start Game", lambda: None)
    running = True
    while running:
        screen.fill(BLACK)
        draw_tutorial_text(screen, font)
        start_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        running = handle_tutorial_events(start_button)
    return 'playing'

def draw_tutorial_text(screen, font):
    """Displays the tutorial text."""
    instructions = [
        "Welcome to the Simple Roguelike Game!",
        "Use arrow keys to move.",
        "Select weapons using the buttons at the bottom.",
        "Sword: Press SPACE to attack adjacent enemies.",
        "Gun: Click on a cell to shoot a bullet.",
        "Bow: Select direction with arrow keys to shoot an arrow.",
        "Spell: Click on a cell to cast a spell.",
        "Mine: Click on a cell to place a mine.",
        "Laser: Press L to fire lasers in all directions.",
    ]
    for idx, line in enumerate(instructions):
        text_surf = font.render(line, True, WHITE)
        screen.blit(text_surf, (20, 20 + idx * 25))

def handle_tutorial_events(start_button):
    """Handle events in the tutorial screen."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.is_clicked(event.pos):
                return False
    return True

def play_game(clock):
    """Runs the main game loop."""
    player, enemies = initialize_characters()
    bullets, arrows = [], []
    spell_effects, laser_effects = [], []
    mines = []
    weapon_buttons = create_weapon_buttons(player)
    player_turn = True
    waiting_for_actions = False
    running = True
    while running:
        screen.fill(BLACK)
        draw_grid(screen)
        draw_game_elements(
            screen, player, enemies, bullets, arrows,
            spell_effects, laser_effects, mines, weapon_buttons
        )
        pygame.display.flip()
        clock.tick(FPS)
        running, player_turn, waiting_for_actions = handle_events(
            player, enemies, bullets, arrows, spell_effects,
            laser_effects, mines, weapon_buttons, player_turn,
            waiting_for_actions, running
        )
        # Update game state and get whether actions are still pending
        waiting_for_actions = update_game_state(
            bullets, arrows, spell_effects, laser_effects, mines, enemies
        )
        if not waiting_for_actions and not player_turn:
            handle_enemies_turn(enemies, player)
            player_turn = True
        if player.health <= 0 or not enemies:
            running = False
    pygame.quit()
    sys.exit()

def initialize_characters():
    """Initialize the player and enemies."""
    player = Character(COLS // 2, ROWS // 2, BLUE, 10)
    enemies = create_enemies(player, 5)
    return player, enemies

def create_enemies(player, num_enemies):
    """Create a list of enemy characters."""
    enemies = []
    for _ in range(num_enemies):
        x, y = get_random_position(player, enemies)
        enemies.append(Character(x, y, RED, 5))
    return enemies

def get_random_position(player, enemies):
    """Get a random position not occupied by player or enemies."""
    while True:
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)
        if not player.is_at(x, y) and all(not e.is_at(x, y) for e in enemies):
            return x, y

def create_weapon_buttons(player):
    """Create and return a list of weapon buttons."""
    button_width = 80
    button_height = 30
    button_y = HEIGHT - button_height - 10
    button_padding = 5
    weapon_names = ['Sword', 'Gun', 'Bow', 'Spell', 'Mine', 'Laser']
    weapon_buttons = []
    for idx, name in enumerate(weapon_names):
        x = button_padding + (button_width + button_padding) * idx
        button = Button(x, button_y, button_width, button_height, name, lambda n=name: select_weapon(n.lower(), player, weapon_buttons))
        weapon_buttons.append(button)
    select_weapon('sword', player, weapon_buttons)
    return weapon_buttons

def select_weapon(weapon_name, player, weapon_buttons):
    """Updates the current weapon and button selection."""
    player.current_weapon = weapon_name
    for button in weapon_buttons:
        button.selected = (button.text.lower() == weapon_name)

def draw_game_elements(
    screen, player, enemies, bullets, arrows,
    spell_effects, laser_effects, mines, weapon_buttons
):
    """Draw all game elements on the screen."""
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for arrow in arrows:
        arrow.draw(screen)
    for effect in spell_effects:
        effect.draw(screen)
    for effect in laser_effects:
        effect.draw(screen)
    draw_mines(screen, mines)
    for button in weapon_buttons:
        button.draw(screen)

def handle_events(
    player, enemies, bullets, arrows, spell_effects,
    laser_effects, mines, weapon_buttons, player_turn,
    waiting_for_actions, running
):
    """Handle user input events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if player_turn and not waiting_for_actions:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if handle_mouse_click(event, player, enemies, bullets, spell_effects, mines, weapon_buttons):
                    player_turn, waiting_for_actions = False, True
            elif event.type == pygame.KEYDOWN:
                if handle_key_press(event, player, enemies, arrows, laser_effects):
                    player_turn, waiting_for_actions = False, True
    return running, player_turn, waiting_for_actions

def handle_mouse_click(event, player, enemies, bullets, spell_effects, mines, weapon_buttons):
    """Handle mouse click events for player actions."""
    mouse_x, mouse_y = event.pos
    for button in weapon_buttons:
        if button.is_clicked((mouse_x, mouse_y)):
            button.callback()
            return False
    return handle_weapon_click(player, enemies, bullets, spell_effects, mines, mouse_x, mouse_y)

def handle_weapon_click(player, enemies, bullets, spell_effects, mines, mouse_x, mouse_y):
    """Handle weapon actions on mouse click."""
    target_x, target_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
    if player.current_weapon == 'gun':
        bullet = Bullet(player.x, player.y, target_x, target_y, speed=5)
        bullets.append(bullet)
        return True
    elif player.current_weapon == 'spell':
        cast_spell(target_x, target_y, enemies)
        effect = SpellEffect(
            x=target_x * CELL_SIZE + CELL_SIZE // 2,
            y=target_y * CELL_SIZE + CELL_SIZE // 2,
            radius=2 * CELL_SIZE
        )
        spell_effects.append(effect)
        return True
    elif player.current_weapon == 'mine':
        place_mine(target_x, target_y, mines)
        return True
    return False

def handle_key_press(event, player, enemies, arrows, laser_effects):
    """Handle keypress events for player actions."""
    if event.key == pygame.K_SPACE and player.current_weapon == 'sword':
        player.attack_with_sword(enemies)
        return True
    elif player.current_weapon == 'bow':
        return handle_bow(event, player, arrows)
    elif player.current_weapon == 'laser' and event.key == pygame.K_l:
        paths = []
        fire_laser(player, enemies, paths)
        effect = LaserEffect(paths)
        laser_effects.append(effect)
        return True
    else:
        return handle_movement(event, player, enemies)

def handle_bow(event, player, arrows):
    """Handle bow shooting direction."""
    direction = get_direction_from_key(event.key)
    if direction:
        arrow = Arrow(player.x, player.y, direction, speed=3, range_limit=15)
        arrows.append(arrow)
        return True
    return False

def get_direction_from_key(key):
    """Get shooting direction from key press."""
    if key == pygame.K_LEFT:
        return (-1, 0)
    elif key == pygame.K_RIGHT:
        return (1, 0)
    elif key == pygame.K_UP:
        return (0, -1)
    elif key == pygame.K_DOWN:
        return (0, 1)
    return None

def handle_movement(event, player, enemies):
    """Handle player movement."""
    dx, dy = get_movement_from_key(event.key)
    if dx != 0 or dy != 0:
        player.move(dx, dy, enemies)
        return True
    return False

def get_movement_from_key(key):
    """Get movement direction from key press."""
    if key == pygame.K_LEFT:
        return -1, 0
    elif key == pygame.K_RIGHT:
        return 1, 0
    elif key == pygame.K_UP:
        return 0, -1
    elif key == pygame.K_DOWN:
        return 0, 1
    return 0, 0

def update_game_state(
    bullets, arrows, spell_effects, laser_effects, mines, enemies
):
    """Update bullets, arrows, and spell effects."""
    update_projectiles(bullets, enemies)
    update_projectiles(arrows, enemies)
    update_effects(spell_effects)
    update_effects(laser_effects)
    check_mines(mines, enemies)
    enemies[:] = remove_dead_characters(enemies)
    # Check if there are any actions still in progress
    waiting_for_actions = (
        bool(bullets) or bool(arrows) or bool(spell_effects) or bool(laser_effects)
    )
    return waiting_for_actions

def update_projectiles(projectiles, enemies):
    """Update projectiles and remove finished ones."""
    for proj in projectiles[:]:
        proj.update(enemies)
        if proj.is_finished():
            projectiles.remove(proj)

def update_effects(effects):
    """Update effects and remove finished ones."""
    for effect in effects[:]:
        effect.update()
        if effect.is_finished():
            effects.remove(effect)

def handle_enemies_turn(enemies, player):
    """Handle the enemies' turn."""
    for enemy in enemies:
        dx, dy = get_enemy_movement(enemy, player)
        others = [player] + [e for e in enemies if e != enemy]
        enemy.move(dx, dy, others)

def get_enemy_movement(enemy, player):
    """Determine enemy movement towards the player."""
    dx = 1 if enemy.x < player.x else -1 if enemy.x > player.x else 0
    dy = 1 if enemy.y < player.y else -1 if enemy.y > player.y else 0
    return dx, dy

if __name__ == "__main__":
    main()
