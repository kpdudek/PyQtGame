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
        self.physics.append(physics)        

    def update_position(self,force,obstacles):
        for idx in range(0,len(self.polys)):
            self.physics[idx].gravity()
            self.collision_check(obstacles,idx)

    def collision_check(self,obstacles,idx):
        self.polys[idx].translate(self.physics[idx].velocity[0],0.)
        collision = False
        for obstacle in obstacles:
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
            if polygon_is_collision(self.polys[idx],obstacle):
                collision = True
                break

        if collision:
            self.polys[idx].translate(0.,-1*self.physics[idx].velocity[1])
            self.physics[idx].velocity[1] = 0.
        else:
            t = np.array([[0.],self.physics[idx].velocity[1]])
            self.poses[idx] += t

    # def check_collison(self,pose,width,height,obstacles,idx):
    #     ########### Check X Axis Collision ###########
    #     pose[0] += self.physics[idx].velocity[0] 

    #     ### Checking bounds of environment
    #     if pose[0]+self.sizes[idx][0] > width:
    #         pose[0] = width-self.sizes[idx][0]
    #     elif pose[0] < 0:
    #         pose[0] = 0

    #     # Check if that pose would be in collision
    #     top_left = np.array([pose[0],pose[1]],dtype=float)
    #     bottom_right = np.array([pose[0]+self.sizes[idx][0],pose[1]+self.sizes[idx][1]],dtype=float)
    #     vertices = Polygon(top_left,bottom_right,poly_type='rect').vertices

    #     collision = False
    #     obs_count = 0
    #     vertices_transformed = transform('img',vertices.copy(),translate=height)
    #     for obstacle in obstacles.copy():
    #         obs_count += 1
    #         # if polygon_is_collision(obstacle,vertices_transformed).any():
    #         #     collision = True
    #         #     break
    #         if polygon_is_collision(vertices_transformed,obstacle).any():
    #             collision = True
    #             break
    #     # Only write that position change if it is collision free
    #     if not collision:
    #         self.execute_move(pose,vertices.copy(),idx)
    #     else:
    #         pose = self.poses[idx].copy()
    #         self.physics[idx].velocity[0] = 0.

    #     ########### Check Y Axis Collision ###########
    #     pose[1] += self.physics[idx].velocity[1] 
    
    #     if pose[1] < 0:
    #         pose[1] = 0
    #     elif pose[1]+self.sizes[idx][1] > height:
    #         pose[1] = height-self.sizes[idx][1]

    #     # Check if that pose would be in collision
    #     top_left = np.array([pose[0],pose[1]],dtype=float)
    #     bottom_right = np.array([pose[0]+self.sizes[idx][0],pose[1]+self.sizes[idx][1]],dtype=float)
    #     vertices = Polygon(top_left,bottom_right,poly_type='rect').vertices

    #     collision = False
    #     obs_count = 0
    #     vertices_transformed = transform('img',vertices.copy(),translate=height)
    #     for obstacle in obstacles.copy():
    #         obs_count += 1
    #         # if polygon_is_collision(obstacle,vertices_transformed).any() == True:
    #         #     collision = True
    #         #     break
    #         # print(f"Vertices:\n{vertices_transformed}\nObstacle{obs_count}:\n{obstacle}")
    #         if polygon_is_collision(vertices_transformed,obstacle).any() == True:
    #             collision = True
    #             # print('Collision!')
    #             break
    #     # Only write that position change if it is collision free
    #     if not collision:
    #         self.execute_move(pose,vertices.copy(),idx)
    #     else:
    #         pose[1] -= self.physics[idx].velocity[1]
    #         self.physics[idx].velocity[1] = 0.

    # def execute_move(self,pose,vertices,idx):
    #     self.poses[idx] = pose
    #     self.vertices[idx] = vertices

