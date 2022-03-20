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
        self.r      = 10    # Wheel radius
        self.d      = 10    # Distance from wheel to centerline of vehicle
        self.phi    = 0     # Heading of robot
        self.A = np.matrix( [[self.r*np.cos(self.phi)/2, self.r*np.cos(self.phi)/2], \
            [self.r*np.sin(self.phi)/2, self.r*np.sin(self.phi)/2], \
            [-self.r/(2*self.d), self.r/(2*self.d)]] )
        self.dt = 0.1
        # self.wheelSpeeds = [(np.pi/2, np.pi), (3*np.pi/4, 3*np.pi/4), (np.pi, np.pi/2)]
        self.wheelSpeeds = [(0, np.pi), (np.pi/2, np.pi/2), (np.pi, 0)]

    def CalcA(self, prevPose):
        x0 = prevPose[0]
        y0 = prevPose[1]
        phi0 = prevPose[2]

        A = np.matrix( [[self.r*np.cos(phi0)/2, self.r*np.cos(phi0)/2], \
            [self.r*np.sin(phi0)/2, self.r*np.sin(phi0)/2], \
            [-self.r/(2*self.d), self.r/(2*self.d)]] )
        
        return A

    def Kinematics(self, wheelSpeeds, ic):
        ul = wheelSpeeds[0]
        ur = wheelSpeeds[1]

        x0 = ic[0]
        y0 = ic[1]
        phi0 = ic[2]

        vl = ul*self.r
        vr = ur*self.r
        v = self.d * (vr + vl) 

        phi = self.r * (ur - ul) / (self.d * 2) + phi0
        x = v * np.cos(phi) * self.dt + x0
        y = v * np.sin(phi) * self.dt + y0
        q = np.matrix([[x], [y], [phi]])
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