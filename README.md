# Simple Roguelike Game

A simple roguelike game built with Python and Pygame. This game features a player navigating a grid, attacking enemies with various weapons, and avoiding obstacles. The game includes a tutorial screen that explains how to use each weapon before starting.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [How to Run the Game](#how-to-run-the-game)
- [Gameplay Instructions](#gameplay-instructions)
- [Code Overview](#code-overview)
  - [1. `settings.py`](#1-settingspy)
  - [2. `character.py`](#2-characterpy)
  - [3. `weapons.py`](#3-weaponspy)
  - [4. `buttons.py`](#4-buttonspy)
  - [5. `effects.py`](#5-effectspy)
  - [6. `utils.py`](#6-utilspy)
  - [7. `main.py`](#7-mainpy)
- [License](#license)

## Features

- **Grid-based movement**: Navigate a grid as the player character.
- **Multiple weapons**: Choose from several weapons, each with unique mechanics:
  - Sword
  - Gun
  - Bow
  - Spell
  - Mine
  - Laser
- **Enemy AI**: Enemies move towards the player each turn.
- **Visual effects**: Spells and lasers have visual representations.
- **Tutorial screen**: Learn how to play the game before starting.

## Installation

### Prerequisites

- Python 3.x installed on your system.

### Installing Dependencies

1. **Install Pygame**:

   Open your terminal or command prompt and run:

   ```bash
   pip install pygame
   ```

## How to Run the Game

1. **Download the Game Files**:

   Save all the code files (`settings.py`, `character.py`, `weapons.py`, `buttons.py`, `effects.py`, `utils.py`, `main.py`) into a single directory on your local machine.

2. **Navigate to the Project Directory**:

   Open your terminal or command prompt and navigate to the directory containing the game files.

3. **Run the Game**:

   Execute the following command:

   ```bash
   python main.py
   ```

## Gameplay Instructions

- **Tutorial Screen**:

  - Upon launching the game, you will see the tutorial screen with instructions.
  - Read through the instructions to understand how each weapon works.
  - Click the **Start Game** button to begin playing.

- **Movement**:

  - Use the **arrow keys** to move your character (the blue square) one cell per turn.
  - Each movement counts as your turn.

- **Weapon Selection**:

  - Click on the weapon buttons at the bottom of the screen to select your weapon.
  - The selected weapon button is highlighted.

- **Attacking**:

  - **Sword**: Press the **SPACE** bar to attack adjacent enemies.
  - **Gun**: Click on any grid cell to shoot a bullet towards that cell.
  - **Bow**: Press an **arrow key** to shoot an arrow in that direction.
  - **Spell**: Click on any grid cell to cast a spell at that location.
  - **Mine**: Click on any grid cell to place a mine.
  - **Laser**: Press the **L** key to fire lasers in all four directions.

- **Enemies**:

  - Enemies (red squares) move one cell towards you after your turn.
  - If an enemy moves into your cell, both you and the enemy lose 1 health point.

- **Health Bars**:

  - Health bars are displayed above each character.
  - Green indicates current health; red indicates lost health.

- **Winning and Losing**:

  - Defeat all enemies to win.
  - If your health drops to zero, it's game over.

## Code Overview

The game's code is organized into several modules, each responsible for different aspects of the game. Below is a high-level overview of each module.

### 1. `settings.py`

Contains configuration settings and constants used throughout the game, such as:

- Screen dimensions
- Grid dimensions
- Color definitions
- Frame rate
- Font settings
- Initializes the Pygame screen

### 2. `character.py`

Defines the `Character` class, representing both the player and enemy characters.

- **Character Attributes**:
  - Position (`x`, `y`)
  - Color
  - Health
  - Current weapon

- **Character Methods**:
  - `draw(screen)`: Draws the character and health bar on the screen.
  - `move(dx, dy, others)`: Moves the character, checking for collisions.
  - `attack_with_sword(enemies)`: Attacks adjacent enemies with the sword.

### 3. `weapons.py`

Contains classes and functions related to weapons and their mechanics.

- **Bullet Class**:
  - Represents a bullet fired from the gun.
  - Calculates the bullet's path and handles movement and collision.

- **Arrow Class**:
  - Represents an arrow fired from the bow.
  - Moves in a straight line in the chosen direction.

- **Weapon Functions**:
  - `cast_spell(target_x, target_y, enemies)`: Damages enemies within a radius.
  - `place_mine(x, y, mines)`: Places a mine at the specified location.
  - `check_mines(mines, enemies)`: Checks for mine detonations.
  - `draw_mines(screen, mines)`: Draws mines on the screen.
  - `fire_laser(player, enemies, laser_paths)`: Fires lasers in all directions.

### 4. `buttons.py`

Defines the `Button` class for creating clickable UI buttons.

- **Button Attributes**:
  - Position and size
  - Text label
  - Callback function
  - Selection state

- **Button Methods**:
  - `draw(surface)`: Draws the button on the given surface.
  - `is_clicked(pos)`: Checks if the button was clicked.

### 5. `effects.py`

Contains classes for visual effects in the game.

- **SpellEffect Class**:
  - Visual representation of a spell being cast.
  - Draws a circle indicating the area of effect.

- **LaserEffect Class**:
  - Visual representation of lasers being fired.
  - Draws lines along the laser paths.

### 6. `utils.py`

Utility functions used throughout the game.

- `draw_grid(screen)`: Draws the grid lines on the screen.
- `remove_dead_characters(characters)`: Removes characters with zero or negative health.

### 7. `main.py`

The main script that initializes the game and runs the game loop.

- **Main Functions**:
  - `main()`: Entry point of the game.
  - `tutorial_screen(clock)`: Displays the tutorial screen.
  - `play_game(clock)`: Runs the main game loop.
  - `initialize_characters()`: Initializes the player and enemies.
  - `create_weapon_buttons(player)`: Creates weapon selection buttons.
  - `handle_events(...)`: Handles user input and game events.
  - `update_game_state(...)`: Updates the state of projectiles and effects.
  - `handle_enemies_turn(enemies, player)`: Manages enemy movements.

- **Game Loop**:

  - **Event Handling**: Processes user input for movement and weapon usage.
  - **Game State Updates**: Updates positions of bullets, arrows, and other effects.
  - **Rendering**: Draws all game elements on the screen.
  - **Turn Management**: Alternates turns between the player and enemies.