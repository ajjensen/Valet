#!/usr/bin/python3
import numpy as np
import pygame
from DifferentialDrive import DifferentialDrive

pygame.init()
screen_width = 1024
screen_height = 768
screen =  pygame.display.set_mode((screen_width, screen_height))
screen.fill((255, 255, 255))
startx = 100
starty = 100

car = DifferentialDrive()

running = True
plotted = False

while running:
    pygame.draw.circle(screen, (0,0,255), (startx,starty), 2)
    pose = np.matrix([startx, starty, 0])

    if not plotted:
        for speed in car.wheelSpeeds:
            # plot a point and an arrow for new position and orientation
            q = car.Kinematics(speed, pose)
            x = q.item(0)
            y = q.item(1)
            phi = q.item(2)
            # pygame.draw.circle(screen, (0,255,0), (x,y), 10)
            pygame.draw.line(screen, (0,255,0), (x,y), (x + 10*np.cos(phi), y + 10*np.sin(phi)), width=3)
            pygame.display.flip()
        plotted = True
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
pygame.quit()