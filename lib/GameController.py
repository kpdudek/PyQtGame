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
    pause_game_signal = pyqtSignal()
    clear_keys_signal = pyqtSignal()
    dock_widget_signal = pyqtSignal(object)

    def __init__(self,dynamic_obstacles):
        super().__init__()

        self.dynamic_obstacles = dynamic_obstacles

        self.button_grid = QGridLayout()
        self.setLayout(self.button_grid)

        self.save_button = ControlButton('Save',fn=self.save_scene)
        self.button_grid.addWidget(self.save_button,0,0)

        self.exit_button = ControlButton('Exit Game',fn=self.exit_game)
        self.button_grid.addWidget(self.exit_button,0,1)

        self.pause_button = ControlButton('Pause',fn=self.pause_game)
        self.button_grid.addWidget(self.pause_button,0,2)

        self.show_controls_button = ControlButton('Controls',fn=self.show_controls)
        self.button_grid.addWidget(self.show_controls_button,0,3)

        self.show_physics_button = ControlButton('Physics',fn=self.show_physics)
        self.button_grid.addWidget(self.show_physics_button,0,4)

        self.obstacle_manager_button = ControlButton('Obstacles',fn=self.show_obstacles)
        self.button_grid.addWidget(self.obstacle_manager_button,0,5)

        self.fps_label = QLabel('...')
        self.fps_label.setFixedSize(100,20)
        self.fps_label.setStyleSheet(f"font:bold 14px")
        self.button_grid.addWidget(self.fps_label,0,6)

    def save_scene(self):
        self.save_scene_signal.emit()
    
    def exit_game(self):
        self.exit_game_signal.emit()

    def pause_game(self):
        self.pause_game_signal.emit()
    
    def show_controls(self):
        self.controls_window = KeyboardShortcuts()
        self.dock_widget_signal.emit(self.controls_window)

    def show_physics(self):
        self.physics_window = PhysicsDisplay()
        self.dock_widget_signal.emit(self.physics_window)

    def show_obstacles(self):
        self.obstacles_window = ObstaclesDisplay(self.dynamic_obstacles)
        self.dock_widget_signal.emit(self.obstacles_window)

class GameController(QWidget,FilePaths,Colors):
    new_scene_signal = pyqtSignal()
    prev_scene_signal = pyqtSignal()
    advance_scene_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.button_grid = QGridLayout()
        self.setLayout(self.button_grid)

        self.go_back_button = ControlButton('Go Back',fn=self.prev_scene)
        self.button_grid.addWidget(self.go_back_button,0,0)

        self.advance_button = ControlButton('Advance',fn=self.advance_scene)
        self.button_grid.addWidget(self.advance_button,0,1)

        self.next_scene_button = ControlButton('End Turn',fn=self.new_scene)
        self.button_grid.addWidget(self.next_scene_button,0,3)

    def new_scene(self):
        self.new_scene_signal.emit()

    def prev_scene(self):
        self.prev_scene_signal.emit()

    def advance_scene(self):
        self.advance_scene_signal.emit()

class PromptManager(QWidget,Colors,FilePaths):
    first_loop = True
    def __init__(self,screen_width,screen_height):
        self.ui_list = ['welcome_prompt.ui']
        self.screen_width = screen_width
        self.screen_height = screen_height

    def check_prompts(self):
        if self.first_loop:
            self.welcome_prompt = Prompt(self.ui_list[0],self.screen_width,self.screen_height)
            self.first_loop = False
