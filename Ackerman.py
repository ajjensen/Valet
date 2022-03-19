#!/usr/bin/python3
from Vehicle import *

class Ackerman(Vehicle):

    def __init__(self, startPos = (10,10)):
        self.image = 'Ackerman.png'
        super(Ackerman, self).__init__(self.image, startPos)