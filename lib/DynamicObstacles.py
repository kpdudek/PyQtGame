#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, math
import numpy as np

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

        self.ball(1000.,200.)
        self.ball(800.,200.)
        self.ball(1200.,200.)


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
        poly.unit_circle(8,math.ceil(size[0]/2.))
        poly.teleport(x_c,y_c)
        self.polys.append(poly)

        centroid_offset = pose - poly.sphere.pose
        self.centroid_offsets.append(centroid_offset)

        physics = Physics(10.,15.)
        self.physics.append(physics)        

    def update_position(self,force,obstacles):
        for idx in range(0,len(self.polys)):
            self.physics[idx].gravity()
            self.collision_check(obstacles,idx)

    def collision_check(self,obstacles,idx):
        self.polys[idx].translate(self.physics[idx].velocity[0],0.)
        collision = False
        for obstacle in obstacles:
            if sphere_is_collision(self.polys[idx],obstacle):
                if polygon_is_collision(self.polys[idx],obstacle):
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
                if polygon_is_collision(self.polys[idx],obstacle):
                    collision = True
                    break

        if collision:
            self.polys[idx].translate(0.,-1*self.physics[idx].velocity[1])
            self.physics[idx].velocity[1] = 0.
        else:
            t = np.array([[0.],self.physics[idx].velocity[1]])
            self.poses[idx] += t

