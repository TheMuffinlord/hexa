import pygame, math
from constants import *

class Hexagon(pygame.sprite.Sprite):
    def __init__(self, row, col):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(row, col)
        self.size = HEX_SIZE

    def hex_corner(self, corner):
        angle_degrees = 60 * corner
        angle_radius = math.pi / 180 * angle_degrees
        return (self.position.x + self.size * math.cos(angle_radius), self.position.y + self.size * math.sin(angle_radius))

    def draw(self, screen):
        corners = []
        for i in range(0,6):
            corners.append(self.hex_corner(i))
        pygame.draw.polygon(screen, "white", corners)

