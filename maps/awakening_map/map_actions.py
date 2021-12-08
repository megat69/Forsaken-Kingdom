from time import sleep
from getch import getch
from tiles import display_tiles
import sys
from maps.map_actions_lib import text_display, blend_background
from colorama import Fore, Back, Style

def action1(**kwargs):
    text_display(kwargs["translations"]["awakening_map"]["welcome_sign"], **kwargs)

def action2(**kwargs):
    if "Boat" in kwargs["inventory"][kwargs["inventory_keys"].index(kwargs["translations"]["main"]["inventory"]["items"])][1]:
        if kwargs["player_direction"] == 0:
            kwargs["player_pos"][1] -= 2
        elif kwargs["player_direction"] == 1:
            kwargs["player_pos"][0] -= 2
        elif kwargs["player_direction"] == 2:
            kwargs["player_pos"][0] += 2
        else:
            kwargs["player_pos"][1] += 2
    else:
        action4(False, **kwargs)
    
def action3(**kwargs):
    text_display(kwargs["translations"]["awakening_map"]["action3"]["hi"], **kwargs)
    text_display(kwargs["translations"]["awakening_map"]["action3"]["follow"], **kwargs)
    for i in range(1, 4):
        display_tiles(
            kwargs["TILES"], kwargs["playable_area"], 
            [kwargs["player_pos"][0] - i, kwargs["player_pos"][1]], kwargs["chars"], 
            kwargs["player_icons"], 1, kwargs["monsters"], kwargs["monsters_on_map"]
        )
        sleep(0.5)
    else:
        # Change level
        # Looping for every loop time
        blend_background(kwargs["player_pos"], kwargs["playable_area"], kwargs["TILES"], kwargs["chars"])
            
    # Forsaken kingdom
    text_display(f"{Style.BRIGHT}{Fore.YELLOW}{Back.YELLOW}F O R S A K E N    K I N G D O M{Back.RESET}{Style.RESET_ALL}".center(86) +
                 f"\n\n" + Fore.YELLOW + kwargs["translations"]["awakening_map"]["action3"]["intro"] + Fore.RESET, display_game_tiles=False, play_sound=False, **kwargs)
    
    # Changes chapter
    with open("current_chapter.sav", "r") as f:
        current_chapter = int(f.read().replace("\n", ""))
    with open("current_chapter.sav", "w") as f:
        f.write(str(current_chapter + 1))
    print(kwargs["translations"]["main"]["relaunch_to_access_new_chapter"])
    sys.exit(0)
        
def action4(default=True, **kwargs):
    text_display(kwargs["translations"]["awakening_map"]["action4"][0] + (f' {kwargs["translations"]["awakening_map"]["action4"][1]} !' if default is True else f' ! ¶¶¶¶¶¶¶¶¶{kwargs["translations"]["awakening_map"]["action4"][2]}...'), 1.25, **kwargs)

def action5(**kwargs):
    text_display(kwargs["translations"]["awakening_map"]["action5"], **kwargs)


actions = [action1, action2, action3, action4, action5]