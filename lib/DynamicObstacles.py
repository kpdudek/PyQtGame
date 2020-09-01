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

class DynamicObstacles(QWidget,Colors,FilePaths):
    
    def __init__(self,width,height):
        super().__init__()

        self.width = width
        self.height = height

        self.polys = []
        self.centroid_offsets = []
        self.physics = []
        self.pixmaps = []
        self.poses = []
        self.sizes = []

        # C library for collision checking
        self.c_float_p = ctypes.POINTER(ctypes.c_double)
        self.fun = ctypes.CDLL(f'{self.user_path}lib/cc_lib.so')
        self.fun.polygon_is_collision.argtypes = [self.c_float_p,ctypes.c_int,ctypes.c_int,self.c_float_p,ctypes.c_int,ctypes.c_int] 

    def ball(self,x,y):
        pixmap = QPixmap(f'{self.user_path}graphics/ball.png')
        self.pixmaps.append(pixmap)

        size = [pixmap.size().width(),pixmap.size().height()]
        pose = np.array([ [x] , [y] ])
        self.poses.append(pose)
        self.sizes.append(size)

        x_c = pose[0] + (size[0]/2.)
        y_c = pose[1] + (size[1]/2.)

        poly = Polygon()
        poly.unit_circle(6,math.ceil(size[0]/2.))
        poly.teleport(x_c,y_c)
        self.polys.append(poly)

        centroid_offset = pose - poly.sphere.pose
        self.centroid_offsets.append(centroid_offset)

        physics = Physics(10.,15.)
        # print(physics.id())
        self.physics.append(physics)

    def remove_ball(self,idx=None):
        if len(self.polys)==0:
            return
        if idx:
            self.polys.pop(idx)
            self.centroid_offsets.pop(idx)
            self.physics.pop(idx)
            self.pixmaps.pop(idx)
            self.poses.pop(idx)
            self.sizes.pop(idx)
        else:
            self.polys.pop()
            self.centroid_offsets.pop()
            self.physics.pop()
            self.pixmaps.pop()
            self.poses.pop()
            self.sizes.pop()      

    def update_position(self,force,obstacles):
        for idx in range(0,len(self.polys)):
            self.physics[idx].gravity()
            self.collision_check(obstacles,idx)

    def collision_check(self,obstacles,idx):
        self.polys[idx].translate(self.physics[idx].velocity[0],0.)
        collision = False

        for obstacle in obstacles:
            if sphere_is_collision(self.polys[idx],obstacle):

                data = copy.deepcopy(self.polys[idx].vertices)
                data = data.astype(np.double)
                data_p = data.ctypes.data_as(self.c_float_p)

                data2 = copy.deepcopy(obstacle.vertices)
                data2 = data2.astype(np.double)
                data_p2 = data2.ctypes.data_as(self.c_float_p)

                # C Function call in python
                res = self.fun.polygon_is_collision(data_p,2,len(self.polys[idx].vertices[0,:]),data_p2,2,len(obstacle.vertices[0,:]))
                if res:
                    collision = True
                    break
        
        if collision:
            self.polys[idx].translate(-1*self.physics[idx].velocity[0],0.)
            self.physics[idx].velocity[0] = 0.
        else:
            t = np.array([self.physics[idx].velocity[0],[0.]])
            self.poses[idx] += t
        
        # Y Collision Check
        self.polys[idx].translate(0.,self.physics[idx].velocity[1])
        collision = False
        for obstacle in obstacles:
            if sphere_is_collision(self.polys[idx],obstacle):
                data = copy.deepcopy(self.polys[idx].vertices)
                data = data.astype(np.double)
                data_p = data.ctypes.data_as(self.c_float_p)

                data2 = copy.deepcopy(obstacle.vertices)
                data2 = data2.astype(np.double)
                data_p2 = data2.ctypes.data_as(self.c_float_p)

                # C Function call in python
                res = self.fun.polygon_is_collision(data_p,2,len(self.polys[idx].vertices[0,:]),data_p2,2,len(obstacle.vertices[0,:]))
                if res:
                    collision = True
                    break

        if collision:
            self.polys[idx].translate(0.,-1*self.physics[idx].velocity[1])
            self.physics[idx].velocity[1] = 0.
        else:
            t = np.array([[0.],self.physics[idx].velocity[1]])
            self.poses[idx] += t

