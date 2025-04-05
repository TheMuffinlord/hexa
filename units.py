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

    def get_s(self):
        return -self.q-self.r

    def wrap_edges(self):
        '''max_r = max(-MAP_POLAR_SIZE, -self.q - MAP_POLAR_SIZE)
        min_r = min(MAP_POLAR_SIZE, -self.q + MAP_POLAR_SIZE)
        max_q = max(-MAP_POLAR_SIZE, -self.r - MAP_POLAR_SIZE)
        min_q = min(MAP_POLAR_SIZE, -self.r + MAP_POLAR_SIZE)
        if self.q < max_q:
            self.q = min_q
        if self.q > min_q:
            self.q = max_q
        if self.r < max_r:
            self.r = min_r
        if self.r > min_r:
            self.r = max_r
        ok so essentially if any value goes over the polar size
        it needs to be cut back off. how do i do this and do it well'''
        #ok i think i know what i need. if any value goes over the edge of the map
        bound_check = lambda x: x not in range(-MAP_POLAR_SIZE, MAP_POLAR_SIZE+1)
        low_edge = lambda x: max(-MAP_POLAR_SIZE, -x - MAP_POLAR_SIZE)
        high_edge = lambda x: min(MAP_POLAR_SIZE, -x + MAP_POLAR_SIZE) + 1
        print(f"{self.q}, {self.r}, {self.get_s()}")
        print(f"q: {bound_check(self.q)}, r: {bound_check(self.r)}, s:{bound_check(-self.q-self.r)}")
        print(f"facing: {self.check_facing()}")
        if bound_check(self.q) or bound_check(self.r) or bound_check(self.get_s()):
            facing = self.check_facing()
            if facing == 0 or facing == 6: #gotta find a way to do this that doesn't take two cases
                self.r = low_edge(self.r)
            if facing == 3:
                self.r = high_edge(self.r)
            if facing == 2:
                self.q = high_edge(self.r)
                self.r = low_edge(self.q)
            if facing == 5:
                self.q = low_edge(self.r)
                self.r = high_edge(self.q)
            if facing == 1:
                self.r = low_edge(self.q)
                self.q = low_edge(self.r)
            if facing == 4:
                self.r = high_edge(self.q)
                self.q = high_edge(self.r)
        #check facing
        #depending on angle faced, 
    
    def over_edge(self):
        bound_check = lambda x: x not in range(-MAP_POLAR_SIZE, MAP_POLAR_SIZE+1)
        return bound_check(self.q) or bound_check(self.r) or bound_check(self.get_s())

    def check_facing(self):
        return self.facing // 60

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

    #six commands to move in every direction
    def move_up(self):
        self.r -= 1
        if self.over_edge():
            self.r += 1

    def move_down(self):
        self.r += 1
        if self.over_edge():
            self.r -= 1 
    
    def move_ul(self):
        self.q -= 1
        if self.over_edge():
            self.q += 1
    
    def move_dl(self):
        self.q -= 1
        self.r += 1
        if self.over_edge():
            self.q += 1
            self.r -= 1

    def move_ur(self):
        self.q += 1
        self.r -= 1
        if self.over_edge():
            self.q -= 1
            self.r += 1

    def move_dr(self):
        self.q += 1
        if self.over_edge():
            self.q -= 1

    def move_fwd(self):
        if self.timer <= 0:
        #oh boy now we hit that six directional logic
            face = self.check_facing()
            if face == 0 or face == 6: #down
                self.move_down()
            if face == 3: #up
                self.move_up()
            if face == 1: #down left
                self.move_dl()
            if face == 2: #up left
                self.move_ul()
            if face == 4: #up right
                self.move_ur()
            if face == 5: #down right
                self.move_dr()
            #self.wrap_edges()
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
        if keys[pygame.K_SPACE]:
            self.q = 0
            self.r = 0
        self.position = pygame.Vector2(self.get_x(), self.get_y())