#!/usr/bin/env python3

import os, sys, time, math
import numpy as np
import datetime as dt
from threading import Thread
import inspect

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from Utils import *
from PaintUtils import *

class Item(QLabel,Colors,FilePaths):
    # transform = None
    clicked_signal = pyqtSignal(object)
    dragged_signal = pyqtSignal(object)
    released_signal = pyqtSignal(object)
    
    def __init__(self,sprite,r,c,inv_pose):
        super().__init__()
        pose = np.array([[self.geometry().x()],[self.geometry().y()]])
        self.transform = -1.*(pose - inv_pose)

        # self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setFrameShape(QFrame.StyledPanel)
        self.sprite = sprite
        self.index = np.array([[r],[c]])    
        self.mous_pos = None

    def set_pixmap(self):
        self.setPixmap(self.sprite.pixmaps[self.sprite.idx])

    def add_pixmap(self,sprite):
        self.sprite = sprite
        self.set_pixmap()

    def remove_pixmap(self):
        self.sprite = None
        self.clear()
    
    def mousePressEvent(self,e):
        pose = np.array([[e.x()],[e.y()]])
        self.mous_pos = pose + self.transform
        self.clicked_signal.emit(self.index)

    def mouseMoveEvent(self,e):
        pose = np.array([[e.x()],[e.y()]])
        self.mous_pos = pose + self.transform
        self.dragged_signal.emit(self.index)

    def mouseReleaseEvent(self,e):
        self.released_signal.emit(self.index)

class Inventory(QWidget,Colors,FilePaths):
    '''
    Inventory entries are sprites
    '''
    item_clicked = pyqtSignal(object)
    item_dragged = pyqtSignal(object)
    item_released = pyqtSignal()

    def __init__(self,screen_width,screen_height):
        super().__init__()
        self.setWindowTitle('Inventory')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.auto_fill_background = False

        self.layout = QGridLayout()

        self.width = 400
        self.height = 250
        self.geom = QRect(math.floor((screen_width-self.width)/2), math.floor((screen_height-self.height)/2), self.width, self.height)
        self.setGeometry(self.geom) 

        self.pose = np.array([[self.geometry().x()],[self.geometry().y()]])

        r,c = 3,4
        size = r*c
        self.full = False
        self.items = np.empty(size,dtype=object).reshape(r,c)
        self.r_max,self.c_max = self.items.shape
        self.generate_layout()
        self.idx = np.array([[0],[0]])

        self.setLayout(self.layout)

    def generate_layout(self):
        for i in range(0,self.r_max):
            for j in range(0,self.c_max):
                label = Item(None,i,j,self.pose)
                label.setStyleSheet(f"font:bold 14px; color: {self.divider_color}")
                label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                label.clicked_signal.connect(self.inv_click)
                label.dragged_signal.connect(self.inv_drag)
                label.released_signal.connect(self.inv_release)
                self.items[i,j] = label
                self.layout.addWidget(label,i,j)

    def find_open_slot(self):
        for item_array in self.items:
            item = item_array[0]
            if not item.sprite:
                log(f'Found available inventory slot: ({item.index[0]},{item.index[1]})')
                return item.index
        return None

    def is_empty(self):
        for item_array in self.items:
            item = item_array[0]
            if item.sprite:
                log(f'Found taken inventory slot: ({item.index[0]},{item.index[1]})')
                return False
        log('Inventory is empty...')
        return True

    def add_item(self,sprite):
        r,c = self.idx
        if self.items[r,c][0].sprite == None:
            self.items[r,c][0].add_pixmap(sprite)
            
            if (r == self.r_max-1) and (c != self.c_max-1):
                self.idx[0] = 0
                self.idx[1] += 1
            elif (r == self.r_max-1) and (c == self.c_max-1):
                self.idx[0] = 0
                self.idx[1] = 0
            else:
                self.idx[0] += 1
        else:
            idx = self.find_open_slot()

            if idx == None:
                if not self.full:
                    self.full = True
                    log('Inventory filled up!')
                return

            self.items[idx[0],idx[1]][0].add_pixmap(sprite)

            if (r == self.r_max-1) and (c != self.c_max-1):
                self.idx[0] = 0
                self.idx[1] += 1
            elif (r == self.r_max-1) and (c == self.c_max-1):
                self.idx[0] = 0
                self.idx[1] = 0
            else:
                self.idx[0] += 1

    def remove_item(self,item):
        r,c = item.index
        self.idx = item.index.copy()
        self.items[r,c][0].remove_pixmap()
        
        if self.is_empty():
            self.idx = np.array([[0],[0]])
        
    def inv_release(self,index):
        self.item_released.emit()
        self.remove_item(self.items[index[0],index[1]][0])
        self.full = False

    def inv_drag(self,index):
        if self.items[index[0],index[1]][0].sprite:
            # log(f'Clicked: {self.items[index[0],index[1]][0].sprite.name} at index {index[0]},{index[1]}')
            self.mouse_pos = self.items[index[0],index[1]][0].mous_pos
            self.item_dragged.emit(self.mouse_pos)

    def inv_click(self,index):
        # TODO: pass the item itself through this signal instead of its index

        if self.items[index[0],index[1]][0].sprite:
            log(f'Clicked: {self.items[index[0],index[1]][0].sprite.name} at index {index[0]},{index[1]}')

            sprite = self.items[index[0],index[1]][0].sprite

            self.mouse_pos = self.items[index[0],index[1]][0].mous_pos
            sprite.polys[sprite.idx].teleport(self.mouse_pos[0],self.mouse_pos[1])
            sprite.pose = self.mouse_pos + sprite.centroid_offsets[sprite.idx]

            self.item_clicked.emit(sprite)