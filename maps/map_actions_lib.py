# -*- coding: utf-8 -*-
from time import sleep
from getch import getch
from tiles import display_tiles, Tile
from colorama import Back, Fore, Style

def text_display(text, slowness_multiplier:float=1, display_game_tiles:bool=True, do_getch:bool=True, **kwargs):
    for i in range(len(text)):
        if text[i] != "¶":
            if display_game_tiles: display_tiles(kwargs["TILES"], 
                          [kwargs["playable_area"][0] - text[:i+1].count("\n"), kwargs["playable_area"][1]], 
                          kwargs["player_pos"], kwargs["chars"], kwargs["player_icons"], kwargs["player_direction"],
                          kwargs["pos_of_chars"], kwargs["monsters"], kwargs["monsters_on_map"])
            else:
                display_tiles([[Tile(4, 2, 0, Back.RESET) for x in range(len(kwargs["TILES"][0]))] for y in range(len(kwargs["TILES"]))], 
                          [kwargs["playable_area"][0] - text[:i+1].count("\n"), kwargs["playable_area"][1]], 
                          kwargs["player_pos"], kwargs["chars"], " ", 0,
                          kwargs["pos_of_chars"], kwargs["monsters"], kwargs["monsters_on_map"])
            print(Style.RESET_ALL, text[:i+1].replace("¶", ""), Style.RESET_ALL, sep="")
        sleep((0.05 if text[i] != "\n" else 0.2) * slowness_multiplier)
    if do_getch: getch()
    
def blend_background(player_pos, playable_area, TILES, chars, slowness_multiplier:float=1):
    for x1 in range(max(0, player_pos[0] - (playable_area[0] // 2)),
                   min(len(TILES), playable_area[0] // 2 + player_pos[0])):
        for y1 in range(max(0, player_pos[1] - (playable_area[1] // 2)),
                       min(len(TILES[0]), playable_area[1] // 2 + player_pos[1])): 
            print("\n"*5)
            # Looping for every tile
            for x in range(max(0, player_pos[0] - (playable_area[0] // 2)),
                       min(len(TILES), playable_area[0] // 2 + player_pos[0])):
                for y in range(max(0, player_pos[1] - (playable_area[1] // 2)),
                               min(len(TILES[0]), playable_area[1] // 2 + player_pos[1])):
                    print(chars[TILES[x][y].char_pos] * 3 if x > x1 or y > y1 else "   ", end="")
                print("")
        sleep(0.1 * slowness_multiplier)