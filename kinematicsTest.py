#!/usr/bin/python3
import numpy as np
import pygame
from DifferentialDrive import DifferentialDrive

pygame.init()
screen_width = 1024
screen_height = 768
screen =  pygame.display.set_mode((screen_width, screen_height))
screen.fill((255, 255, 255))
x0 = 100
y0 = 100
phi0 = 0
ic = (x0, y0, phi0)

car = DifferentialDrive()

running = True
plotted = False

# plot starting position
pygame.display.flip()

while running:

    if not plotted:
        for speed in car.wheelSpeeds:
            # plot a point and an arrow for new position and orientation
            q = car.Kinematics(speed, ic)
            x = q.item(0)
            y = q.item(1)
            phi = q.item(2)
            pygame.draw.circle(screen, (0,255,0), (x,y), 5)
            pygame.draw.line(screen, (0,255,0), (x,y), (x + 20*np.cos(phi), y + 20*np.sin(phi)), width=3)
            pygame.display.flip()
        plotted = True

    pygame.draw.circle(screen, (0,0,255), (x0,y0), 5)
    pygame.draw.line(screen, (0,0,255), (x0,y0), (x0 + 10*np.cos(phi0), y0 + 10*np.sin(phi0)), width=3)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
pygame.quit()