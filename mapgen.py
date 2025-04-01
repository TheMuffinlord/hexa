import pygame, math
from hexes import *
from constants import *

def fill_map_offset():
    hexmap = []
    for row in range(MAP_ROWS):
        for col in range(MAP_COLS):
            new_hex = Hexagon(col, row)
            hexmap.append(new_hex)

def fill_map_polar():
    hexmap = []
    for q in range(-MAP_POLAR_SIZE, MAP_POLAR_SIZE+1):
        r_low = max(-MAP_POLAR_SIZE, -q - MAP_POLAR_SIZE)
        r_high = min(MAP_POLAR_SIZE, -q + MAP_POLAR_SIZE) + 1
        for r in range(r_low, r_high):
            new_hex = Hexagon_Polar(q, r)
            hexmap.append(new_hex)