#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, math

from Utils import *
from PaintUtils import *
from Widgets import *

class GameMenuOptions(QWidget,FilePaths,Colors):
    save_scene_signal = pyqtSignal()
    exit_game_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.button_grid = QGridLayout()
        self.setLayout(self.button_grid)

        self.save_button = ControlButton('Save',fn=self.save_scene)
        self.button_grid.addWidget(self.save_button,0,0)

        self.exit_button = ControlButton('Exit Game',fn=self.exit_game)
        self.button_grid.addWidget(self.exit_button,0,1)

        self.show_controls_button = ControlButton('Controls',fn=self.show_controls)
        self.button_grid.addWidget(self.show_controls_button,0,2)

        self.show_physics_button = ControlButton('Physics',fn=self.show_physics)
        self.button_grid.addWidget(self.show_physics_button,0,3)

    def save_scene(self):
        self.save_scene_signal.emit()
    
    def exit_game(self):
        self.exit_game_signal.emit()
    
    def show_controls(self):
        self.controls_window = KeyboardShortcuts()

    def show_physics(self):
        self.physics_window = PhysicsDisplay()

class GameController(QWidget,FilePaths,Colors):
    new_scene_signal = pyqtSignal()
    prev_scene_signal = pyqtSignal()
    advance_scene_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        # self.button_grid_widget = QWidget()
        self.button_grid = QGridLayout()
        self.setLayout(self.button_grid)

        self.go_back_button = ControlButton('Go Back',fn=self.prev_scene)
        self.button_grid.addWidget(self.go_back_button,0,0)

        self.advance_button = ControlButton('Advance',fn=self.advance_scene)
        self.button_grid.addWidget(self.advance_button,1,0)

        self.next_scene_button = ControlButton('End Turn',fn=self.new_scene)
        self.button_grid.addWidget(self.next_scene_button,0,1)

    def new_scene(self):
        self.new_scene_signal.emit()

    def prev_scene(self):
        self.prev_scene_signal.emit()

    def advance_scene(self):
        self.advance_scene_signal.emit()
