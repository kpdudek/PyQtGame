#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, math
import numpy as np
import ctypes

from Utils import *
from PaintUtils import *
from Physics import *
from Geometry import *
from Sprite import *

class DynamicObstacles(Colors,FilePaths):
    
    def __init__(self,width,height):
        super().__init__()

        self.width = width
        self.height = height

        self.sprites = []
        self.num_sprites = 0

        self.player = None

        # C library for collision checking
        self.c_float_p = ctypes.POINTER(ctypes.c_double)
        self.fun = ctypes.CDLL(f'{self.user_path}lib/{self.cc_lib_path}')
        self.fun.polygon_is_collision.argtypes = [self.c_float_p,ctypes.c_int,ctypes.c_int,self.c_float_p,ctypes.c_int,ctypes.c_int] 

    def ball(self,x,y,dir=0.):
        list_idx = self.num_sprites
        sprite = Sprite('mouse/right/',list_idx=list_idx,name=f'Test_{len(self.sprites)+1}',ang=0.,scale=40,physics={'mass':12.,'max_vel':10.})
        sprite.direction(dir)
        x = np.array([x])
        y = np.array([y])
        sprite.polys[sprite.idx].teleport(x,y)
        sprite.pose = np.array([x,y]) + sprite.centroid_offsets[sprite.idx]
        
        self.sprites.append(sprite)
        self.num_sprites += 1

    def remove_ball(self,idx=None):
        if len(self.sprites)==0:
            return

        if idx:
            self.sprites.pop(idx)
        else:
            self.sprites.pop()

        self.num_sprites -= 1    

    def update_position(self,obstacles):
        for idx in range(0,len(self.sprites)):
            if not self.sprites[idx].skip_physics:
                self.sprites[idx].physics.gravity()
                # self.collision_check(obstacles,idx)

                x_diff = self.sprites[idx].pose[0]-self.player.sprite.pose[0]
                y_diff = self.sprites[idx].pose[1]-self.player.sprite.pose[1]
                dist = math.sqrt(math.pow(x_diff,2) + math.pow(y_diff,2))
                if dist < 250:
                    max_x_force = 1.
                    max_y_force = 50.
                    force = np.array([(1./x_diff)*55,(1./y_diff)*500])
                    if abs(force[0]) > max_x_force:
                        force[0] = np.sign(force[0])*max_x_force
                    if abs(force[1]) > max_y_force:
                        force[1] = np.sign(force[1])*max_y_force
                else:
                    force = np.array([[0.],[0.]])
                
                self.sprites[idx].physics.accelerate(force)
                
                self.collision_check(obstacles,idx)
                self.sprites[idx].animate(self.sprites[idx].physics.velocity[0])
            else:
                self.sprites[idx].animate(self.sprites[idx].physics.velocity[0])

    def collision_check(self,obstacles,idx):
        offsets = self.sprites[idx].centroid_offsets[self.sprites[idx].idx]
        self.sprites[idx].polys[self.sprites[idx].idx].teleport(self.sprites[idx].pose[0]-offsets[0],self.sprites[idx].pose[1]-offsets[1])

        # X Collision Check
        self.sprites[idx].polys[self.sprites[idx].idx].translate(self.sprites[idx].physics.velocity[0],0.)
        collision = False
        for obstacle in obstacles:
            if sphere_is_collision(self.sprites[idx].polys[self.sprites[idx].idx],obstacle):
                data = copy.deepcopy(self.sprites[idx].polys[self.sprites[idx].idx].vertices)
                data = data.astype(np.double)
                data_p = data.ctypes.data_as(self.c_float_p)

                data2 = copy.deepcopy(obstacle.vertices)
                data2 = data2.astype(np.double)
                data_p2 = data2.ctypes.data_as(self.c_float_p)

                # C Function call in python
                res = self.fun.polygon_is_collision(data_p,2,len(self.sprites[idx].polys[self.sprites[idx].idx].vertices[0,:]),data_p2,2,len(obstacle.vertices[0,:]))
                if res:
                    collision = True
                    break
    
        if collision:
            self.sprites[idx].polys[self.sprites[idx].idx].translate(-1*self.sprites[idx].physics.velocity[0],0.)
            self.sprites[idx].physics.velocity[0] = 0.
        else:
            t = np.array([self.sprites[idx].physics.velocity[0],[0.]])
            self.sprites[idx].pose += t
        
        # Y Collision Check
        self.sprites[idx].polys[self.sprites[idx].idx].translate(0.,self.sprites[idx].physics.velocity[1])
        collision = False
        for obstacle in obstacles:
            if sphere_is_collision(self.sprites[idx].polys[self.sprites[idx].idx],obstacle):
                data = copy.deepcopy(self.sprites[idx].polys[self.sprites[idx].idx].vertices)
                data = data.astype(np.double)
                data_p = data.ctypes.data_as(self.c_float_p)

                data2 = copy.deepcopy(obstacle.vertices)
                data2 = data2.astype(np.double)
                data_p2 = data2.ctypes.data_as(self.c_float_p)

                # # C Function call in python
                res = self.fun.polygon_is_collision(data_p,2,len(self.sprites[idx].polys[self.sprites[idx].idx].vertices[0,:]),data_p2,2,len(obstacle.vertices[0,:]))
                if res:
                    collision = True
                    break

        if collision:
            self.sprites[idx].polys[self.sprites[idx].idx].translate(0.,-1*self.sprites[idx].physics.velocity[1])
            self.sprites[idx].physics.velocity[1] = 0.
        else:
            t = np.array([[0.],self.sprites[idx].physics.velocity[1]])
            self.sprites[idx].pose += t

