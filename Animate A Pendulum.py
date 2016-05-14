import pygame, sys
from pygame.locals import *
from math import sin, cos, radians

pygame.init()

windowSize = 250
timeTick = 100
bobSize = 15

window = pygame.display.set_mode((windowSize, windowSize))
pygame.display.set_caption("Pendulum")

screen = pygame.display.get_surface()
screen.fill((255, 255,255))

pivot = (windowSize/2, windowSize/10)
swingLength = pivot[1]*4

class BobMass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.theta = 45
        self.dtheta = 0
        self.rect = pygame.Rect(pivot[0]-swingLength*cos(radians(self.theta)),
                                pivot[1]+swingLength*sin(radians(self.theta)),
                                1,1)
        self.draw()

    def recomputeAngle(self):
        scaling = 3000.0 / (swingLength**2)

        firstDDtheta = -sin(radians(self.theta))*scaling
        midDtheta = self.dtheta + firstDDtheta
        midtheta = self.theta + (self.dtheta + midDtheta) / 2.0

        midDDtheta = -sin(radians(midtheta))*scaling
        midDtheta = self.dtheta + (firstDDtheta + midDDtheta) / 2
        midtheta = self.theta + (self.dtheta + midDtheta) / 2

        midDDtheta = -sin(radians(midtheta)) * scaling
        lastDtheta = midDtheta + midDDtheta
        lasttheta = midtheta + (midDtheta + lastDtheta) / 2.0

        lastDDtheta = -sin(radians(lastDtheta)) * scaling
        lastDtheta = midDtheta + (midDDtheta + lastDDtheta) / 2.0
        lasttheta = midtheta + (midDtheta + lastDtheta) / 2.0

        self.dtheta = lastDtheta
        self.theta = lasttheta
        self.rect = pygame.Rect(pivot[0] - swingLength*sin(radians(self.theta)),
                                pivot[1]+swingLength*cos(radians(self.theta)), 1,1)

    def draw(self):
        pygame.draw.circle(sceen, (0,0,0), pivot, 5. 0)
        pygame.draw.cirle(screen, (0,0,0), self.rect.center, bobSize, 0)
        pygame.draw.aaline(screen, (0,0,0), pivot, self.rect.center)
        pygame.draw.line(screen, (0,0,0), (0,pivot[1]), (windowSize, pivot[1]))


    def update(self):
        self.recomputeAngle()
        screen.fill((255, 255, 255))
        self.draw()

bob = BobMass()

tick = userEvent + 2
pygame.time.set_timer(tick, timeTick)

def input(events):
    for event in events:
        if event.type == quit():
            sys.exit(0)
        elif event.type == tick:
            bob.update()
while True:
    input(pygame.event.get())
    pygame.display.flip()