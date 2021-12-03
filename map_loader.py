from tiles import Tile
from colorama import Back

colors = [Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE, Back.RESET]

def load_map(name:str, extension:str=".txt"):
    with open(name+extension, "r") as f:
        rows = f.read().splitlines()

    rows = [
        row.split(" ") for row in rows
    ]

    for row in rows:
        for i in range(len(row)):
            row[i] = row[i].split(",")
            row[i][0] = int(row[i][0])
            row[i][1] = int(row[i][1]) if row[i][1] != "N" else -1
            row[i][2] = int(row[i][2])
            row[i][2] = int(row[i][2])
            color_int = int(row[i][3])
            row[i][3] = colors[int(row[i][3])]

            # Creating the tile
            row[i] = Tile(*row[i], color_int)

    return rows