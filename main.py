import pygame, sys
from constants import *
from hexes import *
from units import *
from mapgen import *


def main():
    pygame.init()
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    #doing p good not to eat shit at this stage
   

    drawable = pygame.sprite.Group()
    updatable = pygame.sprite.Group()

    Hexagon.containers = (drawable, updatable)
    Hexagon_Polar.containers = (drawable, updatable)
    hex_unit.containers = (drawable, updatable)

    #hex1 = Hexagon(0,0)
    #for corner in hex1.corners:
    #    print(corner)
    #print(hex1.hex_width())
    #hex2 = Hexagon(1,1)
    fill_map_polar()
    unit1 = hex_unit_polar(0,0,60)
    """unit2 = hex_unit(2,2,60)
    unit3 = hex_unit(3,3,120)
    unit2 = hex_unit(4,4,180)
    unit5 = hex_unit(5,5,240)
    unit6 = hex_unit(6,6,300) """
    #print(len(hexmap))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.Surface.fill(screen, "black")
        for item in updatable:
            item.update(dt)
        for item in drawable:
            item.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60)/1000
    #fukken idk

if __name__ == "__main__":
    main()