import pygame, math
from constants import *

class Hexagon(pygame.sprite.Sprite): #probably remove this. i can do math for pure xy coords now
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
        #pygame.draw.circle(screen, self.circle_color, self.position, self.radius)

    def collision(self, other):
        if other.position.distance_to(self.position) < (self.radius + other.radius):
            return True
        return False

    def update(self, dt):
        pass

class Hexagon_Polar(pygame.sprite.Sprite):
    def __init__(self, q, r, drawn=True, color="white"):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.size = HEX_SIZE #zoom logic will go here eventually ig
        self.radius = int(self.size * math.cos(math.radians(30)))
        self.q = q
        self.r = r
        self.s = (q * -1)-r #three dimension axial
        self.drawn = drawn #visibility toggle
        self.color = color
        self.offset = (0,0)#for later
        self.position = pygame.Vector2(self.get_x(), self.get_y())
        self.corners = []
        self.all_neighbors = self.update_neighbors()
        self.valid_neighbors = []
        for i in range(0,6):
            self.corners.append(self.hex_corner(i))
        
    def hex_corner(self, corner):
        angle_degrees = 60 * corner
        angle_radius = math.pi / 180 * angle_degrees
        return (int(self.position.x + self.size * math.cos(angle_radius)), int(self.position.y + self.size * math.sin(angle_radius)))

    def get_x(self):
        center_x = int(SCREEN_WIDTH/2)
        return (int(self.size * (1.5 * self.q))) + center_x
        '''if self.col % 2 == 0:
            return int((self.col * (self.radius * 2)))
        return int(self.col * (self.radius * HEX_X_OFFSET))
        if self.col % 2 == 0:
            return int(((self.radius) * self.col) + self.radius)
        return int(((self.radius) * self.col) - self.radius)
        return int(self.col * ((math.sqrt(3) * (self.size/2))))'''
    
    def get_y(self):
        center_y = int(SCREEN_HEIGHT/2)
        return (int(self.size * (math.sqrt(3)/2 * self.q + math.sqrt(3) * self.r))) + center_y
        '''if self.col % 2 == 0:
            return int((self.row * (self.size * HEX_Y_OFFSET))+(self.radius))
        return int(self.row * (self.size * HEX_Y_OFFSET))
        #if self.row % 2 == 0:
                   return int(((self.radius) * self.col) + self.radius)
        return int(((self.radius) * self.col) - self.radius)
        #return int(self.row * (self.hex_height()*2+2))'''

    def get_s(self):
        return -self.q-self.r

    def draw(self, screen):
        if self.drawn == True:
            pygame.draw.polygon(screen, self.color, self.corners, 2)
        #pygame.draw.circle(screen, self.circle_color, self.position, self.radius)

    def collision(self, other):
        if other.position.distance_to(self.position) < (self.radius + other.radius):
            return True
        return False

    def update_neighbors(self): #working
        return [(self.q+1, self.r), (self.q+1, self.r-1), (self.q, self.r-1), (self.q-1, self.r), (self.q-1, self.r+1), (self.q, self.r+1)]

    def neighbors_exists(self, coordmap): #working, would be cool if it checked for facing
        neighbor_checks = [False, False, False, False, False, False]
        for n in range(6):
            if self.all_neighbors[n] in coordmap:
                neighbor_checks[n] = True
        return neighbor_checks
        
    def hex_direction(self, direction):
        return self.all_neighbors[direction]
    
    def hex_add(self, other):
        return (self.q + other.q, self.r + other.r)
    
    def hex_neighbor(self, direction):
        return self.hex_add(self.hex_direction(direction))
    
    def hex_subtract(self, other): #working
        return (self.q - other.q, self.r - other.r)
    
    def hex_distance(self, other): #working
        distance = self.hex_subtract(other)
        return (abs(distance[0]) + abs(distance[0] + distance[1]) + abs(distance[1]))//2

    def hex_lerp(self, other, inter_distance):
        point_lerp = lambda a, b, t: a + (b - a) * t
        return (point_lerp(self.q, other.q, inter_distance), point_lerp(self.r, other.r, inter_distance))
    
    def hex_round(self, other):
        q = round(other[0])
        r = round(other[1])
        s = round(-other[0] - other[1])
        q_d = abs(q - other[0])
        r_d = abs(r - other[1])
        s_d = abs(s - (-other[0]-other[1]))
        if q_d > r_d and q_d > s_d:
            q = -r-s
        elif r_d > s_d:
            r = -q-s
        return (int(q), int(r))

    def hex_line(self, other):
        dist = self.hex_distance(other)
        results = []
        if dist != 0: #don't know why this suddenly broke but i'd rather this than /0 errors
            for i in range(0, dist+1):
                results.append(self.hex_round(self.hex_lerp(other, 1/dist * i)))
        return results
    
    def line_draw(self, hexlist, recolor=True, line_list=[]):
        if recolor == True:
            for hex in hexlist:
                line_list.append(Hexagon_Polar(hex[0], hex[1], True, "green"))
        elif recolor == False:
            for hex in range(len(line_list)):
                pygame.sprite.Sprite.kill(line_list[hex])
            line_list = []
        return line_list
                

    def check_facing(self): #moved from units, will be useful for multiple subclasses
        face = self.facing // 60
        if face == 6:
            face = 0
        return face

    def update(self, dt):
        pass