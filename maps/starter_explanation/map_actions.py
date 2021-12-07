from maps.map_actions_lib import text_display, blend_background
from time import sleep
from getch import getch
from monsters import MapMonster
import sys
from colorama import Fore

was_monster_spawned = False
_DEBUG = False

def action1(**kwargs):
    global was_monster_spawned
    if was_monster_spawned is False:
        if _DEBUG is False:
            text_display(kwargs["translations"]["starter_explanation"]["sages_intro"], **kwargs)
            text_display(kwargs["translations"]["starter_explanation"]["take_sword"], **kwargs)
        if not "Sword (Atk +3)" in kwargs["inventory"][kwargs["inventory_keys"].index(kwargs["translations"]["main"]["inventory"]["items"])][1]:
            kwargs["inventory"][kwargs["inventory_keys"].index(kwargs["translations"]["main"]["inventory"]["items"])][1].append("Sword (Atk +3)")
        if _DEBUG is False:
            text_display(kwargs["translations"]["starter_explanation"]["received"] + f"{Fore.YELLOW}SWORD{Fore.RESET}  !", 3, **kwargs)
            text_display(kwargs["translations"]["starter_explanation"]["fight_monster"], **kwargs)
        kwargs["monsters_on_map"].append(MapMonster(kwargs["monsters"][0], [12, 6], 10, True))
        was_monster_spawned = True
    
    if was_monster_spawned is True and len(kwargs["monsters_on_map"]) == 0:
        text_display(kwargs["translations"]["starter_explanation"]["congrats"], **kwargs)
        text_display(kwargs["translations"]["starter_explanation"]["sages_healing"], **kwargs)
        kwargs["inventory"][kwargs["inventory_keys"].index(kwargs["translations"]["main"]["inventory"]["health"])][1] = kwargs["inventory"][kwargs["inventory_keys"].index(kwargs["translations"]["main"]["inventory"]["health"])][2]
        for b in (False, True):
            blend_background(kwargs["player_pos"], kwargs["playable_area"], kwargs["TILES"], kwargs["chars"], 0.25, invert=b)
        text_display(kwargs["translations"]["starter_explanation"]["fully_healed"], **kwargs)
        
        # Changes chapter
        with open("current_chapter.sav", "r") as f:
            current_chapter = int(f.read().replace("\n", ""))
        with open("current_chapter.sav", "w") as f:
            f.write(str(current_chapter + 1))
        print(kwargs["translations"]["main"]["relaunch_to_access_new_chapter"])
        blend_background(kwargs["player_pos"], kwargs["playable_area"], kwargs["TILES"], kwargs["chars"], 0.75)
        sys.exit(0)
        

def action2(**kwargs):
    text_display("I guess I could make a Link to another videogame series from this broken piece of clay...", **kwargs)

actions = [action1, action2]