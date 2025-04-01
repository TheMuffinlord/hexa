import pygame, math
from constants import *

class Hexagon(pygame.sprite.Sprite):
    def __init__(self, col, row):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        #self.position = pygame.Vector2(row*HEX_SIZE, col*HEX_SIZE)
        self.size = HEX_SIZE #zoom logic will go here eventually ig
        self.radius = int(self.size * math.cos(math.radians(30)))
        #self.half_height = math.sqrt((self.size * 2) - (self.radius*2))
        #pos_x = col * 
        self.col = col
        self.row = row
        self.position = pygame.Vector2(self.get_x(), self.get_y())
        self.corners = []
        self.circle_color = "red"
        for i in range(0,6):
            self.corners.append(self.hex_corner(i))
        
    """ def hex_width(self):
        return int(self.size * math.cos(math.radians(30)))
    
    def hex_height(self):
        return int(self.size * math.sin(math.radians(30))) """

    def hex_corner(self, corner):
        angle_degrees = 60 * corner
        angle_radius = math.pi / 180 * angle_degrees
        return (int(self.position.x + self.size * math.cos(angle_radius)), int(self.position.y + self.size * math.sin(angle_radius)))

    def get_x(self):
        '''if self.col % 2 == 0:
            return int((self.col * (self.radius * 2)))'''
        return int(self.col * (self.radius * HEX_X_OFFSET))
        '''if self.col % 2 == 0:
            return int(((self.radius) * self.col) + self.radius)
        return int(((self.radius) * self.col) - self.radius)
        #return int(self.col * ((math.sqrt(3) * (self.size/2))))'''
    
    def get_y(self):
        if self.col % 2 == 0:
            return int((self.row * (self.size * HEX_Y_OFFSET))+(self.radius))
        return int(self.row * (self.size * HEX_Y_OFFSET))
        #if self.row % 2 == 0:
        '''           return int(((self.radius) * self.col) + self.radius)
        return int(((self.radius) * self.col) - self.radius)
        #return int(self.row * (self.hex_height()*2+2))'''

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.corners, 2)
        pygame.draw.circle(screen, self.circle_color, self.position, self.radius)

    def collision(self, other):
        if other.position.distance_to(self.position) < (self.radius + other.radius):
            return True
        return False
