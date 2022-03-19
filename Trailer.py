#!/usr/bin/python3
from Vehicle import *

class Trailer(Vehicle):

    def __init__(self, startPos = (10,10)):
        self.image = 'Trailer.png'
        super(Trailer, self).__init__(self.image, startPos)