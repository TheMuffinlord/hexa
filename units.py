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

#time for the polar express
class hex_unit_polar(Hexagon_Polar):
    def __init__(self, q, r, facing): #addl variables for later
        super().__init__(q, r)
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

    def wrap_edges(self):
        if self.q < -MAP_POLAR_SIZE:
            self.q += MAP_POLAR_SIZE +1
        if self.q > MAP_POLAR_SIZE +1 :
            self.q -= MAP_POLAR_SIZE -1
        if self.r < max(-MAP_POLAR_SIZE, -self.q - MAP_POLAR_SIZE):
            self.r += min(MAP_POLAR_SIZE, -self.q + MAP_POLAR_SIZE) + 1
        if self.r > min(MAP_POLAR_SIZE, -self.q + MAP_POLAR_SIZE) + 1:
            self.r -= max(-MAP_POLAR_SIZE, -self.q - MAP_POLAR_SIZE)


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
            if face == 0 or face == 6: #down
                self.r += 1
            if face == 3: #up
                self.r -= 1
            if face == 1: #down left
                self.q -= 1
                self.r += 1
            if face == 2: #up left
                self.q -= 1
            if face == 4: #up right
                self.q += 1
                self.r -= 1
            if face == 5: #down right
                self.q += 1
            self.wrap_edges()
            self.timer = INPUT_WAIT_TIMER

    def move_back(self):
        #hey y'all wanna see some bullshit
        old_facing = self.facing
        self.facing -= 180
        if self.facing < 0:
            self.facing += 360
        self.move_fwd()
        self.facing = old_facing

    def update(self, dt):
        self.timer -= dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate("l")
        if keys[pygame.K_d]:
            self.rotate("r")
        if keys[pygame.K_w]:
            self.move_fwd()
        if keys[pygame.K_s]:
            self.move_back()
        self.position = pygame.Vector2(self.get_x(), self.get_y())