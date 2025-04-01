import pygame, math
from constants import *
from hexes import *

class hex_unit(Hexagon):
    def __init__(self, col, row, facing): #addl variables for later
        super().__init__(col, row)
        self.facing = facing
        self.timer = 0
        #todo: add unit id; may go to further subclasses?
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.facing)
        right = pygame.Vector2(0, 1).rotate(self.facing + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle())

    def rotate(self, lr):
        if self.timer <= 0:
        #simple version to test logic
            if lr == "l":
                self.facing -= 60
            if lr == "r":
                self.facing += 60
            if self.facing > 360:
                self.facing -= 360
            if self.facing < 0:
                self.facing += 360
            if self.facing % 60 != 0:
                self.facing = self.facing // 60
            self.timer = INPUT_WAIT_TIMER

    def move_fwd(self):
        if self.timer <= 0:
        #oh boy now we hit that six directional logic
            face = self.facing // 60
            if face == 0 or face == 6:
                self.row += 1
            if face == 3:
                self.row -= 1
                #those are easy
            if face == 1:
                if self.col % 2 == 0:
                    self.row += 1
                self.col -= 1
            if face == 2:
                if self.col % 2 != 0:
                    self.row -= 1
                self.col -= 1
            if face == 4:
                if self.col % 2 != 0:
                    self.row -= 1
                self.col += 1
            if face == 5:
                if self.col % 2 == 0:
                    self.row += 1
                self.col += 1

            if self.row < 0:
                self.row = MAP_ROWS
            if self.col < 0:
                self.col = MAP_COLS
            self.timer = INPUT_WAIT_TIMER

    def update(self, dt):
        self.timer -= dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate("l")
        if keys[pygame.K_d]:
            self.rotate("r")
        if keys[pygame.K_w]:
            self.move_fwd()
        #if keys[pygame.K_s]:
        #    self.move(dt * -1)
        self.position = pygame.Vector2(self.get_x(), self.get_y())

