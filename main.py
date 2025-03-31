import pygame, sys
from constants import *
from hexes import *

def main():
    pygame.init()
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    #doing p good not to eat shit at this stage
    hex1 = Hexagon(100,100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.Surface.fill(screen, "black")
        hex1.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60)/1000
    #fukken idk

if __name__ == "__main__":
    main()