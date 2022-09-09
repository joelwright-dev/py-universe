import enum
from ipaddress import NetmaskValueError
from re import S
import pygame
import pygame.math as pymath
import random
import math

pygame.init()

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
space = pygame.Color("#0C0C1D")
c1 = pygame.Color("#2E1760")
c2 = pygame.Color("#3423A6")
c3 = pygame.Color("#7180B9")
c4 = pygame.Color("#FFA630")

#Create window
size = (800,800)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("Complex Behaviour")

running = True
clock = pygame.time.Clock()

def addVectors(vector1, vector2):
    """ Returns the sum of two vectors """
    
    # x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    # y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    # angle  = 0.5 * math.pi - math.atan2(y, x)
    # length = math.hypot(x, y)

    print("he", vector1, vector2)

    vector = vector1 + vector2
    vector = vector.as_polar()

    return (vector)

class Dot(pygame.sprite.Sprite):
    def __init__(self,color,position,charge,mass,isNucleon):
        super().__init__()
        self.color = color
        self.position = pygame.math.Vector2(position)
        self.charge = charge
        self.mass = mass
        self.isNucleon = isNucleon
        self.dir = pygame.math.Vector2(position).normalize()
        self.velocityx = random.randint(-10, 10)/100
        self.velocityy = random.randint(-10, 10)/100
        self.radius = 2
        self.image = pygame.Surface([self.radius*2,self.radius*2])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        #pygame.draw.circle(self.image, self.color, (self.radius*2 // 2, self.radius*2 // 2), self.radius)
        #self.rect = self.image.get_rect(center = (round(self.position.x), round(self.position.y)))

    def reflect(self, NV):
        self.dir = self.dir.reflect(pygame.math.Vector2(NV))

    def update(self):
        self.rect.center = round(self.position.x), round(self.position.y)

    def draw(self,screen):
        screen.blit(self.image,self.rect)

def create(count,color,charge,mass,isNucleon):
    dots = []
    for i in range(count):
        if(isNucleon):
            position = (random.randint(350, 450),random.randint(350, 450))
        else:
            position = (random.randint(0,screen.get_size()[0]),random.randint(0,screen.get_size()[1]))
        dot = Dot(color,position,charge,mass,isNucleon)
        dots.append(dot)

    return dots

def update(group,screen):
    for particle in group:
        particle.update()
        particle.rect.clamp_ip(screen.get_rect())
        particle.draw(screen)

class Square(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        self.color = WHITE
        self.position = pygame.math.Vector2(position)
        self.image = pygame.Surface([size,size])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.charge = 1

    def update(self):
        self.rect.center = round(self.position.x), round(self.position.y)

    def draw(self,screen):
        screen.blit(self.image,self.rect)


def fieldcreate(field, resolution):
    squares = []
    for i in range(math.ceil(screen.get_size()[0]/resolution)+1):
        for j in range(math.ceil(screen.get_size()[1]/resolution)+1):
            position = (i*resolution, j*resolution)
            square = Square(position, resolution)
            squares.append(square)
    return squares

# up = create(18,YELLOW,2/3)
# down = create(18,BLUE,-1/3)
# electron = create(6,WHITE,-1)



def calculate_strong(distance):
    F = S * 1/distance**2
    return F

def calculate_residual_strong(distance, p1, p2):
    F = 0
    if(p1.isNucleon and p2.isNucleon):
        if distance < Sd:
            F = - S * (1 / (1 + math.e**(-8*(distance-0.5)/Sd)) + 1)
        else: 
            F = S * (2 / (1 + math.e**(-4*(distance-1.5)/Sd)) - 1)
    return F

def calculate_electromagnetic(distance,p1,p2):
    F = E * (p1.charge * p2.charge)/(distance**2+dampener)
    return F

def add_momentum(xmomentum,ymomentum, a):
    calculateNetMomentum()
    xmomentum *= 2
    ymomentum *= 2
    mass = 0
    for particle in all_particles:
        if particle != a:
            mass += particle.mass
    xvelocity = xmomentum/mass
    yvelocity = ymomentum/mass

    for particle in all_particles:
        if particle != a:
            particle.velocityx += xvelocity
            particle.velocityy += yvelocity

def update_velocity():
    for p1 in all_particles:
        fx = 0
        fy = 0
        for p2 in all_particles:
            if(p1 != p2):
                dx = p1.position.x - p2.position.x
                dy = p1.position.y - p2.position.y
                d = math.sqrt(dx**2 + dy**2)

                if d > 0:
                    F = calculate_residual_strong(d, p1, p2) + calculate_electromagnetic(d,p1,p2)
                    fx += F * dx/d
                    fy += F * dy/d
                    # else:
                #     F = random.randint(1,10)
                #     fx += F * dx/1000
                #     fy += F * dy/1000

        p1.velocityx = p1.velocityx + fx/p1.mass
        p1.velocityy = p1.velocityy + fy/p1.mass

def update_position():
    for a in all_particles:
        a.position.x += a.velocityx
        a.position.y += a.velocityy

        # if(a.position.x <= 0 or a.position.x >= screen.get_size()[0]):
        #     #add_momentum(a.velocityx*a.mass,0, a)
        #     a.velocityx = -1*a.velocityx
        #     calculateNetMomentum()
        # if(a.position.y <= 0 or a.position.y >= screen.get_size()[1]):
        #     #add_momentum(0,a.velocityy*a.mass, a)
        #     a.velocityy = -1*a.velocityy
        #     calculateNetMomentum()

def move():
    for i in range(DOS):
        update_velocity()
        update_position()

def calculateNetMomentum():
    momentumx=0
    momentumy=0
    for particle in all_particles:
        momentumx += particle.velocityx*particle.mass
        momentumy += particle.velocityy*particle.mass

    print(momentumx,momentumy)

def convertMagnitude(magnitude):
    # const = 100
    # intensity = magnitude*const
    # if intensity>255:
    #     intensity=255
    # colour = (intensity, intensity, intensity)
    # return colour

    const = 255
    intensity = const/(1+math.e**(-magnitude*10))
    colour = (intensity, intensity, intensity)
    return colour

def calculateField(field, particles):
    for region in field:
        fpx = 0
        fpy = 0
        fnx = 0
        fny = 0
        for particle in particles:
            dx = region.position.x - particle.position.x
            dy = region.position.y - particle.position.y
            d = math.sqrt(dx**2 + dy**2)
            F = calculate_electromagnetic(d,region,particle)
            if(particle.charge>0):
                fpx += F * dx/d
                fpy += F * dy/d
            else:
                fnx += F * dx/d
                fny += F * dy/d
        
        magnitude = math.sqrt(fpx**2+fpy**2)-math.sqrt(fnx**2+fny**2)
        region.colour = convertMagnitude(magnitude)
        region.image.fill(region.colour)

def freecam():
    keys = pygame.key.get_pressed()
    #shift = [0, 0]
    if keys[pygame.K_a]:
        shift[0] += speed
    if keys[pygame.K_d]:
        shift[0] -= speed
    if keys[pygame.K_w]:
        shift[1] += speed
    if keys[pygame.K_s]:
        shift[1] -= speed
    for particle in all_particles:
        particle.position.x += shift[0]
        particle.position.y += shift[1]



elecromagnaticfield = fieldcreate("ELECTROMAGNATIC", 10)
protons = create(20,YELLOW,1,10,True)
neutrons = create(20,GREEN,0,1000,True)
electrons = create(20, RED,-1,1,False)
#neutrons = create(10,BLUE,0,1839)

all_particles = protons + neutrons + electrons

S = 0.2
Sd = 100
E = 10
dampener = 10
DOS = 10

shift = [0, 0]
speed = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(space)
    # update(up,screen)
    # update(down,screen)

    #update(electron,screen)

    move()
    calculateField(elecromagnaticfield, all_particles)
    update(elecromagnaticfield, screen)
    update(protons,screen)
    update(neutrons,screen)
    update(electrons,screen)

    freecam()

    pygame.display.flip()

    clock.tick(10)

pygame.quit()