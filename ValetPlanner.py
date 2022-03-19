#!/usr/bin/python3
import numpy as np
from psutil import AccessDenied
import pygame
from Ackerman import Ackerman
from DifferentialDrive import DifferentialDrive
from Obstacle import Obstacle
from Trailer import Trailer

class ValetPlanner:

    def __init__(self, vehicleType = 'DifferentialDrive'):
        pygame.init()
        self.screen_width = 1024
        self.screen_height = 768
        self.screen =  pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill((255, 255, 255))

        if vehicleType == 'DifferentialDrive':
            self.vehicle = DifferentialDrive()
        elif vehicleType == 'Ackerman':
            self.vehicle = Ackerman()
        elif vehicleType == 'Trailer':
            self.vehicle = Trailer()
        else:
            pass

        # instantiate obstacles
        carpos1 = (100, 700)
        carpos2 = (500, 700)
        self.car_obstacle1 = Obstacle('Car', carpos1, 0.15)
        self.car_obstacle2 = Obstacle('Car', carpos2, 0.15)
        self.car_bunch = Obstacle('CarGroup', (int(self.screen_width/3), int(self.screen_height/2)), 0.2)
        
        # create groups
        self.all_sprites = pygame.sprite.Group()
        self.all_obstacles = pygame.sprite.Group()

        self.all_sprites.add(self.vehicle)
        self.all_sprites.add(self.car_obstacle1)
        self.all_sprites.add(self.car_obstacle2)
        self.all_sprites.add(self.car_bunch)
        self.all_obstacles.add(self.car_obstacle1)
        self.all_obstacles.add(self.car_obstacle2)
        self.all_obstacles.add(self.car_bunch)

        # draw all sprites
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

    def go(self):

        running = True

        # Main Game Loop
        while running:

            # Event loop for pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            

            # updates the contents of the screen
            self.screen.fill((255, 255, 255))
            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            pygame.display.flip()
        
        # Quit pygame, close screen when main game loop is exited
        pygame.quit()