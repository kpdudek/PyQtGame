#!/usr/bin/env python3

import random, sys, os, math, json
import numpy as np
import time

from Utils import *

class PhysicsInfo(object):
    physics_info = {'velocity':None,'acceleration':None,'max_vel':None,'grav_accel':None,'drag':None,'force':None,'mass':None,'touching_ground':None,}

    def __init__(self,mass,grav_accel,max_vel):
        self.physics_info['mass'] = mass
        self.physics_info['grav_accel'] = grav_accel
        self.physics_info['max_vel'] = max_vel
    
    def assign(self,force,drag,acceleration,velocity,touching_ground):
        self.physics_info['force'] = force
        self.physics_info['drag'] = drag
        self.physics_info['acceleration'] = acceleration
        self.physics_info['velocity'] = velocity
        self.physics_info['touching_ground'] = touching_ground

class Physics(QWidget,FilePaths):
    velocity = np.array([ [0.] , [0.] ])
    acceleration = np.array([ [0.] , [0.] ])
    
    max_vel = 18
    c_d = 0.06
    time = 1.0
    grav_accel = np.array([ [0.] , [13.] ])

    touching_ground = False
    info_signal = pyqtSignal(object)

    def __init__(self,mass):
        super().__init__()
        self.mass = mass

        self.info = PhysicsInfo(self.mass,self.grav_accel,self.max_vel)

    def accelerate(self,force):
        self.force = force
        # self.gravity()
        self.compute_drag()

        # x,y = self.force
        self.acceleration = self.force/self.mass#[float(x) / float(self.mass),float(y) / float(self.mass)]
        # self.velocity[0] += self.acceleration[0] * self.time
        # self.velocity[1] += self.acceleration[1] * self.time
        self.velocity += self.acceleration*self.time

        for count,vel in enumerate(self.velocity):
            if abs(vel) > self.max_vel:
                self.velocity[count] = np.sign(vel) * self.max_vel

        self.info.assign(self.force,self.drag,self.acceleration,self.velocity,self.touching_ground)
        self.info_signal.emit(self.info)

    def gravity(self):
        # self.velocity[1] += self.grav_accel * self.time
        self.accelerate(self.grav_accel)

    def compute_drag(self):
        if np.sum(self.force) < 0.01:
            return
        sign = -1 * np.sign(self.velocity[0])
        self.drag = sign * self.c_d * abs(self.velocity[0])
        self.velocity[0] += self.drag

    def is_collision(self):
        pass

    def rotate(self):
        pass

    