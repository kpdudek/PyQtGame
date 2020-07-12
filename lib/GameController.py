#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, pwd, math

from Utils import *
from PaintUtils import *
from Widgets import *


class GameController(QFrame,FilePaths,Colors):
    next_scene_signal = pyqtSignal()
    prev_scene_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Set main widget as main windows central widget
        # self.layout = QStackedLayout()
        # self.setLayout(self.layout)
        # self.layout.setAlignment(Qt.AlignCenter)

        # self.paint
        # renderer = QtSvg.QSvgRenderer(f'{self.user_path}graphics/game_controls.svg')
        # # widget.resize(renderer.defaultSize())
        # painter = QtGui.QPainter(self)
        # # painter.restore()
        # renderer.render(painter)
        # painter.end()

        # self.button_grid_widget = QWidget()
        self.button_grid = QGridLayout()
        self.setLayout(self.button_grid)

        # self.button_grid_widget.setLayout(self.button_grid)
        # self.layout.addWidget(self.button_grid_widget)

        self.go_back_button = QPushButton('Go Back')
        self.go_back_button.clicked.connect(self.prev_scene)
        self.button_grid.addWidget(self.go_back_button,0,0)

        self.next_scene_button = QPushButton('End Turn')
        self.next_scene_button.clicked.connect(self.next_scene)
        self.button_grid.addWidget(self.next_scene_button,0,1)

        # self.main_title = QtSvg.QSvgWidget(f'{self.user_path}graphics/game_controls.svg')
        # self.main_title.setMinimumHeight(150)
        # self.layout.addWidget(self.main_title)
        # self.setStyleSheet("background-image: {}")
        # self.setStyleSheet(f'background-image: {self.user_path}graphics/game_controls.svg')

    def next_scene(self):
        self.next_scene_signal.emit()

    def prev_scene(self):
        self.prev_scene_signal.emit()