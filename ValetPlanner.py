#!/usr/bin/python3
import numpy as np
from psutil import AccessDenied
import pygame
from Ackerman import Ackerman
from DifferentialDrive import DifferentialDrive
from Obstacle import Obstacle
from Trailer import Trailer
from pygame.locals import (RLEACCEL, QUIT)
from queue import PriorityQueue
import anytree


class ValetPlanner:

    def __init__(self, vehicleType = 'DifferentialDrive'):
        self.maxCount = 2500
        self.startPos = (100, 100, 0)
        self.posTol = (-20, 20)
        self.hdTol = (-np.pi/8, np.pi/8)
        self.Open = PriorityQueue()
        self.current = 0

        pygame.init()
        self.screen_width = 1024
        self.screen_height = 768
        self.screen =  pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill((255, 255, 255))
        
        # instantiate obstacles
        carpos1 = (500, 700)
        self.car_obstacle1 = Obstacle('Car', carpos1, 0.15)
        self.car_bunch = Obstacle('CarGroup', (int(self.screen_width/3), int(self.screen_height/2)), 0.2)
        
        # create groups
        self.all_sprites = pygame.sprite.Group()
        self.all_obstacles = pygame.sprite.Group()
        # create group for possible paths

        self.all_sprites.add(self.car_obstacle1)
        self.all_sprites.add(self.car_bunch)
        self.all_obstacles.add(self.car_obstacle1)
        self.all_obstacles.add(self.car_bunch)

        if vehicleType == 'DifferentialDrive':
            self.vehicle = DifferentialDrive(self.startPos)
            self.all_sprites.add(self.vehicle)
            carpos2 = (900, 700)
            self.qGoal = (carpos1[0] + (carpos1[0]-carpos2[0])/2, carpos1[1], np.pi)
            self.car_obstacle2 = Obstacle('Car', carpos2, 0.15)
            self.all_sprites.add(self.car_obstacle2)
            self.all_obstacles.add(self.car_obstacle2)
        elif vehicleType == 'Ackerman':
            self.vehicle = Ackerman()
            self.all_sprites.add(self.vehicle)
            carpos2 = (900, 700)
            self.qGoal = (carpos1 + (carpos1[0]-carpos2[0])/2, carpos1[1], np.pi)
            self.car_obstacle2 = Obstacle('Car', carpos2, 0.15)          
            self.all_sprites.add(self.car_obstacle2)
            self.all_obstacles.add(self.car_obstacle2)
        elif vehicleType == 'Trailer':
            self.vehicle = Trailer()
            self.all_sprites.add(self.vehicle)
        else:
            pass

        # draw all sprites
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

    def DrawPath(self, parent, child, color=(192, 192, 192)):
        pygame.draw.line(self.screen, color, parent, child, width=3)

    def DrawBoundary(self):
        # Not implemented
        pass

    def h(self):
        return 0


    def AStarSearch(self):
        if not self.Open.empty():
            self.current = self.Open.get()
        else:
            return False

        if self.InTolerance(self.current[0][0]):
            return True

        for speed in self.vehicle.wheelSpeeds:

            neighbor_matrix     = self.vehicle.Kinematics(speed, self.current[0][0])
            neighbor            = (neighbor_matrix.item(0), neighbor_matrix.item(1), neighbor_matrix.item(2))
            neighbor_gScore     = self.vehicle.CalcCost(self.current[0][0:2], neighbor)
            tentative_gScore    = self.current[1] + neighbor_gScore
            self.DrawPath(self.current[0][0][0:2], neighbor[0:2])

            if tentative_gScore < neighbor_gScore:
                parentPose = self.current
                this_gScore = tentative_gScore
                this_fScore = tentative_gScore + self.h(neighbor)

                self.Open.put( ((neighbor, parentPose, this_fScore), this_gScore) )

    def PerformMotion(self):
        pass

    def InTolerance(self, pos):
        qGoal_lower = (self.qGoal[0] + self.posTol[0], self.qGoal[1] + self.posTol[0], self.qGoal[2] + self.hdTol[0])
        qGoal_upper = (self.qGoal[0] + self.posTol[1], self.qGoal[1] + self.posTol[1], self.qGoal[2] + self.hdTol[1])

        if (pos >= (qGoal_lower)) and (pos <= (qGoal_upper)):
            return True
        else:
            return False


    def go(self):
        # Custom event for when the vehicle reaches the Goal
        SUCCESS = pygame.USEREVENT + 1
        FAILED = pygame.USEREVENT + 2

        running = True
        done = False
        count = 0
        cost = np.inf   # g() - cost of cheapest path from start to n currently known
        f = np.inf      # f() - current best guess of how short a path can be through n
        self.Open.put( ((self.startPos, (), 0), 0) )     # ((currentPose, parentPose, fScore), gScore)

        # Main Game Loop + Planning algorithm
        while running:

            # continue search
            if ~done and self.AStarSearch():
                    pygame.event.post(pygame.event.Event(SUCCESS))
            elif self.Open.empty():
                    pygame.event.post(pygame.event.Event(FAILED))

            # Event loop for pygame
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == SUCCESS:
                    done = True
                    self.PerformMotion()
                if event.type == FAILED:
                    done = True

            # updates the contents of the screen
            self.screen.fill((255, 255, 255))
            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            pygame.display.flip()
        
        # Quit pygame, close screen when main game loop is exited
        pygame.quit()