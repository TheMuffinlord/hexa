import pygame
from hexes import *
from units import *
from mapgen import *
from textbox import *
from constants import *

def add_unit_to_group(unit, group):
    group.add(unit)

def battle_screen(player_units, enemies, screen, map, clock, dt): 
    #print(player_units)
    #print(enemies)
    #print(map)
    loop_updatable = pygame.sprite.Group()
    loop_drawable = pygame.sprite.Group()
    loop_playable = pygame.sprite.Group()
    loop_automatic = pygame.sprite.Group()
    loop_passive = pygame.sprite.Group()
     #should only ever contain one unit!
    turn_order = [] 
    for unit in player_units:       
        add_unit_to_group(unit, loop_updatable)
        add_unit_to_group(unit, loop_drawable)
        add_unit_to_group(unit, loop_playable)
    for unit in enemies:
        add_unit_to_group(unit, loop_automatic)
        add_unit_to_group(unit, loop_drawable)
        add_unit_to_group(unit, loop_updatable)
    for tile in map:
        add_unit_to_group(tile, loop_drawable)
        add_unit_to_group(tile, loop_passive)
    
    action_waiting = False
    kbd_waiting = False
    mouse_waiting = False
    in_progress = True
    game_running = True

    #initialize the turn state
    for unit in player_units:
        turn_order.append(unit)
    for unit in enemies:
        turn_order.append(unit)
    
    current_unit = turn_order[0]
    current_unit.active = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN: #going to have to put mouse logic in ehre too
                pressed_key = event.key
                action_waiting = True
                kbd_waiting = True
                if mouse_waiting == True:
                    print("keyboard overriding mouse") #good enough for debug!
                    mouse_waiting = False
                if pressed_key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #targeting logic, break out
                clicked_location = pygame.mouse.get_pos()
                print(f"clicked at {clicked_location}")
                action_waiting = True
                mouse_waiting = True
                if kbd_waiting == True:
                    print("mouse overriding keyboard")
                    kbd_waiting = False
            if action_waiting == True:
                print("action caught")
                if mouse_waiting == True:
                    in_progress = mouse_interpreter(clicked_location, current_unit, loop_playable, loop_automatic, loop_passive)
                    action_waiting = False
                    mouse_waiting = False
                elif kbd_waiting == True:
                    in_progress = kbd_interpreter(pressed_key, current_unit, loop_playable, loop_automatic, loop_passive)
                    action_waiting = False
                    kbd_waiting = False
                else: 
                    action_waiting = False
                    print("some other action took place?")

            if in_progress == False:
                current_unit.active = False
                print(f"current unit active: {current_unit.active}")
                current_unit = next_unit_in_line(turn_order, current_unit)
                current_unit.energy = current_unit.max_energy
                print(f"new unit: {current_unit.name}, energy: {current_unit.energy}")
                current_unit.active = True
                in_progress = True
                if current_unit == turn_order[0]:
                    next_turn(turn_order)


        pygame.Surface.fill(screen, "black")
        for item in loop_updatable:
            item.update(dt, None)
        for item in loop_drawable:
            item.draw(screen)    

        pygame.display.flip()
        dt = clock.tick(60)/1000            


def kbd_interpreter(pressed_key, current_unit, playable, automatic, passive):
    if current_unit in playable:
        match(pressed_key):
            case pygame.K_a:
                current_unit.rotate("l")
            case pygame.K_d:
                current_unit.rotate("r")
            case pygame.K_w:
                #add logic here to ensure unit *can* move up
                current_unit.move_fwd()
            case pygame.K_s:
                #add logic here to make sure unit *can* move down
                current_unit.move_back()
            case pygame.K_q:
                #skip turn
                return False
        return current_unit.active
    else:
        print("current unit not playable")
        return False
    
def mouse_interpreter(clicked_location, current_unit, playable, automatic, passive):
    print(f"clicked screen at {clicked_location}")
    return True #i will write these i swear

def next_unit_in_line(turn_order, current_unit):
    for unit in turn_order:
        if unit == current_unit:
            cu_index = turn_order.index(unit) + 1
            if cu_index >= len(turn_order):
                cu_index = 0
    return turn_order[cu_index]

def next_turn(turn_order): #reset all energy to maximum. may need to feed some other logic eventually?
    print(f"new turn starting. turn order: {turn_order}")
    for unit in turn_order:
        unit.energy = unit.max_energy
    #return turn_order