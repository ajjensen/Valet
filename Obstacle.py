#!/usr/bin/python3
import pygame

class Obstacle(pygame.sprite.Sprite):

    def __init__(self, obsType = 'Car', startPos = (100, 700), scaleFactor = 0.1):
        if obsType == 'Car':
            self.imageFileName = 'ObstacleCar.png'
        else:
            self.imageFileName = 'CarGroup.png'
        
        super(Obstacle, self).__init__()
        img_temp = pygame.image.load(self.imageFileName).convert_alpha()
        oldSize = img_temp.get_size()
        newSize = (int(oldSize[0]*scaleFactor), int(oldSize[1]*scaleFactor))
        self.surf = pygame.transform.scale(img_temp, newSize)
        self.rect = self.surf.get_rect(center = startPos)