import pygame, math
from constants import *
from hexes import *

class hex_unit(Hexagon): #debating whether to remove this honestly
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
    def __init__(self, q, r, name, team): #addl variables for later
        super().__init__(q, r)
        
        self.name = name
        self.active = False
        self.timer = 0
        self.team = team
        self.facing = self.initial_facing()
        #todo: add unit id; may go to further subclasses?
    
    def timer_check(self):
        return self.timer <= 0
    
    def timer_tick(self, dt):
        self.timer -= dt

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.facing)
        right = pygame.Vector2(0, 1).rotate(self.facing + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
        
    def draw(self, screen):
        if self.active == True:
            color = "yellow"
        elif self.team == 1:
            color = "blue"
        elif self.team == 2:
            color = "red"
        else:
            color = "white"
        pygame.draw.polygon(screen, color, self.triangle())



    def bound_edges(self):
        low_edge = lambda x: max(-MAP_POLAR_SIZE, -x - MAP_POLAR_SIZE)
        high_edge = lambda x: min(MAP_POLAR_SIZE, -x + MAP_POLAR_SIZE) + 1
        if self.over_edge():
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
    
    def over_edge(self):
        bound_check = lambda x: x not in range(-MAP_POLAR_SIZE, MAP_POLAR_SIZE+1)
        return bound_check(self.q) or bound_check(self.r) or bound_check(self.get_s())

    def check_facing(self):
        face = self.facing // 60
        if face == 6:
            face = 0
        return face


    def initial_facing(self):
        if self.team == 1:
            return 300
        if self.team == 2:
            return 120

    def rotate(self, lr):
        if self.timer_check():
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
            self.set_inactive()

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
        if self.timer_check():
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
            self.set_inactive()
            self.timer = INPUT_WAIT_TIMER

    def move_back(self):
        #hey y'all wanna see some bullshit
        old_facing = self.facing
        self.facing -= 180
        if self.facing < 0:
            self.facing += 360
        self.move_fwd()
        self.facing = old_facing

    def set_inactive(self):
        self.active = False

    def update(self, dt, keys):
        self.timer_tick(dt)
        #print("waiting on key press")
        #if self.active:
        if keys == pygame.K_a:
            #print("A pressed")
            self.rotate("l")
        elif keys == pygame.K_d:
            #print("D pressed")
            self.rotate("r")
        elif keys == pygame.K_w:
            #print("W pressed")
            self.move_fwd()
        elif keys== pygame.K_s:
            #print("S pressed")
            self.move_back()
        elif keys == pygame.K_SPACE:
            #print("space bar pressed")
            self.q = 0
            self.r = 0
        elif keys:
            self.set_inactive()
            
        self.position = pygame.Vector2(self.get_x(), self.get_y())




