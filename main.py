import pygame
import math
pygame.init()

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (200, 50, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 180)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
TAN = (200,150,100)
width, height = 1000, 1000
window = pygame.display.set_mode((width, height))

PLANETS = []

sun_mass = (1.98847*10**30)
earth_mass = 5.9736*10**24 #sun_mass*.00000300411874456241
mars_mass = 6.4185*10**23 #sun_mass*3.2278586049e-7
venus_mass = 4.8685*10**24 #sun_mass*1.6606737844e-7
mercury_mass = 3.3022*10**23 #sun_mass*0.00000244836482321
sun_radius = 30
sun_posx,sun_posy = width//2,height//2


mur_mass = 3.285 * 10**23
mur_radius = 5

FONT = pygame.font.SysFont("comicsans", 16)
FONT2 = pygame.font.SysFont("comicsans", 30)

class Planets:
    AU = 149.6e6 *1000
    G = 6.67428e-11
    Scale = 250/AU #100
    TimeStep = 3600*24

    def __init__(self, x, y, radius,mass,color):#x_vel,y_vel):
        self.x  = x
        self.y  = y
        self.color = color
        self.radius = radius
        self.mass = mass
        self.x_vel = 0
        self.y_vel = 0
        self.orbit =[]
        self.sun = False
        self.distance_to_sun = 0

    def draw(self, win, draw_dist = False,draw_line = False):
        x = self.x *self.Scale +width/2
        y = self.y * self.Scale+height/2


        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if draw_line:
            if len(self.orbit) > 2:
                updated_points = []
                for point in self.orbit:
                    x, y = point
                    x = x * self.Scale + width / 2
                    y = y * self.Scale + height / 2
                    updated_points.append((x, y))
                pygame.draw.lines(win, self.color, False, updated_points, 2)
        if draw_dist:
            if not self.sun:
                distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)}km", 1, WHITE)
                win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def move(self):
        self.x += self.x_vel
        self.y +=0# self.y_vel

    def attraction(self,other):
        other_x,other_y = other.x,other.y
        dist_x = other_x-self.x
        dist_y = other_y-self.y
        dist = math.sqrt(dist_x**2 +dist_y**2)
        if dist ==0:
            dist = .00000001

        if other.sun:
            self.distance_to_sun = dist

        force = self.G * self.mass * other.mass / dist**2
        theta = math.atan2(dist_y,dist_x)
        force_x = math.cos(theta) *force
        force_y = math.sin(theta) * force
        return force_x,force_y

    def update_position(self,planets):
        total_forcex = total_forcey = 0
        for planet in planets:
            if self==planet:
                continue

            fx,fy = self.attraction(planet)
            total_forcex += fx
            total_forcey += fy

        self.x_vel += total_forcex / self.mass*self.TimeStep
        self.y_vel += total_forcey / self.mass * self.TimeStep

        self.x += self.x_vel * self.TimeStep
        self.y += self.y_vel * self.TimeStep
        self.orbit.append((self.x,self.y))


def set_planet_position(x,y,planet):
    # print(planet.x,planet.y)
    # print(pygame.mouse.get_pos())
    x1 = planet.x * planet.Scale + width / 2
    y1 = planet.y * planet.Scale + height / 2
    x2 =( (-1.6*x) / planet.Scale) #+ width / 2
    y2 = ((y-y) / planet.Scale) # height / 2
    if x > x1 - planet.radius and x < x1 + planet.radius:
        if y > y1 - planet.radius and y < y1 + planet.radius:
            print(2)
            planet.x,planet.y = (x - width/2)*(planet.Scale**-1), (y - width/2)*(planet.Scale**-1)






    pass

def draw(win,count):
    win.fill((0,0,0))
    count_y = count//365


    elapsed_time = FONT2.render(f'Days: {count} Years: {count_y}', 1, WHITE)
    win.blit(elapsed_time, (width -70 - elapsed_time.get_width(), 40))





def main():
    run=True
    count = 0
    clock = pygame.time.Clock()
    sun = Planets(0,0,sun_radius,sun_mass,YELLOW)
    sun.sun = True
    earth = Planets(-1*Planets.AU, 0  , sun_radius*16/30, earth_mass, BLUE)
    earth.y_vel = 29.783 * 1000

    mars = Planets(-1.524*Planets.AU, 0, sun_radius* 12/30, mars_mass, RED)
    mars.y_vel = 24.077 * 1000

    venus = Planets(.723*Planets.AU, 0, sun_radius* 14/30, venus_mass, GRAY)
    venus.y_vel = -35.02 * 1000

    mercury = Planets(.387*Planets.AU, 0, sun_radius*8/30, mercury_mass, TAN)
    mercury.y_vel = -47.4 * 1000

    planets = [sun,earth,mars,venus,mercury]

    while run:
        clock.tick(60)
        count +=int(Planets.TimeStep/(3600*24))
        draw(window,count)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x,y = pos
                # print(1)
                for planet in planets:
                    set_planet_position(x, y,planet)



        for planet in planets:
            planet.update_position(planets)
            planet.draw(window)


        pygame.display.update()
        key = pygame.key.get_pressed()
        # move_planet(key, sun)

main()
