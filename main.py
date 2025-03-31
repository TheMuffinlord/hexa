import pygame, sys
from constants import *
from hexes import *

def fill_map():
    hexmap = []
    for row in range(MAP_ROWS):
        #if row % 2 == 1:
            #
            # new_y = hex1.radius + (row * HEX_SIZE)
        #else:
            #cry i guess
        for col in range(MAP_COLS):
            new_hex = Hexagon(col, row)
            hexmap.append(new_hex)

def main():
    pygame.init()
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    #doing p good not to eat shit at this stage
   

    hexfield = pygame.sprite.Group()

    Hexagon.containers = (hexfield)

    #hex1 = Hexagon(0,0)
    #for corner in hex1.corners:
    #    print(corner)
    #print(hex1.hex_width())
    #hex2 = Hexagon(1,1)
    fill_map()
    #print(len(hexmap))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.Surface.fill(screen, "black")
        for hexagon in hexfield:
            hexagon.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60)/1000
    #fukken idk

if __name__ == "__main__":
    main()