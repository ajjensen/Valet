#!/usr/bin/python3
from re import U
import numpy as np
import pygame

class DifferentialDrive(pygame.sprite.Sprite):

    def __init__(self, startPos = (100,100)):
        self.imageFileName = 'DiffDrive.png'
        super(DifferentialDrive, self).__init__()

        # Pygame Image for sprite:
        scaleFactor = 1/10
        img_temp = pygame.image.load(self.imageFileName).convert_alpha()
        oldSize = img_temp.get_size()
        newSize = (int(oldSize[0]*scaleFactor), int(oldSize[1]*scaleFactor))
        self.surf = pygame.transform.scale(img_temp, newSize)
        self.rect = self.surf.get_rect(center = startPos)
        self.pos = startPos

        # Kinematic parameters:
        # self.steeringAngles = []  # Steering angles to test each step. 
        self.r      = 50    # Wheel radius
        self.d      = 50    # Distance from wheel to centerline of vehicle
        self.phi    = 0     # Heading of robot
        self.A = np.matrix( [[-self.r/(2*self.d), self.r/(2*self.d)], \
            [self.r*np.cos(self.phi)/2, self.r*np.cos(self.phi)/2], \
            [self.r*np.sin(self.phi)/2, self.r*np.sin(self.phi)/2], \
            [1, 0], \
            [0, 1]] )
        self.dt = 1.0
        self.wheelSpeeds = [(np.pi/2, np.pi), (np.pi, np.pi), (np.pi, np.pi/2)]

    def CalcA(self, phi):
        A = np.matrix( [[-self.r/(2*self.d), self.r/(2*self.d)], \
            [self.r*np.cos(phi)/2, self.r*np.cos(phi)/2], \
            [self.r*np.sin(phi)/2, self.r*np.sin(phi)/2], \
            [1, 0], \
            [0, 1]] )
        return A

    def Kinematics(self, wheelSpeeds, phi):
        u = np.matrix([[wheelSpeeds[0]], [wheelSpeeds[1]]])
        A = self.CalcA(phi)
        q = A * u * self.dt
        return q

    def Dynamics(self):
        # unimplemented
        pass

    def RungeKutta4(self):
        # unimplented
        pass

    def CalcCost(self):
        pass

    def Move(self):
        pass