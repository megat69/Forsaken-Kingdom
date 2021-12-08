from colorama import Fore, Back, Style
_DEBUG = False
colors = [Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE, Back.RESET]

class Tile:
    def __init__(self, char_pos:int, speed:int, action:int, color, color_int=-1, pos_of_char=0):
        self.char_pos = char_pos  # The character of the tile
        self.speed = speed
        self.action = action
        self.color = color
        self.color_int = color_int
        self.pos_of_char = pos_of_char  # The position of the character (0 is full tile, 1 is left, 2 middle, and 3 right)

def display_tiles(TILES, playable_area, player_pos, chars, player_icons, player_direction, monsters, monsters_on_map, inventory=(("", ""),), colors_enabled=True):
    """
    Displays the tiles of the game.
    """

    if _DEBUG: print("-"*playable_area[1]*3)
    # Displaying tiles and player
    counter = 0
    for x in range(player_pos[0] - (playable_area[0] // 2), (playable_area[0] // 2) + player_pos[0]):
        for y in range(player_pos[1] - (playable_area[1] // 2), (playable_area[1] // 2) + player_pos[1]):
            # Checking if the tile is in the playable area, and if not, displaying 3 spaces
            if x < 0 or y < 0 or x >= len(TILES) or y >= len(TILES[0]):
                print("   ", end=Back.RESET)
            # If the current coords are those of a monster
            elif (x, y) in tuple(tuple(monster.position) for monster in monsters_on_map):
                # Finding the right monster
                monster = tuple(monster for monster in monsters_on_map if tuple(monster.position) == (x, y))[0]
                # Displaying the monster correctly
                if TILES[x][y].pos_of_char == 0:
                    # If so, we know the tile to display below
                    char_around = chars[TILES[x][y].char_pos]
                    color_around = TILES[x][y].color
                else:
                    # We look for every character around him, and we determine which is the most used
                    # while skipping those who are not full
                    chars_around = ""
                    colors_around = ""
                    try:
                        if TILES[x][y-1].pos_of_char == 0:
                            chars_around += chars[TILES[x][y-1].char_pos]
                    except IndexError: pass
                    try:
                        if TILES[x][y+1].pos_of_char == 0:
                            chars_around += chars[TILES[x][y+1].char_pos]
                    except IndexError: pass
                    try:
                        if TILES[x+1][y].pos_of_char == 0:
                            chars_around += chars[TILES[x+1][y].char_pos]
                    except IndexError: pass
                    try:
                        if TILES[x-1][y].pos_of_char == 0:
                            chars_around += chars[TILES[x-1][y].char_pos]
                    except IndexError: pass
                    if chars_around == "": 
                        chars_around = "-"
                        colors_around = "0"
                    
                    # We select the character which is the most present around
                    char_around = max(set(chars_around), key = chars_around.count)
                    color_around = colors[int(max(set(colors_around), key = colors_around.count))]
                    del chars_around
                    del colors_around
                
                print(color_around + char_around + Fore.RED + monster.monster.monster_char + color_around + Fore.RESET + char_around, end=Back.RESET)
                del char_around
                del color_around
            # If the current coords aren't those of a player
            elif x != player_pos[0] or y != player_pos[1]:
                # If this is a regular tile, we display it 3 times
                if TILES[x][y].pos_of_char == 0:
                    print(TILES[x][y].color + chars[TILES[x][y].char_pos] * 3 + Back.RESET, end=Back.RESET)
                # otherwise, we work out where to place it
                elif TILES[x][y].pos_of_char == 1:
                    try:
                        print(TILES[x][y].color + chars[TILES[x][y].char_pos] + TILES[x][y+1].color + chars[TILES[x][y+1].char_pos] * 2, end=Back.RESET)
                    except IndexError:
                        print(TILES[x][y].color + chars[TILES[x][y].char_pos] + " " * 2, end=Back.RESET)
                elif TILES[x][y].pos_of_char == 2:
                    try:
                        print(TILES[x][y-1].color + chars[TILES[x][y-1].char_pos] + TILES[x][y].color + chars[TILES[x][y].char_pos]\
                              + TILES[x][y+1].color + chars[TILES[x][y+1].char_pos], end=Back.RESET)
                    except IndexError:
                        try:
                            try:
                                print(TILES[x+1][y].color + chars[TILES[x+1][y].char_pos] + TILES[x][y].color + chars[TILES[x][y].char_pos]\
                                      + TILES[x+1][y].color + chars[TILES[x+1][y].char_pos], end=Back.RESET)
                            except IndexError:
                                print(TILES[x-1][y].color + chars[TILES[x-1][y].char_pos] + TILES[x][y].color + chars[TILES[x][y].char_pos] +\
                                      TILES[x-1][y].color + chars[TILES[x-1][y].char_pos], end=Back.RESET)
                        except IndexError:
                            print(TILES[x][y].color + " " + chars[TILES[x][y].char_pos] + " ", end=Back.RESET)
                elif TILES[x][y].pos_of_char == 3:
                    try:
                        print(TILES[x][y-1].color + chars[TILES[x][y-1].char_pos] * 2 + TILES[x][y].color + chars[TILES[x][y].char_pos], end=Back.RESET)
                    except IndexError:
                        print(TILES[x][y].color + " " * 2 + chars[TILES[x][y].char_pos], end=Back.RESET)
            else:  # Displaying player character
                # We look if the character usually below the player is a full tile
                if TILES[x][y].pos_of_char == 0:
                    # If so, we know the tile to display below
                    char_around = chars[TILES[x][y].char_pos]
                    color_around = TILES[x][y].color
                else:
                    # We look for every character around him, and we determine which is the most used
                    # while skipping those who are not full
                    chars_around = ""
                    colors_around = ""
                    try:
                        if TILES[x][y-1].pos_of_char == 0:
                            chars_around += chars[TILES[x][y-1].char_pos]
                            colors_around += str(TILES[x][y-1].color_int)
                    except IndexError: pass
                    try:
                        if TILES[x][y+1].pos_of_char == 0:
                            chars_around += chars[TILES[x][y+1].char_pos]
                            colors_around += str(TILES[x][y+1].color_int)
                    except IndexError: pass
                    try:
                        if TILES[x+1][y].pos_of_char == 0:
                            chars_around += chars[TILES[x+1][y].char_pos]
                            colors_around += str(TILES[x+1][y].color_int)
                    except IndexError: pass
                    try:
                        if TILES[x-1][y].pos_of_char == 0:
                            chars_around += chars[TILES[x-1][y].char_pos]
                            colors_around += str(TILES[x-1][y].color_int)
                    except IndexError: pass
                    if chars_around == "": 
                        chars_around = "-"
                    if colors_around == "":
                        colors_around = "0"
                    
                    # We select the character which is the most present around
                    char_around = max(set(chars_around), key = chars_around.count)
                    color_around = colors[int(max(set(colors_around), key = colors_around.count))]
                    del chars_around
                    del colors_around
                
                print(color_around + char_around + Style.BRIGHT + player_icons[player_direction] + Style.RESET_ALL + color_around + char_around, end=Back.RESET)
                del char_around
                del color_around
        try:
            if inventory == (("", ""),) or inventory[counter][0] == "": raise IndexError
            print("\t", inventory[counter][0], ":", (inventory[counter][1] if not isinstance(inventory[counter][1], (list, tuple)) else ", ".join(element for element in inventory[counter][1])))
        except IndexError:
            print("")
        finally:
            counter += 1