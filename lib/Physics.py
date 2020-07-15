#!/usr/bin/env python3

import random, sys, os, pwd, math, json, numpy
import time

from Utils import *

class Physics(FilePaths):
    velocity = [0,0]
    acceleration = 0.0
    time = 1.0
    max_vel = 5

    def __init__(self,mass):
        super().__init__()
        self.mass = mass

    def accelerate(self,force):
        x,y = force
        self.acceleration = [float(x) / float(self.mass),float(y) / float(self.mass)]
        self.velocity[0] += self.acceleration[0] * self.time
        self.velocity[1] += self.acceleration[1] * self.time

        for count,vel in enumerate(self.velocity):
            if abs(vel) > self.max_vel:
                self.velocity[count] = numpy.sign(vel) * self.max_vel

    def is_collision(self):
        pass

    def rotate(self):
        pass

    