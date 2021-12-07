# -*- coding: utf-8 -*-
"""
RPG.
"""
from random import randint
from getch import getch
from map_loader import load_map
from tiles import display_tiles
from monsters import Monster, MapMonster, start_fight
from importlib import import_module
import json
import time
import colorama; colorama.init()
from colorama import Fore
import sys
#from playsound import playsound

# Loading options
with open("options.json", "r") as f:
    options = json.load(f)
# Loading translations
with open(f"translations/{options['lang']}.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

# Available chars, by lighting
chars = "▓▒░҈ ŦÝԬ"
pos_of_chars = "00020122"
player_icons = "←↑↓→"
player_direction = 1
player_pos = [5, 5]
playable_area = (20, 10)
inventory = [
    ["", ""],
    [translations["main"]["inventory"]["health"], 15, 15],
    [translations["main"]["inventory"]["items"], []],
    [translations["main"]["inventory"]["XP"], 0],
    [translations["main"]["inventory"]["level"], 0]
]
inventory_keys = [item[0] for item in inventory]
monsters = [Monster("Ϡ", 3, 4, True, True, 9, 5)]
monsters_on_map = []
# Loading the chapter, and catching if it doesn't exist
try:
    with open("current_chapter.sav") as f:
        current_chapter = f.read().replace("\n", "")
    with open("chapters.json") as f:
        current_chapter = json.load(f)[current_chapter]
        player_pos = current_chapter[1]
except FileExistsError:
    print(translations['main']['save_files_not_found'])
    sys.exit(1)
except KeyError:
    print(translations['main']['unexisting_chapter'])
    sys.exit(1)

# Tilemapping, consists of a 2D list of tuples, first element of the tuple is the solidness ID of the tile
# and second is the speed at which the player can travel through (-1 is collider)
TILES = load_map(f"maps/{current_chapter[0]}/tileset")
# We load the actions of the map
actions = getattr(import_module(f"maps.{current_chapter[0]}.map_actions"), "actions")

# Setting framerate cap vars
last_frame_executed = 0

# Printing console size message
print("\n"*20)
for i in range(playable_area[0]):
    if i == playable_area[0] // 2:
        print(f"|   {translations['main']['console_size']}")
    else:
        print("|")
getch()


# Game loop
running = True
while running:
    # Maximum 60 frames per second
    if time.time() - last_frame_executed < 1/15: continue

    # Tiles displaying
    display_tiles(TILES, playable_area, player_pos, chars, player_icons, player_direction, pos_of_chars, monsters, monsters_on_map, inventory)
        
    user_input = getch()
    
    # Qutting
    if user_input == "n":
        user_input = input(translations['main']['quit_msg'] + " ? (y/n) ")
        if user_input.lower().startswith("y"):
            running = False
        continue
    
    # Player movement
    old_player_pos = player_pos.copy()
    if user_input == "z":
        player_pos[0] -= 1
        player_direction = 1
    elif user_input == "s": 
        player_pos[0] += 1
        player_direction = 2
    elif user_input == "q":
        player_pos[1] -= 1
        player_direction = 0
    elif user_input == "d":
        player_pos[1] += 1
        player_direction = 3
        
    # Checking if the list is not out of bounds
    if player_pos[0] < 0: player_pos[0] = 0
    elif player_pos[0] >= len(TILES): player_pos[0] = len(TILES) - 1
    elif player_pos[1] < 0: player_pos[1] = 0
    elif player_pos[1] >= len(TILES[0]): player_pos[1] = len(TILES[0]) - 1
    
    # If the player collides with a monster, we start the fight
    if (player_pos[0], player_pos[1]) in tuple(tuple(monster.position) for monster in monsters_on_map):
        start_fight(tuple(monster for monster in monsters_on_map if tuple(monster.position) == (player_pos[0], player_pos[1]))[0],
                    inventory, inventory_keys, player_pos, playable_area, TILES, chars, pos_of_chars, monsters, monsters_on_map, translations)

    # Moving player if speed of tile in front is different from -1
    if TILES[player_pos[0]][player_pos[1]].speed == -1:
        player_pos = old_player_pos.copy()

    """# If player moved, we play a sound
    if player_pos != old_player_pos:
        playsound(f"assets/sounds/footstep{randint(1, 5)}.wav", block=False)"""

    # Checking if the player is using the action key
    if user_input == "f":
        # If the player is doing an action, we check the tile in front of it for the action.
        # Beforehand, we create a position list for the direction, so we know later which tile the player is
        # interacting with.
        relative_tile_position = [0, 0]
        if player_direction   == 1: relative_tile_position[0] = -1
        elif player_direction == 2: relative_tile_position[0] =  1
        elif player_direction == 3: relative_tile_position[1] =  1
        elif player_direction == 0: relative_tile_position[1] = -1

        try:
            # We check if the tile is in range
            if player_pos[0] + relative_tile_position[0] < 0 or player_pos[1] + relative_tile_position[1] < 0: raise IndexError
            # If the value of this tile is 0, we just ignore it
            if TILES[player_pos[0] + relative_tile_position[0]][player_pos[1] + relative_tile_position[1]].action != 0:
                # We execute the action function linked to it.
                actions[TILES[player_pos[0] + relative_tile_position[0]][player_pos[1] + relative_tile_position[1]].action - 1](
                    TILES=TILES, player_direction=player_direction, player_pos=player_pos, playable_area=playable_area, chars=chars,
                    player_icons=player_icons, pos_of_chars=pos_of_chars, inventory=inventory, inventory_keys=inventory_keys,
                    monsters=monsters, monsters_on_map=monsters_on_map, translations=translations
                )
        except IndexError:
            # If any error from tile number occurs, we just skip it
            pass
    
    # Calculating level
    if inventory[inventory_keys.index(translations["main"]["inventory"]["XP"])][1] >= \
        20 + inventory[inventory_keys.index(translations["main"]["inventory"]["level"])][1] * 2:
        inventory[inventory_keys.index(translations["main"]["inventory"]["level"])][1] += 1
        inventory[inventory_keys.index(translations["main"]["inventory"]["XP"])][1] = 0
        
    # Remembering played time
    last_frame_executed = time.time()

