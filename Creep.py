import sys
import os
import time
from msvcrt import getch
from msvcrt import kbhit
from colorama import init
from colorama import Fore, Back, Style
init()

size = 20
time_step = .1
simulate_iteration = 0
simulate_steps = 20
max_creep = 9
cursor = [0, 0]

grid = {}

# while True:
#    print(ord(getch()))
# enter 13
# space 32
# a 97
# s 115
# d 100
# w 119

key = ""
simulate = True


class Tile:
    def __init__(self, location, item, creep_height=0):
        self.location = location
        self.item = item
        self.creep_height = creep_height

for x in range(size):
    for y in range(size):
        tile = Tile((x, y), "")
        grid[x, y] = tile


def grow_creep(_grid):
    for y in range(size):
        for x in range(size):
            lowest_neighbor = check_lowest_neighbors_creep(_grid, x, y)
            # print(neighbors)
            if _grid[x, y].item == "spawn" and _grid[x, y].creep_height < max_creep:
                _grid[x, y].creep_height += 1
            if _grid[x, y].creep_height > lowest_neighbor[2] + 1:

                _grid[lowest_neighbor[0], lowest_neighbor[1]].creep_height += 1
                _grid[x, y].creep_height -= 1


def check_lowest_neighbors_creep(_grid, x, y):
    neighbors = [0, 0, 0, 0]
    min_n = 0
    try:
        neighbors[0] = _grid[x, y - 1].creep_height
    except KeyError:
        neighbors[0] = max_creep
    try:
        neighbors[1] = _grid[x + 1, y].creep_height
    except KeyError:
        neighbors[1] = max_creep
    try:
        neighbors[2] = _grid[x, y + 1].creep_height
    except KeyError:
        neighbors[2] = max_creep
    try:
        neighbors[3] = _grid[x - 1, y].creep_height
    except KeyError:
        neighbors[3] = max_creep

    direction = neighbors.index(min(neighbors))

    new_x, new_y = 0, 0
    if direction == 0:
        new_x = x
        new_y = y - 1
    elif direction == 1:
        new_x = x + 1
        new_y = y
    elif direction == 2:
        new_x = x
        new_y = y + 1
    elif direction == 3:
        new_x = x - 1
        new_y = y
    return new_x, new_y, min(neighbors)


def print_grid(_grid):
    os.system("cls")
    sys.stdout.write("\033[0;0H")
    for y in range(size):
        for x in range(size):
            creep = _grid[(x, y)].creep_height
            if creep > 0:
                sys.stdout.write(Back.RED)
            if cursor[0] == x and cursor[1] == y:
                sys.stdout.write(Back.WHITE)
            sys.stdout.write(str(creep))
            sys.stdout.write(Style.RESET_ALL+" ")
        sys.stdout.write("\n")
        sys.stdout.flush()

while True:
    if kbhit():
        key = ord(getch())
        if key == 120:  # x
            print("Exit")
            break
        elif key == 32:  # space
            print("Pause")
            simulate = not simulate
        elif key == 113:  # q
            print("spawn")
            grid[cursor[0], cursor[1]].item = "spawn"
            simulate = True
        elif key == 97:  # a
            print("left")
            cursor[0] -= 1
            simulate = False
            print_grid(grid)
        elif key == 100:  # d
            print("right")
            cursor[0] += 1
            print(cursor)
            simulate = False
            print_grid(grid)
        elif key == 119:  # w
            print("up")
            cursor[1] -= 1
            simulate = False
            print_grid(grid)
        elif key == 115:  # s
            print("down")
            cursor[1] += 1
            simulate = False
            print_grid(grid)
        new_cursor = [0 if i < 0 else i for i in cursor]  # change all negatives to 0
        cursor = new_cursor
    if simulate:
        grow_creep(grid)
        simulate_iteration += 1

    if simulate_iteration == simulate_steps:
        print_grid(grid)
        simulate_iteration = 0
        time.sleep(time_step)

