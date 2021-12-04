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
            text_display("Welcome, young person.\nWe are the 4 sages who "
                         "survived the return of the Tyrant.\n"
                         "\nYou need to save this kingdom, and therefore, we have to teach you how to fight.", **kwargs)
            text_display("Take this sword.", **kwargs)
        if not "Sword (Atk +3)" in kwargs["inventory"][kwargs["inventory_keys"].index("Items")][1]:
            kwargs["inventory"][kwargs["inventory_keys"].index("Items")][1].append("Sword (Atk +3)")
        if _DEBUG is False:
            text_display(f"You  received  a  {Fore.YELLOW}SWORD{Fore.RESET}  !", 3, **kwargs)
            text_display("Now, fight this monster, and then go to talk to us again !", **kwargs)
        kwargs["monsters_on_map"].append(MapMonster(kwargs["monsters"][0], [16, 9], 10, True))
        was_monster_spawned = True
    
    if was_monster_spawned is True and len(kwargs["monsters_on_map"]) == 0:
        text_display("Congratulations, now, you know how to fight !", **kwargs)
        text_display("Let us heal you.", **kwargs)
        kwargs["inventory"][kwargs["inventory_keys"].index("Health")][1] = kwargs["inventory"][kwargs["inventory_keys"].index("Health")][2]
        blend_background(kwargs["player_pos"], kwargs["playable_area"], kwargs["TILES"], kwargs["chars"], 0.25)
        text_display("You are now fully healed.\n\nLet's go, follow us.", **kwargs)
        
        # Changes chapter
        with open("current_chapter.sav", "r") as f:
            current_chapter = int(f.read().replace("\n", ""))
        with open("current_chapter.sav", "w") as f:
            f.write(str(current_chapter + 1))
        print("Relaunch program to access new chapter.")
        sys.exit(0)
        

actions = [action1]