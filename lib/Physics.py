#!/usr/bin/env python3

import random, sys, os, math, json, numpy
import time

from Utils import *

class PhysicsInfo(object):
    velocity = None
    acceleration = None
    max_vel = None
    grav_accel = None
    drag = None
    force = None
    mass = None
    touching_ground = None

    def __init__(self,mass,grav_accel,max_vel):
        self.mass = mass
        self.grav_accel = grav_accel
        self.max_vel = max_vel
    
    def assign(self,force,drag,acceleration,velocity,touching_ground):
        self.force = force
        self.drag = drag
        self.acceleration = acceleration
        self.velocity = velocity
        self.touching_ground = touching_ground

class Physics(QWidget,FilePaths):
    velocity = [0,0]
    acceleration = [0,0]
    
    max_vel = 8

    time = 1.0
    grav_accel = 1.5

    touching_ground = False
    
    info_signal = pyqtSignal(object)

    def __init__(self,mass):
        super().__init__()
        self.mass = mass

        self.info = PhysicsInfo(self.mass,self.grav_accel,self.max_vel)

    def accelerate(self,force):
        self.force = force
        self.gravity()
        self.drag()

        x,y = self.force
        self.acceleration = [float(x) / float(self.mass),float(y) / float(self.mass)]
        self.velocity[0] += self.acceleration[0] * self.time
        self.velocity[1] += self.acceleration[1] * self.time

        for count,vel in enumerate(self.velocity):
            if abs(vel) > self.max_vel:
                self.velocity[count] = numpy.sign(vel) * self.max_vel

        self.info.assign(self.force,self.drag,self.acceleration,self.velocity,self.touching_ground)
        self.info_signal.emit(self.info)

    def gravity(self):
        self.velocity[1] += self.grav_accel * self.time

    def drag(self):
        sign = -1 * numpy.sign(self.velocity[0])
        drag = sign * 0.06 * abs(self.velocity[0])
        self.velocity[0] += drag

    def is_collision(self):
        pass

    def rotate(self):
        pass

    