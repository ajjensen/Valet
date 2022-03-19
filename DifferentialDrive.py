#!/usr/bin/python3
import numpy as np
import pygame

class DifferentialDrive(pygame.sprite.Sprite):

    def __init__(self, startPos = (100,100)):
        self.imageFileName = 'DiffDrive.png'
        super(DifferentialDrive, self).__init__()

        scaleFactor = 1/10
        img_temp = pygame.image.load(self.imageFileName).convert_alpha()
        oldSize = img_temp.get_size()
        newSize = (int(oldSize[0]*scaleFactor), int(oldSize[1]*scaleFactor))
        self.surf = pygame.transform.scale(img_temp, newSize)
        self.rect = self.surf.get_rect(center = startPos)