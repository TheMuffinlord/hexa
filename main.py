import pygame
from constants import *
from hexes import *
from units import *
from mapgen import *
from textbox import *

def main():
    pygame.init()
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    #doing p good not to eat shit at this stage
   

    drawable = pygame.sprite.Group()
    units = pygame.sprite.Group()
    
    
    Hexagon_Polar.containers = (drawable)
    hex_unit_polar.containers = (drawable, units)


    center_hex = Hexagon_Polar(0,0,False)
    hexmap = []
    coordmap = []
    fill_map_polar(hexmap, coordmap)
    #print(coordmap)
    debug_text = ["whoops", "you broke it", "line 3", "line 4", "", "", "line 7"] #ugh i gotta make this scalable
    team1 = fill_team(3,1)
    team2 = fill_team(3,2)

    team1[0].active = True
    active_unit = 0
    all_units = team1 + team2 
    round_started = True
    round_counter = 1
    green_line = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN: #going to have to put mouse logic in ehre too
                pressed_key = event.key
                if pressed_key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                else:
                    for item in units:
                        if item.active == True and item.name == all_units[active_unit].name:
                            round_started = False
                            item.update(dt, pressed_key)
                            center_line = all_units[active_unit].hex_line(center_hex)
                            green_line = all_units[active_unit].line_draw(center_line, False, green_line)
                            green_line = all_units[active_unit].line_draw(center_line)
                            if item.active == False:
                                
                                active_unit += 1
                                if active_unit >= len(all_units):
                                    active_unit = 0
                                    round_started = True
                                else:
                                    round_started = False
                        elif item.active == False:
                            if item.name == all_units[active_unit].name:
                                item.active = True
                                item.energize()
        debug_text[0] = f"active unit: {all_units[active_unit].name}"
        debug_text[2] = f"dist to center: {all_units[active_unit].hex_distance(center_hex)}"
        


        if round_started == False or (round_started == True and all_units[active_unit].energy > 0): #this is it i found the exact conditions
            debug_text[1] = f"remaining energy: {all_units[active_unit].energy + 1}" 
        else: 
            debug_text[1] = "Next round started, hit any key"

        pygame.Surface.fill(screen, "black")
        for item in units:
            item.update(dt, None)
        for item in drawable:
            item.draw(screen)
        
        #debug_text = f"unit 1: {unit1.active},  unit 2: {unit2.active}"

        debug_box(screen, debug_text)
        pygame.display.flip()
        dt = clock.tick(60)/1000
    #fukken idk

if __name__ == "__main__":
    main()