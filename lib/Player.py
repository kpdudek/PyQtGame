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
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.width = width
        self.height = height

        self.pose = np.array([ [200.] , [200.] ]) # pose for pixmap
        self.player_pixmap = None

        self.geom = 'Player.png'
        self.set_geometry(self.geom)
        self.prev_geom = self.geom

        self.physics = PlayerPhysics(self.mass,self.max_vel)
        
        self.poly = Polygon()
        bot_right = np.array([self.pose[0]+self.size[0],self.pose[1]+self.size[1]])
        self.poly.rectangle(self.pose,bot_right)

        self.centroid_offset = self.pose - self.poly.sphere.pose 

        self.physics.info_signal.connect(self.send_info)

        # C library for collision checking
        self.c_float_p = ctypes.POINTER(ctypes.c_double)
        self.fun = ctypes.CDLL(f'{self.user_path}lib/cc_lib.so') # Or full path to file           
        self.fun.polygon_is_collision.argtypes = [self.c_float_p,ctypes.c_int,ctypes.c_int,self.c_float_p,ctypes.c_int,ctypes.c_int] 

    
    def send_info(self,info):
        self.info_signal.emit(info)

    def set_geometry(self,img):
        self.player_pixmap = QPixmap(f'{self.user_path}graphics/{img}')
        self.size = [self.player_pixmap.size().width(),self.player_pixmap.size().height()]

    def update_position(self,key_press,sprint,mouse_pos,obstacles):
        if len(key_press) != 0:
            self.force = np.array([ [0.] , [0.] ])

            for key in key_press:
                if key == 'right':
                    self.force[0] = self.key_force
                    self.geom = 'Player.png'          
                elif key == 'left':
                    self.force[0] = -self.key_force
                    self.geom = 'Player.png'
                
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
            player_vert = transform('img',copy.deepcopy(self.poly.vertices),translate=self.height)
            mouse_vert = transform('img',mouse_pos.copy(),translate=self.height)

            self.poly.teleport(mouse_pos[0],mouse_pos[1])
            self.pose = mouse_pos + self.centroid_offset

            if np.sum(self.mouse_prev) >= 0:
                mouse_vel = mouse_pos - self.mouse_prev
                self.physics.velocity = mouse_vel
            self.mouse_prev = mouse_pos
            self.physics.send_info()
            return
        else: # Always keep track of the mouse pose for drawing the red marker
            self.mouse_pos = mouse_pos

        # Setting player velocity to zero within a threshold and updating geometry
        if abs(self.physics.velocity[0]) < .3:
            self.geom = 'Player.png'
        
        ### Updating player image
        if self.geom != self.prev_geom:
            self.set_geometry(self.geom)
        self.prev_geom = self.geom

        self.collision_str = np.zeros(2).reshape(2,1)

        self.physics.gravity()
        self.collision_check(obstacles)

        self.physics.accelerate(self.force)
        self.collision_check(obstacles)

        self.collision_signal.emit(self.collision_str)

        self.physics.send_info()

    def collision_check(self,obstacles):
        # X Collision Check
        self.poly.translate(self.physics.velocity[0],0.)
        collision = False

        for obstacle in obstacles:
            if sphere_is_collision(self.poly,obstacle):
                data = copy.deepcopy(self.poly.vertices)
                data = data.astype(np.double)
                data_p = data.ctypes.data_as(self.c_float_p)

                data2 = copy.deepcopy(obstacle.vertices)
                data2 = data2.astype(np.double)
                data_p2 = data2.ctypes.data_as(self.c_float_p)

                # C Function call in python
                res = self.fun.polygon_is_collision(data_p,2,len(self.poly.vertices[0,:]),data_p2,2,len(obstacle.vertices[0,:]))
                if res:
                    collision = True
                    break
    
        if collision:
            self.poly.translate(-1*self.physics.velocity[0],0.)
            self.collision_str[0] = 1
            self.physics.velocity[0] = 0.
        else:
            t = np.array([self.physics.velocity[0],[0.]])
            self.pose += t
        
        # Y Collision Check
        self.poly.translate(0.,self.physics.velocity[1])
        collision = False
        for obstacle in obstacles:
            if sphere_is_collision(self.poly,obstacle):
                data = copy.deepcopy(self.poly.vertices)
                data = data.astype(np.double)
                data_p = data.ctypes.data_as(self.c_float_p)

                data2 = copy.deepcopy(obstacle.vertices)
                data2 = data2.astype(np.double)
                data_p2 = data2.ctypes.data_as(self.c_float_p)

                # # C Function call in python
                res = self.fun.polygon_is_collision(data_p,2,len(self.poly.vertices[0,:]),data_p2,2,len(obstacle.vertices[0,:]))
                if res:
                    collision = True
                    break

        if collision:
            self.poly.translate(0.,-1*self.physics.velocity[1])
            self.collision_str[1] = 1
            self.physics.velocity[1] = 0.
        else:
            t = np.array([[0.],self.physics.velocity[1]])
            self.pose += t
