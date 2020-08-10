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
    key_force = 2.
    sprint_multiplier = 2.5
    boost = 25.
    max_vel = 8.
    mass = 12.

    force = np.array([ [0.] , [0.] ])
    velocity = 0.
    collision_str = np.zeros(2).reshape(2,1)
    mouse_pos = np.zeros(2).reshape(2,1) - 1
    collision_pt = np.zeros(2).reshape(2,1) - 1
    calc_offsets = True
    log_collis = True
    mouse_prev = np.zeros(2).reshape(2,1) - 1

    info_signal = pyqtSignal(object)
    pause_signal = pyqtSignal()
    collision_signal = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.pose = np.array([ [200.] , [200.] ])
        self.player_pixmap = None

        self.geom = 'player.svg'
        self.set_geometry(self.geom)
        self.prev_geom = self.geom

        self.physics = PlayerPhysics(self.mass,self.max_vel)
        self.physics.info_signal.connect(self.send_info)
    
    def send_info(self,info):
        self.info_signal.emit(info)

    def set_geometry(self,img):
        self.player_pixmap = QPixmap(f'{self.user_path}graphics/{img}')
        self.size = [self.player_pixmap.size().width(),self.player_pixmap.size().height()]
        # log('Player graphic: {}, size: {}'.format(img,self.size))

        top_left = np.array([self.pose[0],self.pose[1]],dtype=float)
        bottom_right = np.array([self.pose[0]+self.size[0],self.pose[1]+self.size[1]],dtype=float)
        self.vertices = Polygon(top_left,bottom_right,poly_type='rect').vertices

    def update_position(self,key_press,sprint,mouse_pos,width,height,obstacles):
        if len(key_press) != 0:
            self.force = np.array([ [0.] , [0.] ])

            for key in key_press:
                if key == 'right':
                    self.force[0] = self.key_force
                    self.geom = 'player_right.svg'            
                elif key == 'left':
                    self.force[0] = -self.key_force
                    self.geom = 'player_left.svg'
                
                if sprint:
                    self.force[0] = self.force[0] * self.sprint_multiplier

                # print(self.collision_str)
                if self.collision_str[1] == 1:
                    if key == 'up':
                        self.force[1] = -self.boost*self.key_force
                    elif key == 'down':
                        self.force[1] = self.key_force
        else:
            self.force = np.array([ [0.] , [0.] ])

        if np.sum(mouse_pos) >= 0:
            self.mouse_pos = mouse_pos # Always keep track of the mouse pose for drawing the red marker
            player_vert = transform('img',self.vertices.copy(),translate=height)
            mouse_vert = transform('img',mouse_pos.copy(),translate=height)
            if polygon_is_collision(player_vert,mouse_vert).any():
                if self.log_collis:
                    log('Mouse click collided with player...')
                    self.log_collis = False
                self.collision_pt = mouse_pos
            else:
                if np.sum(self.collision_pt) >= 0:
                    if self.calc_offsets:
                        self.x_offset = -1*(self.collision_pt[0] - self.pose[0])
                        self.y_offset = -1*(self.collision_pt[1] - self.pose[1])
                        self.calc_offsets = False

                    self.pose = np.array([ mouse_pos[0]+self.x_offset , mouse_pos[1]+self.y_offset ])
                else:
                    self.pose = np.array([mouse_pos[0]-self.size[0]/2. , mouse_pos[1]-self.size[1]])

                if np.sum(self.mouse_prev) >= 0:
                    vel_x = (mouse_pos[0] - self.mouse_prev[0])
                    vel_y = (mouse_pos[1] - self.mouse_prev[1])
                    self.physics.velocity = np.array([vel_x,vel_y])
                    self.physics.send_info()
            self.mouse_prev = mouse_pos
            return
        else: # Always keep track of the mouse pose for drawing the red marker
            self.mouse_pos = mouse_pos

        # Setting player velocity to zero within a threshold and updating geometry
        if abs(self.physics.velocity[0]) < .3:
            self.geom = 'player.svg'
        
        ### Updating player image
        if self.geom != self.prev_geom:
            self.set_geometry(self.geom)
        self.prev_geom = self.geom

        self.collision_str = np.zeros(2).reshape(2,1)

        for count,obstacle in enumerate(obstacles):
            obstacle = transform('img',obstacle,translate=height)
            obstacles[count] = obstacle

        self.physics.gravity()
        pose = self.pose.copy()
        self.check_collison(pose,width,height,obstacles)
        
        self.physics.accelerate(self.force)
        pose = self.pose.copy()
        self.check_collison(pose,width,height,obstacles)

        self.collision_signal.emit(self.collision_str)

    def check_collison(self,pose,width,height,obstacles):
        ########### Check X Axis Collision ###########
        pose[0] += self.physics.velocity[0] 

        ### Checking bounds of environment
        if pose[0]+self.size[0] > width:
            pose[0] = width-self.size[0]
        elif pose[0] < 0:
            pose[0] = 0

        # Check if that pose would be in collision
        top_left = np.array([pose[0],pose[1]],dtype=float)
        bottom_right = np.array([pose[0]+self.size[0],pose[1]+self.size[1]],dtype=float)
        vertices = Polygon(top_left,bottom_right,poly_type='rect').vertices

        collision = False
        obs_count = 0
        vertices_transformed = transform('img',vertices.copy(),translate=height)
        for obstacle in obstacles.copy():
            obs_count += 1
            if multithreaded_polygon_is_collision(obstacle,vertices_transformed).any():
                collision = True
                break
            if multithreaded_polygon_is_collision(vertices_transformed,obstacle).any():
                collision = True
                break
        # Only write that position change if it is collision free
        if not collision:
            self.execute_move(pose,vertices.copy())
        else:
            pose = self.pose.copy()
            self.collision_str[0] = 1
            self.physics.velocity[0] = 0.

        ########### Check Y Axis Collision ###########
        pose[1] += self.physics.velocity[1] 
    
        if pose[1] < 0:
            pose[1] = 0
        elif pose[1]+self.size[1] > height:
            pose[1] = height-self.size[1]

        # Check if that pose would be in collision
        top_left = np.array([pose[0],pose[1]],dtype=float)
        bottom_right = np.array([pose[0]+self.size[0],pose[1]+self.size[1]],dtype=float)
        vertices = Polygon(top_left,bottom_right,poly_type='rect').vertices

        collision = False
        obs_count = 0
        vertices_transformed = transform('img',vertices.copy(),translate=height)
        for obstacle in obstacles.copy():
            obs_count += 1
            if multithreaded_polygon_is_collision(obstacle,vertices_transformed).any() == True:
                collision = True
                break
            if multithreaded_polygon_is_collision(vertices_transformed,obstacle).any() == True:
                collision = True
                break
        # Only write that position change if it is collision free
        if not collision:
            self.execute_move(pose,vertices.copy())
        else:
            pose[1] -= self.physics.velocity[1]
            self.collision_str[1] = 1
            self.physics.velocity[1] = 0.

    def execute_move(self,pose,vertices):
        self.pose = pose
        self.vertices = vertices

    def animate(self):
        pass
