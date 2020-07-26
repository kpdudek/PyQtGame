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

class Player(QWidget,Colors,FilePaths):
    key_force = 8

    mass = 1
    force = [0,0]
    drag = 2

    velocity = 0
    acceleration = 4

    prev_direction = 0

    info_signal = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.pose = [600,600]
        self.player_pixmap = None

        self.geom = 'player.svg'
        self.set_geometry(self.geom)
        self.prev_geom = self.geom

        self.physics = Physics(12.0)
        self.physics.info_signal.connect(self.send_info)
    
    def send_info(self,info):
        self.info_signal.emit(info)

    def set_geometry(self,img):
        self.player_pixmap = QPixmap(f'{self.user_path}graphics/{img}')
        self.size = [self.player_pixmap.size().width(),self.player_pixmap.size().height()]
        log('Player size: {}'.format(self.size))

        top_left = np.array([[self.pose[0]],[self.pose[1]]],dtype=float)
        top_right = np.array([[self.pose[0]+self.size[0]],[self.pose[1]]],dtype=float)
        bottom_left = np.array([[self.pose[0]],[self.pose[1]+self.size[1]]],dtype=float)
        bottom_right = np.array([[self.pose[0]+self.size[0]],[self.pose[1]+self.size[1]]],dtype=float)
        self.vertices = np.concatenate((top_left,bottom_left,bottom_right,top_right),axis=1)

    def update_position(self,key_press,width,height,obstacles):
        if len(key_press) != 0:
            self.force = [0,0]
            for key in key_press:
                if key == 'right':
                    self.force[0] = self.key_force
                    self.geom = 'player_right.svg'            
                elif key == 'left':
                    self.force[0] = -self.key_force
                    self.geom = 'player_left.svg'
                elif key == 'up':
                    self.force[1] = -20*self.key_force
                elif key == 'down':
                    self.force[1] = self.key_force
                else:
                    log('Player pose update. Key not recognized...',color='r')
        else:
            self.force = [0,0]

        # Setting player velocity to zero within a threshold and updating geometry
        if abs(self.physics.velocity[0]) < .7:
            self.geom = 'player.svg'
        
        ### Updating player image
        if self.geom != self.prev_geom:
            self.set_geometry(self.geom)
        self.prev_geom = self.geom

        
        # Execute turn position move
        pose = [0,0]

        self.physics.accelerate(self.force)
        pose[0] = self.pose[0] + self.physics.velocity[0] 
        pose[1] = self.pose[1] + self.physics.velocity[1] 

        ### Checking bounds of environment
        if pose[0]+self.size[0] > width:
            pose[0] = width-self.size[0]
        elif pose[0] < 0:
            pose[0] = 0
    
        if pose[1] < 0:
            pose[1] = 0
        elif pose[1]+self.size[1] > height:
            pose[1] = height-self.size[1]

        # Check if that pose would be in collision
        top_left = np.array([[pose[0]],[pose[1]]],dtype=float)
        top_right = np.array([[pose[0]+self.size[0]],[pose[1]]],dtype=float)
        bottom_left = np.array([[pose[0]],[pose[1]+self.size[1]]],dtype=float)
        bottom_right = np.array([[pose[0]+self.size[0]],[pose[1]+self.size[1]]],dtype=float)
        vertices = np.concatenate((top_left,bottom_left,bottom_right,top_right),axis=1)

        collision = False
        obs_count = 0
        vertices_transformed = transform('img',vertices,translate=height)
        # vertices_flipped = np.flip(vertices,1)
        for obstacle in obstacles:
            obs_count += 1
            obstacle = transform('img',obstacle,translate=height)
            # obstacles = np.flip(obstacle,1)
            # print(f'Vertices: \n{vertices}\nObstacle {obs_count}: \n{obstacle}')
            # print(f'Calling collision check on:\n{vertices_transformed}\n{obstacle}')
            if polygon_is_collision(obstacle,vertices_transformed,frame='img').any():
                collision = True
                break
        
        print(f'In Collision: {collision}')
        # Only write that position change if it is collision free
        if not collision:
            self.execute_move(pose,vertices)

    def execute_move(self,pose,vertices):
        self.pose = pose
        self.vertices = vertices

    def animate(self):
        pass