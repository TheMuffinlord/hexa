#import pygame, math
from hexes import *
from units import *
from constants import *

""" def fill_map_offset():
    hexmap = []
    for row in range(MAP_ROWS):
        for col in range(MAP_COLS):
            new_hex = Hexagon(col, row)
            hexmap.append(new_hex) """

def fill_map_polar(hex_map, coord_map):
    for q in range(-MAP_POLAR_SIZE, MAP_POLAR_SIZE+1):
        r_low = max(-MAP_POLAR_SIZE, -q - MAP_POLAR_SIZE)
        r_high = min(MAP_POLAR_SIZE, -q + MAP_POLAR_SIZE) + 1
        for r in range(r_low, r_high):
            new_hex = Hexagon_Polar(q, r)
            hex_map.append(new_hex)
            coord_map.append((q, r))
    for hex in hex_map:
        hex.valid_neighbors = hex.neighbors_exists(coord_map)

def fill_team(team_size, team):
    team_list = []
    if team == 1:
        q = -MAP_POLAR_SIZE
        r = 0
        q_inc = 1
        r_inc = -1
        tn = 0
    elif team == 2:
        q = MAP_POLAR_SIZE
        r = 0
        q_inc = -1
        r_inc = 1
        tn = team_size
    for t in range(team_size):        
        team_list.append(hex_unit_polar(q, r, f"team{team}unit{t}", team))
        q += q_inc
        r += r_inc
    return team_list
    