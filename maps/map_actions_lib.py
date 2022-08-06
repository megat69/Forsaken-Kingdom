# -*- coding: utf-8 -*-
from time import sleep
from getch import getch
from tiles import display_tiles, Tile
from colorama import Back, Fore, Style
import sys
from copy import deepcopy
from random import uniform
#from playsound import playsound

def text_display(text, slowness_multiplier:float=1, display_game_tiles:bool=True, do_getch:bool=True, play_sound:bool=True, **kwargs):
	if display_game_tiles:
		display_tiles(kwargs["TILES"],
		              [kwargs["playable_area"][0], kwargs["playable_area"][1]],
		              kwargs["player_pos"], kwargs["chars"], kwargs["player_icons"],
		              kwargs["player_direction"],
		              kwargs["monsters"], kwargs["monsters_on_map"], kwargs["inventory"])
	else:
		display_tiles(
			[[Tile(4, 2, 0, Back.RESET) for x in range(len(kwargs["TILES"][0]))] for y in range(len(kwargs["TILES"]))],
			[kwargs["playable_area"][0], kwargs["playable_area"][1]],
			kwargs["player_pos"], kwargs["chars"], " ", 0,
			kwargs["monsters"], kwargs["monsters_on_map"])
	print(Style.RESET_ALL)
	for i in range(len(text)):
		# Checking if the character is not a skip or a formatting character
		if text[i] != "¶":
			sys.stdout.write(text[i])
		sleep((0.04 if text[i] != "\n" else 0.2) * slowness_multiplier)
	if do_getch: getch()

def blend_background(player_pos, playable_area, TILES, chars, slowness_multiplier:float=1, invert:bool=False):
	"""
	Blends the background.
	"""
	empty_tile = Tile(4, 2, 0, Back.BLACK, 0)
	for x1 in range(max(0, player_pos[0] - (playable_area[0] // 2)),
	                min(len(TILES), playable_area[0] // 2 + player_pos[0])):
		for y1 in range(max(0, player_pos[1] - (playable_area[1] // 2)),
		                min(len(TILES[0]), playable_area[1] // 2 + player_pos[1])):
			scene = deepcopy(TILES)
			if invert:
				scene = [[scene[i][j] if j < y1 else empty_tile for j in range(len(scene[i]))] if i < x1 else [empty_tile for _ in range(len(scene[0]))] for i in range(len(scene))]
			else:
				scene = [[scene[i][j] if j > y1 else empty_tile for j in range(len(scene[i]))] if i > x1 else [empty_tile for _ in range(len(scene[0]))] for i in range(len(scene))]
			print("\n"*5)
			if invert is False:
				display_tiles(scene, playable_area, player_pos, chars, " "*4, 0, tuple(), tuple(), colors_enabled=False)
			else:
				display_tiles(scene, playable_area, player_pos, chars, " "*4, 0, tuple(), tuple(), colors_enabled=False)
		sleep(0.1 * slowness_multiplier)
