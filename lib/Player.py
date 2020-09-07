#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, math
import numpy as np
from multiprocessing import Pool
import ctypes

from Utils import *
from PaintUtils import *
from Physics import *
from Geometry import *
from Sprite import *

class Player(QWidget,Colors,FilePaths):
    key_force = 2.
    sprint_multiplier = 2.5
    boost = 28.
    max_vel = 11.
    mass = 12.

    force = np.array([ [0.] , [0.] ])
    velocity = 0.
    collision_str = np.zeros(2).reshape(2,1)
    mouse_pos = np.zeros(2).reshape(2,1) - 1
    mouse_prev = np.zeros(2).reshape(2,1) - 1

    info_signal = pyqtSignal(object)
    pause_signal = pyqtSignal()
    collision_signal = pyqtSignal(object)
    
    def __init__(self,width,height):
        super().__init__()

        self.width = width
        self.height = height

        self.sprite = Sprite('cat/left/',scale=60)

        self.physics = PlayerPhysics(self.mass,self.max_vel)
        self.physics.info_signal.connect(self.send_info)

        # C library for collision checking
        self.c_float_p = ctypes.POINTER(ctypes.c_double)
        self.fun = ctypes.CDLL(f'{self.user_path}lib/cc_lib.so') # Or full path to file           
        self.fun.polygon_is_collision.argtypes = [self.c_float_p,ctypes.c_int,ctypes.c_int,self.c_float_p,ctypes.c_int,ctypes.c_int] 
    
    def send_info(self,info):
        self.info_signal.emit(info)

    def update_position(self,key_press,sprint,mouse_pos,obstacles):
        if len(key_press) != 0:
            self.force = np.array([ [0.] , [0.] ])

            for key in key_press:
                if key == 'right':
                    self.force[0] = self.key_force
                    # self.geom = 'left_1.png'
                    self.sprite.direction(0.)       
                elif key == 'left':
                    self.force[0] = -self.key_force
                    # self.geom = 'left_1.png'
                    self.sprite.direction(180.)
                
                if sprint:
                    self.force[0] = self.force[0] * self.sprint_multiplier

                if self.collision_str[1] == 1:
                    if key == 'up':
                        self.force[1] = -self.boost*self.key_force
                    elif key == 'down':
                        self.force[1] = self.key_force
        else:
            self.force = np.array([ [0.] , [0.] ])

        if np.sum(mouse_pos) >= 0:
            self.mouse_pos = mouse_pos # Always keep track of the mouse pose for drawing the red marker

            self.sprite.polys[self.sprite.idx].teleport(mouse_pos[0],mouse_pos[1])
            self.sprite.pose = mouse_pos + self.sprite.centroid_offsets[self.sprite.idx]

            if np.sum(self.mouse_prev) >= 0:
                mouse_vel = mouse_pos - self.mouse_prev
                self.physics.velocity = mouse_vel
            self.mouse_prev = mouse_pos
            self.physics.send_info()
            return
        else: # Always keep track of the mouse pose for drawing the red marker
            self.mouse_pos = mouse_pos

        self.collision_str = np.zeros(2).reshape(2,1)

        self.physics.gravity()
        self.collision_check(obstacles)

        self.physics.accelerate(self.force)
        self.collision_check(obstacles)

        self.collision_signal.emit(self.collision_str)

        self.physics.send_info()

        self.sprite.animate(self.physics.velocity[0])

    def collision_check(self,obstacles):
        # X Collision Check
        offsets = self.sprite.centroid_offsets[self.sprite.idx]
        self.sprite.polys[self.sprite.idx].teleport(self.sprite.pose[0]-offsets[0],self.sprite.pose[1]-offsets[1])

        self.sprite.polys[self.sprite.idx].translate(self.physics.velocity[0],0.)
        collision = False

        for obstacle in obstacles:
            if sphere_is_collision(self.sprite.polys[self.sprite.idx],obstacle):
                data = copy.deepcopy(self.sprite.polys[self.sprite.idx].vertices)
                data = data.astype(np.double)
                data_p = data.ctypes.data_as(self.c_float_p)

                data2 = copy.deepcopy(obstacle.vertices)
                data2 = data2.astype(np.double)
                data_p2 = data2.ctypes.data_as(self.c_float_p)

                # C Function call in python
                res = self.fun.polygon_is_collision(data_p,2,len(self.sprite.polys[self.sprite.idx].vertices[0,:]),data_p2,2,len(obstacle.vertices[0,:]))
                if res:
                    collision = True
                    break
    
        if collision:
            self.sprite.polys[self.sprite.idx].translate(-1*self.physics.velocity[0],0.)
            self.collision_str[0] = 1
            self.physics.velocity[0] = 0.
        else:
            t = np.array([self.physics.velocity[0],[0.]])
            self.sprite.pose += t
        
        # Y Collision Check
        self.sprite.polys[self.sprite.idx].translate(0.,self.physics.velocity[1])
        collision = False
        for obstacle in obstacles:
            if sphere_is_collision(self.sprite.polys[self.sprite.idx],obstacle):
                data = copy.deepcopy(self.sprite.polys[self.sprite.idx].vertices)
                data = data.astype(np.double)
                data_p = data.ctypes.data_as(self.c_float_p)

                data2 = copy.deepcopy(obstacle.vertices)
                data2 = data2.astype(np.double)
                data_p2 = data2.ctypes.data_as(self.c_float_p)

                # # C Function call in python
                res = self.fun.polygon_is_collision(data_p,2,len(self.sprite.polys[self.sprite.idx].vertices[0,:]),data_p2,2,len(obstacle.vertices[0,:]))
                if res:
                    collision = True
                    break

        if collision:
            self.sprite.polys[self.sprite.idx].translate(0.,-1*self.physics.velocity[1])
            self.collision_str[1] = 1
            self.physics.velocity[1] = 0.
        else:
            t = np.array([[0.],self.physics.velocity[1]])
            self.sprite.pose += t
