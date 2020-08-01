#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, math, time, numpy

from Utils import *
from PaintUtils import *
from Environment import *
from Player import *
from WelcomeScreen import *
from GameController import *

class Game(QMainWindow,FilePaths):
    
    fps = 45.0
    game_time = 0.0
    loop_number = 0
    fps_time = time.time()
    fps_log = []

    key_pressed = []
    tod = 'day'
    collision_str = ''
    params = {}

    new_env = False
    next_scene = False
    prev_scene = False
    
    clear_key_list = False
    clear_key_count = 0
    clear_key_limit = 10

    exit_game = False

    load = None # If a game is being loaded, set True

    game_running = False

    def __init__(self,screen):
        super().__init__()
            # Game window dimensions
        self.width = 1800
        self.height = 850

        self.screen_height = screen.size().height()
        self.screen_width = screen.size().width()

        # setting title 
        self.setWindowTitle("Game Title")

        welcome_width = 1200
        welcome_height = 800
        self.setGeometry(math.floor((self.screen_width-welcome_width)/2), math.floor((self.screen_height-welcome_height)/2), welcome_width, welcome_height) 

        # Set main widget as main windows central widget
        self.main_widget = WelcomeScreen()
        self.main_widget.env_params.connect(self.set_params)
        self.main_widget.create.connect(self.start_game)
        self.main_widget.load.connect(self.load_game)
        self.setCentralWidget(self.main_widget)
        self.game_main_window = True

        self.setFocusPolicy(Qt.StrongFocus)

        # Show main window
        self.show()

    def load_game(self,name):
        self.load = True
        self.save_file_name = name + '.json'
        self.player = Player()
        self.player.pause_signal.connect(self.pause_game)
        self.player.collision_signal.connect(self.update_collision_str)
        log(f'Loading game called: {self.save_file_name}')
        self.display_environment()

        # Begin game timer and game loop
        self.game_timer = QTimer()
        self.game_timer.setInterval(math.ceil((1.0/self.fps)*1000.0))
        self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start()

        self.game_running = True

        self.player.info_signal.connect(self.display_info)
        
    def start_game(self,name):
        # Game Elements
        self.player = Player()
        self.player.pause_signal.connect(self.pause_game)
        self.save_file_name = name + '.json'
        self.load = False
        log(f'Creating game called: {self.save_file_name}')
        self.display_environment()

        # Begin game timer and game loop
        self.game_timer = QTimer()
        self.game_timer.setInterval(math.ceil((1.0/self.fps)*1000.0))
        self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start()

        self.game_running = True

        self.player.collision_signal.connect(self.update_collision_str)
        self.player.info_signal.connect(self.display_info)

    def set_params(self,param_dict):
        self.params = param_dict
    
    def display_info(self,info):
        try:
            self.game_menu_options.physics_window.update(info,self.key_pressed,self.collision_str,self.game_running)
        except:
            pass # No physics display exists
    
    def update_player(self):
        obstacles = [self.environment.ground_poly.vertices]
        self.player.update_position(self.key_pressed,self.width,self.height,obstacles)

    def display_environment(self):
        self.game_widget = QWidget()
        self.game_layout = QVBoxLayout()
        self.game_widget.setLayout(self.game_layout)
        self.game_layout.setAlignment(Qt.AlignCenter)

        self.prompt_manager = PromptManager(self.screen_width,self.screen_height)

        self.game_menu_options = GameMenuOptions()
        self.game_layout.addWidget(self.game_menu_options)
        self.game_menu_options.save_scene_signal.connect(self.save_scene_event)
        self.game_menu_options.exit_game_signal.connect(self.end_game)
        self.game_menu_options.pause_game_signal.connect(self.pause_game)
        self.game_menu_options.clear_keys_signal.connect(self.clear_keys)
        self.game_menu_options.dock_widget_signal.connect(self.show_dock_widget)

        self.environment = Environment(self.width,self.height,self.player,self.save_file_name,self.params,load = self.load)
        self.width = self.environment.width
        self.height = self.environment.height
        self.game_layout.addWidget(self.environment)

        self.game_controller = GameController()
        self.game_layout.addWidget(self.game_controller)
        self.game_controller.new_scene_signal.connect(self.new_scene_event)
        self.game_controller.prev_scene_signal.connect(self.prev_scene_event)
        self.game_controller.advance_scene_signal.connect(self.advance_scene_event)
        
        if sys.platform == 'win32':
            self.showMaximized()
        else:
            self.setGeometry(0, 0, self.screen_width, self.screen_height)

        self.game_main_window = False
        self.setCentralWidget(self.game_widget)

    def new_scene_event(self):
        log('New scene called...',color='y')
        self.new_env = True
    def prev_scene_event(self):
        log('Switching to previous scene...')
        self.prev_scene = True
    def advance_scene_event(self):
        log('Advancing to the next scene...')
        self.next_scene = True
    def save_scene_event(self):
        log('Save scene called...')
        self.environment.save_game()

    def clear_keys(self):
        self.key_pressed = []
        self.clear_key_list = True
        log('Called clear_keys...')

    def pause_game(self):
        print('entering pause function')
        if self.game_running == True:
            log('Pausing game...')
            self.game_running = False

        elif self.game_running == False:
            log('Resuming game...')
            self.game_running = True
            self.clear_keys()
        else:
            log('Game running state not recognized...')

        self.display_info('')

    def update_collision_str(self,string):
        self.collision_str = string

    def show_dock_widget(self,dock_widget):
        self.dock = QDockWidget(self) 
        self.dock.setWidget(dock_widget) 
        self.dock.setGeometry(dock_widget.geometry())
        self.dock.setAutoFillBackground(dock_widget.auto_fill_background)
        self.dock.show()

    def end_game(self):
        try:
            self.environment.save_game()
        except:
            log('Failed to save the same on an end game call!',color='r')
        self.close()

        try:
            self.game_menu_options.physics_window.close()
        except:
            pass
        try:
            self.prompt_manager.welcome_prompt.close()
        except:
            pass

    # Qt method
    def keyPressEvent(self, event):
        if self.game_main_window:
            return
        
        ### Move Keys
        val = ''
        if event.key() == Qt.Key_D:
            # self.key_pressed.append('right')
            val = 'right'
        elif event.key() == Qt.Key_A:
            # self.key_pressed.append('left')
            val = 'left'
        elif event.key() == Qt.Key_W:
            # self.key_pressed.append('up')
            val = 'up'
        elif event.key() == Qt.Key_S:
            # self.key_pressed.append('down')
            val = 'down'
        
        ### Game operation keys
        elif event.key() == Qt.Key_N:
            self.new_scene_event()
        elif event.key() == Qt.Key_M:
            log('Advancing to next scene')
            self.next_scene = True
        elif event.key() == Qt.Key_B:
            self.prev_scene_event()
        elif event.key() == Qt.Key_Escape:
            log('Exit game called...',color='y')
            # self.exit_game = True
            self.end_game()

        elif event.key() == Qt.Key_P:
            self.pause_game()
        else:
            log('Key press not recognized...')

        ### Append move key to pressed list
        if not (val == ''):
            self.key_pressed.append(val)

    # Qt method
    def keyReleaseEvent(self, event):
        if self.game_main_window:
            return
        
        try:
            val = ''
            if event.key() == Qt.Key_D:
                val = 'right'
            elif event.key() == Qt.Key_A:
                # self.key_pressed.remove('left')
                val = 'left'
            elif event.key() == Qt.Key_W:
                # self.key_pressed.remove('up')
                val = 'up'
            elif event.key() == Qt.Key_S:
                # self.key_pressed.remove('down')
                val = 'down'
            else:
                log('Key release not recognized...')

            while val in self.key_pressed:
                self.key_pressed.remove(val)
        except:
            log('Key release event failed...',color='y')
        
    def game_loop(self):
        if self.game_running:
            if self.new_env:
                self.environment.new_environment()
                self.new_env = False

            elif self.prev_scene:
                self.environment.previous_scene()
                self.prev_scene = False
            
            elif self.next_scene:
                self.environment.advance_scene()
                self.next_scene = False

            if self.clear_key_list:
                self.key_pressed = []
                self.clear_key_count += 1
                if self.clear_key_count == self.clear_key_limit:
                    self.clear_key_list = False
                    self.clear_key_count = 0
            
            ### Update player pose and redraw environment
            self.update_player()

            ### recreate environment and repaint widget
            self.environment.redraw_scene()
            self.environment.repaint()

            # Update game loop tracking information
            self.loop_number += 1
            self.game_time += self.game_timer.interval() / 1000.0
            self.environment.game_time = self.game_time

        curr_time = time.time()
        self.fps_time = 1./((curr_time - self.fps_time))
        self.fps_log.append(self.fps_time)
        if len(self.fps_log) == 50:
            average_fps = numpy.mean(self.fps_log)
            log(f'Average fps: {average_fps}')
            self.fps_log = []
        
        # Set time information for next loop
        self.fps_time = curr_time

        # self.prompt_manager.check_prompts()