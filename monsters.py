# -*- coding: utf-8 -*-
from maps.map_actions_lib import blend_background, text_display
from time import sleep
from random import randint
import sys

class Monster:
    def __init__(self, monster_char, atk_damage_min, atk_damage_max, 
                 increase_atk_by_lvl:bool=True, hostile:bool=True, 
                 detection_radius:int=9, XP_reward:int=5):
        self.monster_char = monster_char
        self.atk_damage_min = atk_damage_min
        self.atk_damage_max = atk_damage_max
        self.increase_atk_by_lvl = increase_atk_by_lvl
        self.hostile = hostile
        self.detection_radius = detection_radius
        self.XP_reward = XP_reward

class MapMonster:
    def __init__(self, monster, position, hp, aggravated:bool=False):
        self.position = position
        self.hp = hp
        self.aggravated = aggravated
        self.monster = monster
        
def start_fight(monster, inventory, inventory_keys, player_pos, playable_area, TILES, chars, pos_of_chars, monsters, monsters_on_map, translations):
    # We blend the background
    blend_background(player_pos, playable_area, TILES, chars, 0.5)
    
    # We display the two players
    header_text = "       "  + translations["monsters"]["playernames"][0] + "\t"*6 + translations["monsters"]["playernames"][1] + "\n\n"
    player_text = ['______ ', '| ___ | ', '|_/ /', '|  __/ ', '| |    ', r'\\_|   ']
    text = "\n".join(player_line + "\t"*5 + monster.monster.monster_char*len(player_line) for player_line in player_text)
    
    # We display the text we generated
    text_display(header_text + text, slowness_multiplier=0, display_game_tiles=False, do_getch=False, TILES=TILES, chars=chars, player_pos=player_pos, 
                 playable_area=playable_area, pos_of_chars=pos_of_chars, monsters=monsters, monsters_on_map=[])
    sleep(1)
    
    # Looping until one of the two participants gets to 0 HP
    while inventory[inventory_keys.index(translations["main"]["inventory"]["health"])][1] > 0 and monster.hp > 0:
        # Slowly replacing header with HP
        header_text = (translations["main"]["inventory"]["health"] + ": " + str(inventory[inventory_keys.index(translations["main"]["inventory"]["health"])][1]), translations["main"]["inventory"]["health"] + ": " + str(monster.hp))
        for i in range(max(len(header_text[0]), len(header_text[1])) + 1):
            print("\n"*(playable_area[0] - len(player_text) - 3))
            print("       " + header_text[0][:i] + "-"*len(header_text[0][i:]) + "\t"*5 + \
                  header_text[1][:i] + "-"*len(header_text[1][i:]))
            print("\n" + text)
            
            sleep(0.15)
        
        sleep(0.5)
        
        # Registering action
        try: user_input = input(f'\n{translations["monsters"]["options"]}\n').lower()[0]
        except IndexError: user_input = ""
        if user_input not in ("f", "h", "r"): continue
    
        # Calculating attack damage based off a constant, the level, and the player items
        atk_damage = 5 + inventory[inventory_keys.index(translations["main"]["inventory"]["level"])][1]
        # We increase attack damage for each item with an atk modifier
        for item in inventory[inventory_keys.index(translations["main"]["inventory"]["items"])][1]:
            if not "Atk" in item: continue
            atk_damage += int(item[item.find("Atk ")+4:-1])
        # Randomizing it
        atk_damage = randint(atk_damage - 2, atk_damage + 1)
        # Fighting if wanted
        if user_input == "f":
            print(translations["monsters"]["dealt_dmg"].format(min(atk_damage, monster.hp)))
            monster.hp -= atk_damage
        
            if monster.hp <= 0:
                print(translations["monsters"]["got_him"])
                sleep(2)
                monsters_on_map.remove(monster)
                inventory[inventory_keys.index("XP")][1] += monster.monster.XP_reward
                continue
        # Healing if wanted
        elif user_input == "h":
            regen = randint(2 + inventory[inventory_keys.index(translations["main"]["inventory"]["level"])][1], 
                     4 + inventory[inventory_keys.index(translations["main"]["inventory"]["level"])][1])
            inventory[inventory_keys.index(translations["main"]["inventory"]["health"])][1] += regen
            print(translations["monsters"]["regened_HP"].format(regen))
        # Trying to run, one chance out of 3
        elif user_input == "r":
            if randint(0, 2) == 0:
                print(translations["monsters"]["ran_away"][0])
                sleep(2)
                return None
            print(translations["monsters"]["ran_away"][1])
        
        # Sleeps for a couple seconds
        sleep(2)
        
        # Randomly damages the player
        if monster.monster.increase_atk_by_lvl is True:
            dmg = randint(monster.monster.atk_damage_min + inventory[inventory_keys.index(translations["main"]["inventory"]["level"])][1], 
                          monster.monster.atk_damage_max + inventory[inventory_keys.index(translations["main"]["inventory"]["level"])][1])
        else:
            dmg = randint(monster.monster.atk_damage_min, monster.monster.atk_damage_max)
        
        inventory[inventory_keys.index(translations["main"]["inventory"]["health"])][1] -= dmg
        print(translations["monsters"]["dmg_received"].format(dmg))
        sleep(1.5)
        
        if inventory[inventory_keys.index(translations["main"]["inventory"]["health"])][1] <= 0:
            print(translations["monsters"]["got_killed"])
            sys.exit(0)

    blend_background(player_pos, playable_area, TILES, chars, 0.5, invert=True)
    
