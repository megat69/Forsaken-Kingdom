from time import sleep
from getch import getch
from tiles import display_tiles
import sys
from maps.map_actions_lib import text_display, blend_background
from colorama import Fore, Back, Style

def action1(**kwargs):
    text_display("Welcome to my RPG !\nIt is pretty restrained, but it's only the beginning...", **kwargs)

def action2(**kwargs):
    if "Boat" in kwargs["inventory"][kwargs["inventory_keys"].index("Items")][1]:
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
    text_display("Hi, young person !", **kwargs)
    text_display("Follow me.", **kwargs)
    for i in range(1, 4):
        display_tiles(
            kwargs["TILES"], kwargs["playable_area"], 
            [kwargs["player_pos"][0] - i, kwargs["player_pos"][1]], kwargs["chars"], 
            kwargs["player_icons"], 1, kwargs["pos_of_chars"], kwargs["monsters"], kwargs["monsters_on_map"]
        )
        sleep(0.5)
    else:
        # Change level
        # Looping for every loop time
        blend_background(kwargs["player_pos"], kwargs["playable_area"], kwargs["TILES"], kwargs["chars"])
            
    # Forsaken kingdom
    text_display(f"{Style.BRIGHT}{Fore.YELLOW}{Back.YELLOW}F O R S A K E N    K I N G D O M{Back.RESET}{Style.RESET_ALL}".center(86) +
                 f"\n\n{Fore.YELLOW}After the sudden death of the king of this land a few years ago, evil took the throne.\n"
                 "\n"
                 "Monsters started to emerge, out of nowhere.\n"
                 "Citizens have to hide, fight... Or die.\n\n"
                 "But this reign has to end. And this is where YOU come into place !\n"
                 f"To destroy the Tyrant !{Fore.RESET}", display_game_tiles=False, **kwargs)
    
    # Changes chapter
    with open("current_chapter.sav", "r") as f:
        current_chapter = int(f.read().replace("\n", ""))
    with open("current_chapter.sav", "w") as f:
        f.write(str(current_chapter + 1))
    print("Relaunch program to access new chapter.")
    sys.exit(0)
        
def action4(default=True, **kwargs):
    text_display(f"I cannot cross the river{' there !' if default is True else ' ! ¶¶¶¶¶¶¶¶¶Yet...'}", 1.25, **kwargs)

def action5(**kwargs):
    text_display("Already looking for easter eggs, in the first level of the game ?! ¶¶¶¶Wow.", **kwargs)


actions = [action1, action2, action3, action4, action5]