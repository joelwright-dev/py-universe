import enum
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
size = (700,600)
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
    def __init__(self,color,position,charge,mass):
        super().__init__()
        self.color = color
        self.position = pygame.math.Vector2(position)
        self.charge = charge
        self.mass = mass
        self.dir = pygame.math.Vector2(position).normalize()
        self.velocityx = 0
        self.velocityy = 0
        self.radius = random.randint(3,3)
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

def create(count,color,charge,mass):
    dots = []
    for i in range(count):
        position = (random.randint(0,screen.get_size()[0]),random.randint(0,screen.get_size()[1]))
        dot = Dot(color,position,charge,mass)
        dots.append(dot)

    return dots

def update(group,screen):
    for particle in group:
        particle.update()
        particle.rect.clamp_ip(screen.get_rect())
        particle.draw(screen)

def attract(particles1, particles2, force):
    S = 0
    E = 1

    for i in range(len(particles1)):
        fx = 0
        fy = 0

        for j in range(len(particles2)):
            a = particles1[i]
            b = particles2[j]
            dx = a.position.x - b.position.x
            dy = a.position.y - b.position.y
            d = math.sqrt(dx**2 + dy**2)

            if(d > 0):
                if force == "STRONG":
                    F = S * 1/d**2
                elif force == "ELECTROMAGNETIC":
                    F = -E * (a.charge * b.charge)/d**2
                fx += F * dx/d
                fy += F * dy/d

        a.velocityx = (a.velocityx + fx)*0.5
        a.velocityy = (a.velocityy + fy)*0.5
        a.position.x += a.velocityx
        a.position.y += a.velocityy

        if(a.position.x <= 0 or a.position.x >= screen.get_size()[0]):
            a.velocityx = -1*a.velocityx
            a.velocityx += 1
        if(a.position.y <= 0 or a.position.y >= screen.get_size()[1]):
            a.velocityy = -1*a.velocityy
            a.velocityy +=1 

# up = create(18,YELLOW,2/3)
# down = create(18,BLUE,-1/3)
# electron = create(6,WHITE,-1)

S = 1
E = 100

def calculate_strong(distance):
    F = S * 1/distance**2
    return F

def calculate_electromagnetic(distance,p1,p2):
    F = E * (p1.charge * p2.charge)/distance**2
    return F

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
                    F = calculate_strong(d) + calculate_electromagnetic(d,p1,p2)
                    fx += F * dx/d
                    fy += F * dy/d
                else:
                    F = random.randint(1,10)
                    fx += F * dx/100
                    fy += F * dy/100

        p1.velocityx = p1.velocityx + fx/p1.mass
        p1.velocityy = p1.velocityy + fy/p1.mass

def update_position():
    for a in all_particles:
        a.position.x += a.velocityx
        a.position.y += a.velocityy

        if(a.position.x <= 0 or a.position.x >= screen.get_size()[0]):
            a.velocityx = -1*a.velocityx
        if(a.position.y <= 0 or a.position.y >= screen.get_size()[1]):
            a.velocityy = -1*a.velocityy

def move():
    update_velocity()
    update_position()

protons = create(10,YELLOW,1,1836)
electrons = create(10, WHITE,-1,1)
# neutrons = create(150,BLUE,0)

all_particles = protons + electrons

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(space)
    # update(up,screen)
    # update(down,screen)

    #update(electron,screen)

    move()
    update(protons,screen)
    update(electrons,screen)

    # randomnumber = random.randint(1,10)
    # if randomnumber == 1:
    #     position = (random.randint(0,screen.get_size()[0]),random.randint(0,screen.get_size()[1]))
    #     dot = Dot(BLUE,position)
    #     protons.append(dot)

    # attract(protons,neutrons,"ELECTROMAGNETIC")
    # attract(neutrons,protons,"ELECTROMAGNETIC")
    # attract(protons,protons,"ELECTROMAGNETIC")

    # attract(protons,protons,"STRONG")
    # attract(protons,neutrons,"STRONG")
    # attract(neutrons,neutrons,"STRONG")
    # attract(neutrons,protons,"STRONG")

    pygame.display.flip()

    clock.tick(1000)

pygame.quit()