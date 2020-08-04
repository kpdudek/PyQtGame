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

class Inventory(QWidget,Colors,FilePaths):

    def __init__(self,screen_width,screen_height):
        super().__init__()
        self.setWindowTitle('Inventory')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.auto_fill_background = True

        self.layout = QGridLayout()
        # self.layout.setAlignment(Qt.AlignCenter)

        width = 800
        height = 600
        self.geom = QRect(math.floor((screen_width-width)/2), math.floor((screen_height-height)/2), width, height)
        self.setGeometry(self.geom) 

        self.grid_entries = [[0,0]]

        self.controls_label = QLabel('Inventory')
        self.controls_label.setStyleSheet(f"font:bold italic 24px")
        self.controls_label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.layout.addWidget(self.controls_label,self.grid_entries[0][0],self.grid_entries[0][1])

        self.setLayout(self.layout)