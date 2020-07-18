#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, math, json

from Utils import *
from PaintUtils import *

class Environment(QWidget,Colors,FilePaths):
    time_of_day = None
    game_time = 0.0

    generate_env = True

    env_snapshot = {}
    game_snapshot = {}

    env_idx = 0
    env_create_count = 0

    def __init__(self,width,height,player,save_file, load = True, time_of_day = None):
        super().__init__()
        self.load = load
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.player = player
        self.save_file = save_file

        self.num_prefix = 3
        if self.load:
            self.load_game()
            self.width = self.game_snapshot['width']
            self.height = self.game_snapshot['height']
            self.os = self.game_snapshot['os']
            self.generate_env = False
            self.env_idx = len(self.game_snapshot)-1 - self.num_prefix
            self.env_snapshot = self.game_snapshot[str(self.env_idx)]
        else:
            self.width = width
            self.height = height
            self.os = sys.platform

            self.game_snapshot.update({'width':self.width})
            self.game_snapshot.update({'height':self.height})
            self.game_snapshot.update({'os':self.os})

            self.time_of_day = time_of_day

        self.main_frame = QLabel()
        self.layout.addWidget(self.main_frame)

        self.canvas = QPixmap(self.width,self.height)
        self.main_frame.setPixmap(self.canvas)

        # Display environment components
        self.set_sky()
        self.draw_ground()
        self.draw_player()

        if not self.load:
            log('Saving new game for the first time...')
            self.game_snapshot.update({str(self.env_create_count):self.env_snapshot})
            self.save_game()
            self.env_create_count += 1
        else:
            self.env_create_count = len(self.game_snapshot) - self.num_prefix

        self.generate_env = False

        log('Environment initialized...')
        log(f'Create count: {self.env_create_count} | env idx: {self.env_idx}')

    def load_game(self):
        with open(f'{self.user_path}saves/{self.save_file}') as fp:
            game = json.load(fp)
        self.game_snapshot = game

        log(f'Environment keys: {self.game_snapshot.keys()}')
    
    def save_game(self):
        try:
            fp = open(f'{self.user_path}saves/{self.save_file}','w')
            json.dump(self.game_snapshot,fp)
            fp.close()
            log('Save game returned sucessfully!',color='g')
        except:
            log('Save game failed!',color='r')

    def set_sky(self):
        painter = QtGui.QPainter(self.main_frame.pixmap())

        if self.generate_env:
            self.env_snapshot.update({'time_of_day':self.time_of_day})
        else:
            self.time_of_day = self.env_snapshot['time_of_day']
        
        if self.time_of_day == 'day':
            pen = QtGui.QPen()
            pen.setWidth(3)
            pen.setColor(QtGui.QColor(self.sky_blue['hex']))
            painter.setPen(pen)

            brush = QtGui.QBrush()
            brush.setColor(QtGui.QColor(self.sky_blue['hex']))
            brush.setStyle(Qt.SolidPattern)
            painter.setBrush(brush)

            painter.drawRect(QtCore.QRect(0, 0, self.width, self.height))
            painter.end()
            
            self.draw_sun()
            self.draw_clouds()

        elif self.time_of_day == 'night':
            pen = QtGui.QPen()
            pen.setWidth(3)
            pen.setColor(QtGui.QColor(self.midnight_blue['hex']))
            painter.setPen(pen)

            brush = QtGui.QBrush()
            brush.setColor(QtGui.QColor(self.midnight_blue['hex']))
            brush.setStyle(Qt.SolidPattern)
            painter.setBrush(brush)

            painter.drawRect(QtCore.QRect(0, 0, self.width, self.height))
            painter.end()

            self.draw_stars()
            self.draw_moon()

    def draw_clouds(self):
        painter = QtGui.QPainter(self.main_frame.pixmap())

        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor(self.white['hex']))
        painter.setPen(pen)

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.white['hex']))
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        # Generate random clouds
        if self.generate_env:
            clouds = []

            self.num_clouds = 10
    
            self.cloud_x_range = [20,self.width-20]
            self.cloud_y_range = [0,math.ceil(self.height/2.)]

            self.env_snapshot.update({'num_clouds':self.num_clouds})

        else:
            self.num_clouds = self.env_snapshot['num_clouds']
        

        ### Draw clouds using number of clouds, and range to generate random pose if generating new environment
        for cloud_idx in range(0,self.num_clouds):
            
            if self.generate_env:
                new_cloud = {}
                sub_clouds = []
                cloud_size = [10,20]

                x = random.randint(self.cloud_x_range[0],self.cloud_x_range[1])
                y = random.randint(self.cloud_y_range[0],self.cloud_y_range[1])
                new_cloud.update({'origin':[x,y]})

                num_sub_clouds = random.randint(5,15)
                new_cloud.update({'num_sub_clouds':num_sub_clouds})

            else:
                x,y = self.env_snapshot['clouds'][cloud_idx]['origin']
                num_sub_clouds = self.env_snapshot['clouds'][cloud_idx]['num_sub_clouds']

            for sub_cloud_idx in range(0,num_sub_clouds):
                
                if self.generate_env:
                    sub_cloud = {}

                    rad_x = random.randint(cloud_size[0],cloud_size[1])
                    rad_y = random.randint(cloud_size[0],cloud_size[1])
                    sub_cloud.update({'radii':[rad_x,rad_y]})

                    offset = 20
                    x_offset = random.randint(-offset,offset)
                    y_offset = random.randint(-offset,offset)
                    sub_cloud.update({'offsets':[x_offset,y_offset]})

                    sub_clouds.append(sub_cloud)
                else:
                    rad_x,rad_y = self.env_snapshot['clouds'][cloud_idx]['sub_clouds'][sub_cloud_idx]['radii'] 
                    x_offset,y_offset = self.env_snapshot['clouds'][cloud_idx]['sub_clouds'][sub_cloud_idx]['offsets']
                
                painter.drawEllipse(QPoint(x+x_offset,y+y_offset),rad_x,rad_y)
            
            if self.generate_env:      
                new_cloud.update({'sub_clouds':sub_clouds})
                clouds.append(new_cloud)

        if self.generate_env:
            self.env_snapshot.update({'clouds':clouds})
        painter.end()
    
    def draw_stars(self):
        painter = QtGui.QPainter(self.main_frame.pixmap())

        self.star_pen_width = 5
        pen = QtGui.QPen(self.star_pen_width)
        pen.setWidth(self.star_pen_width)
        pen.setColor(QtGui.QColor(self.star_gold['hex']))
        painter.setPen(pen)

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.star_gold['hex']))
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        if self.generate_env:
            stars = []

            self.num_stars = 200 

            # Generate random stars
            self.star_x_range = [0,self.width-0]
            self.star_y_range = [0,math.ceil(self.height/2.)]   

            self.env_snapshot.update({'num_stars':self.num_stars})
        else:
            self.num_stars = self.env_snapshot['num_stars']         
        
        for star_idx in range(0,self.num_stars):
            if self.generate_env:
                new_star = {}

                self.star_pen_width = random.randint(2,7)
                pen.setWidth(self.star_pen_width)
                painter.setPen(pen)

                x = random.randint(self.star_x_range[0],self.star_x_range[1])
                y = random.randint(self.star_y_range[0],self.star_y_range[1])
                new_star.update({'origin':[x,y]})
                new_star.update({'radius':self.star_pen_width})

                stars.append(new_star)
            else:
                x,y = self.env_snapshot['stars'][star_idx]['origin']
                self.star_pen_width = self.env_snapshot['stars'][star_idx]['radius']
                pen.setWidth(self.star_pen_width)
                painter.setPen(pen)

            painter.drawPoint(x,y)
        
        painter.end()

        if self.generate_env:
            self.env_snapshot.update({'stars':stars})

    def draw_ground(self):
        painter = QtGui.QPainter(self.main_frame.pixmap())

        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor(self.brown['hex']))
        painter.setPen(pen)

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.brown['hex']))
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        if self.generate_env:
            origin = [0,self.height-50]
            size = [self.width,50]
            ground = {'origin':origin,'size':size}
        else:
            origin = self.env_snapshot['ground']['origin']
            size = self.env_snapshot['ground']['size']
    
        # Generate ground
        p = QPolygonF()
        # for corner_idx in range(0,4):
        p.append(QPointF(origin[0],origin[1]))
        p.append(QPointF(origin[0]+size[0],origin[1]))
        p.append(QPointF(origin[0]+size[0],origin[1]+size[1]))
        p.append(QPointF(origin[0],origin[1]+size[1]))
        # painter.drawRect(QtCore.QRect(origin[0], origin[1], origin[0]+size[0], origin[1]+size[1]))
        painter.drawPolygon(p)
        painter.end()

        if self.generate_env:
            self.env_snapshot.update({'ground':ground})

    def draw_sun(self):
        painter = QtGui.QPainter(self.main_frame.pixmap())

        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor(self.star_gold['hex']))
        painter.setPen(pen)

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.star_gold['hex']))
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        if self.generate_env:
            sun = {}
            origin = [35,35]
            radii = [50,50]

            sun.update({'origin':origin,'radii':radii})
        else:
            origin = self.env_snapshot['sun']['origin']
            radii = self.env_snapshot['sun']['radii']
        
        # Generate sun
        painter.drawEllipse(QPoint(origin[0],origin[1]),radii[0],radii[1])
        painter.end()

        if self.generate_env:
            self.env_snapshot.update({'sun':sun})
    
    def draw_moon(self):
        painter = QtGui.QPainter(self.main_frame.pixmap())

        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor(self.white['hex']))
        painter.setPen(pen)

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.white['hex']))
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        if self.generate_env:
            moon = {}
            origin = [35,35]
            radii = [50,50]

            moon.update({'origin':origin,'radii':radii})
        else:
            origin = self.env_snapshot['moon']['origin']
            radii = self.env_snapshot['moon']['radii']
        
        # Generate sun
        painter.drawEllipse(QPoint(origin[0],origin[1]),radii[0],radii[1])
        painter.end()

        if self.generate_env:
            self.env_snapshot.update({'moon':moon})

    def draw_player(self):
        painter = QtGui.QPainter(self.main_frame.pixmap())
        
        pose = QPoint(self.player.pose[0],self.player.pose[1])
        painter.drawPixmap(pose,self.player.player_pixmap)
        
        painter.end()

    def redraw_scene(self):
        self.set_sky()
        self.draw_ground()
        self.draw_player()
            
    def update_player(self):
        self.canvas = QPixmap(self.width,self.height)
        self.main_frame.setPixmap(self.canvas)

        self.redraw_scene()

    def new_environment(self):
        '''
        New environment expects the current environment to be saved already.
        Additionally, the environment create count should be for the new entry
        '''
        try:
            self.game_snapshot[str(self.env_create_count)]
            log(f'Environment already exists with idx: {self.env_create_count}')
            return
        except:
            pass

        self.env_snapshot = {}

        if self.time_of_day == 'day':
            self.time_of_day = 'night'
        else:
            self.time_of_day = 'day'

        self.generate_env = True
        self.redraw_scene()
        self.generate_env = False
        self.env_idx = self.env_create_count

        self.game_snapshot.update({str(self.env_create_count):self.env_snapshot})
        self.save_game()
        self.env_create_count += 1

        log(f'New scene created. env_create_count: {self.env_create_count} | env_idx: {self.env_idx}')

    def advance_scene(self):
        self.env_idx += 1
        if self.env_idx > (len(self.game_snapshot) -1 - self.num_prefix):
            log('Reached end of environments...')
            self.env_idx -= 1
            return
        
        self.env_snapshot = self.game_snapshot[str(self.env_idx)]
        log(f'Set environment index: {self.env_idx}')
        self.redraw_scene()

    def previous_scene(self):
        self.env_idx -= 1
        if self.env_idx < 0:
            log('Reached beginning of environments...')
            self.env_idx = 0
            return
        
        self.env_snapshot = self.game_snapshot[str(self.env_idx)]
        log(f'Set environment index: {self.env_idx}')
        self.redraw_scene()

