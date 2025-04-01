import pygame, math
from constants import *
from hexes import *

class hex_unit(Hexagon):
    def __init__(self, col, row, facing): #addl variables for later
        super().__init__(col, row)
        self.facing = facing
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.facing)
        right = pygame.Vector2(0, 1).rotate(self.facing + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle())
