#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, math, time
from multiprocessing import Process
import numpy as np
import copy

from Utils import *
from PaintUtils import *
from Environment import *
from Player import *
from WelcomeScreen import *
from GameController import *
from Inventory import *
from DynamicObstacles import *
from Widgets import *

class Game(QMainWindow,FilePaths,ElementColors):
    fps_calc = []
    game_time = 0.0
    loop_number = 0
    fps_time = time.time()
    prev_fps_time = time.time()
    fps_log = []
    fps_throttle = []

    key_pressed = []
    sprint = False
    mouse_pos = np.zeros(2).reshape(2,1) - 1
    tod = 'day'
    collision_str = None
    params = {}

    inv_dock_hide = None
    new_env = False
    next_scene = False
    prev_scene = False
    
    clear_key_list = False
    clear_key_count = 0
    clear_key_limit = 10

    exit_game = False
    load = None # If a game is being loaded, set True
    game_running = False
    run_once = True

    def __init__(self,screen,fps=45.0):
        super().__init__()
        self.fps = fps

        self.screen_height = screen.size().height()
        self.screen_width = screen.size().width()

        self.width = self.screen_width
        self.height = self.screen_height

        # setting title 
        self.setWindowFlag(Qt.FramelessWindowHint)

        welcome_width = 800
        welcome_height = 600
        self.setGeometry(math.floor((self.screen_width-welcome_width)/2), math.floor((self.screen_height-welcome_height)/2), welcome_width, welcome_height) 

        # Set main widget as main windows central widget
        self.main_widget = WelcomeScreen()
        self.main_widget.env_params.connect(self.set_params)
        self.main_widget.create.connect(self.start_game)
        self.main_widget.load.connect(self.load_game)
        self.setCentralWidget(self.main_widget)
        self.game_main_window = True

        self.prompt_manager = PromptManager(self.screen_width,self.screen_height)

        self.inventory = Inventory(self.screen_width,self.screen_height)
        self.inventory.item_released.connect(self.return_from_inventory)
        self.inventory.item_clicked.connect(self.store_selected_item)
        self.inventory.item_dragged.connect(self.update_inventory_selection)

        self.dynamic_obstacles = DynamicObstacles(self.width,self.height)

        self.obs_display = ObstaclesDisplay(self.dynamic_obstacles)
        self.physics_window = PhysicsDisplay()
        
        self.player = Player(self.width,self.height,self.dynamic_obstacles,self.inventory)
        self.player.collision_signal.connect(self.update_collision_str)
        self.player.info_signal.connect(self.display_info)

        self.dynamic_obstacles.player = self.player

        self.setFocusPolicy(Qt.StrongFocus)

        # Show main window
        self.show()

    def load_game(self,name):
        self.load = True
        self.save_file_name = name + '.json'
        log(f'Loading game called: {self.save_file_name}')
        self.display_environment()

        # Begin game timer and game loop
        self.game_timer = QTimer()
        self.game_timer.setInterval(math.ceil((1.0/self.fps)*1000.0))
        self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start()

        self.game_running = True

    def start_game(self,name):
        # Game Elements
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

    def set_params(self,param_dict):
        self.params = param_dict
    
    def display_info(self,info):
        try:
            self.physics_window.update(info,self.key_pressed,self.collision_str,self.game_running,self.player.sprite.pose,self.avgfps,self.throtfps)
        except:
            pass # No physics display exists
    
    def update_dynamics(self):
        player_obstacles = [self.environment.ground_poly,self.environment.frame_poly]
        for sprite in self.dynamic_obstacles.sprites:
            player_obstacles.append(sprite)#.polys[sprite.idx])
        while None in player_obstacles:
            player_obstacles.remove(None)
        
        mark_to_remove = self.player.update_position(self.key_pressed,self.sprint,self.mouse_pos.copy(),player_obstacles)

        if mark_to_remove:
            for sprite in mark_to_remove:
                self.inventory.add_item(sprite)
                if not self.inventory.full:
                    self.dynamic_obstacles.sprites.remove(sprite)

        # force = .25
        obstacles = [self.environment.ground_poly,self.environment.frame_poly,self.player.sprite.polys[self.player.sprite.idx]]
        self.dynamic_obstacles.update_position(obstacles)

    def store_selected_item(self,sprite):
        try:
            self.dynamic_obstacles.sprites.append(sprite)
            self.dynamic_obstacles.num_sprites += 1
            self.dyn_obs_idx = len(self.dynamic_obstacles.sprites)-1
            self.dynamic_obstacles.sprites[-1].skip_physics = True
            # self.item_stored = True
        except:
            # self.item_stored = False
            log(f'Failed to store item {sprite}')

    def update_inventory_selection(self,pose):
        try:
            sprite = self.dynamic_obstacles.sprites[self.dyn_obs_idx]
            sprite.polys[sprite.idx].teleport(pose[0],pose[1])
            sprite.pose = (pose + sprite.centroid_offsets[sprite.idx])#*(np.array([[1.],[-1.]]))
        except:
            log(f'Update call failed with index {self.dyn_obs_idx}',color='r')
            self.dyn_obs_idx = len(self.dynamic_obstacles.sprites)-1
    
    def return_from_inventory(self):
        try:
            self.dyn_obs_idx = None
            self.dynamic_obstacles.sprites[-1].skip_physics = False
        except:
            log(f'Failed to return item!',color='r')
    
    def display_environment(self):
        self.game_widget = QWidget()
        self.game_layout = QVBoxLayout()

        self.game_layout.setContentsMargins(0,0,0,0)
        self.game_widget.setContentsMargins(0,0,0,0)
        
        self.game_widget.setLayout(self.game_layout)
        self.game_layout.setAlignment(Qt.AlignCenter)

        self.game_layout.addStretch()

        self.environment = Environment(self.width,self.height,self.player,self.dynamic_obstacles,self.save_file_name,self.params,load = self.load)
        self.width = self.environment.width
        self.height = self.environment.height
        self.game_layout.addWidget(self.environment)

        self.game_layout.addStretch()

        self.game_main_window = False
        self.setCentralWidget(self.environment)
        self.setContentsMargins(0,0,0,0)

        if sys.platform == 'win32':
            self.showMaximized()
        else:
            self.setGeometry(0, 0, self.screen_width, self.screen_height)

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

    def display_inventory(self):
        if self.inv_dock_hide:
            self.inv_dock.hide()
            self.inv_dock.setGeometry(self.inventory.geom)
            self.inv_dock_hide = False
        else:
            self.inv_dock = QDockWidget(self) 
            self.inv_dock.setWidget(self.inventory) 
            self.inv_dock.setGeometry(self.inventory.geom)
            self.inv_dock.setAutoFillBackground(self.inventory.auto_fill_background)
            self.inv_dock.show()
            self.inv_dock_hide = True

    def show_obstacle_dock(self,dock_widget):
        self.obstacle_dock = QDockWidget(self) 
        self.obstacle_dock.setWidget(dock_widget) 
        self.obstacle_dock.setGeometry(dock_widget.geometry())
        self.obstacle_dock.setAutoFillBackground(dock_widget.auto_fill_background)
        self.obstacle_dock.show()

    def show_physics_dock(self,dock_widget):
        self.physics_dock = QDockWidget(self) 
        self.physics_dock.setWidget(dock_widget) 
        self.physics_dock.setGeometry(dock_widget.geometry())
        self.physics_dock.setAutoFillBackground(dock_widget.auto_fill_background)
        self.physics_dock.show()

    def end_game(self):
        try:
            self.environment.save_game()
        except:
            if not self.game_main_window:
                log('Failed to save the same on an end game call!',color='r')
        self.close()
    
    # Qt method
    def mousePressEvent(self,e):
        if self.game_main_window:
            return
        try:
            canvas_x = self.environment.geometry().x()+self.environment.main_frame.geometry().x()
            canvas_y = self.environment.geometry().y()+self.environment.main_frame.geometry().y()

            mouse_x = e.x() - canvas_x
            mouse_y = e.y() - canvas_y

            self.mouse_pos = np.array([[float(mouse_x)],[float(mouse_y)]])
            log(f'<Mouse Press> X: {mouse_x} Y: {mouse_y}')
        except:
            log('Could not convert mouse press into canvas coordinate...',color='y')
    
    def mouseMoveEvent(self,e):
        if self.game_main_window:
            return
        try:
            canvas_x = self.environment.geometry().x()+self.environment.main_frame.geometry().x()
            canvas_y = self.environment.geometry().y()+self.environment.main_frame.geometry().y()

            mouse_x = e.x() - canvas_x
            mouse_y = e.y() - canvas_y

            self.mouse_pos = np.array([[float(mouse_x)],[float(mouse_y)]])
        except:
            log('Could not convert mouse press into canvas coordinate...',color='y')

    def mouseReleaseEvent(self,e):
        if self.game_main_window:
            return
        try:
            self.mouse_pos = np.zeros(2).reshape(2,1) - 1
            self.player.collision_pt = np.zeros(2).reshape(2,1) - 1
            self.player.calc_offsets = True
            self.mouse_prev = np.zeros(2).reshape(2,1) - 1
            self.player.log_collis = True
        except:
            log('Could not complete mouse release operations...')
    
    # Qt method
    def keyPressEvent(self, event):
        if self.game_main_window:
            if event.key() == Qt.Key_Escape:
                self.end_game()
            return

        modifiers = QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            self.sprint = True
        else:
            self.sprint = False
        
        ### Move Keys
        val = ''
        if event.key() == Qt.Key_D:
            val = 'right'
        elif event.key() == Qt.Key_A:
            val = 'left'
        elif event.key() == Qt.Key_W:
            val = 'up'
        elif event.key() == Qt.Key_S:
            val = 'down'
        elif event.key() == Qt.Key_E:
            self.display_inventory()
        
        ### Game operation keys
        elif event.key() == Qt.Key_N:
            self.new_scene_event()
            
        elif event.key() == Qt.Key_M:
            log('Advancing to next scene')
            self.next_scene = True

        elif event.key() == Qt.Key_O:
            if not self.obs_display.displayed:
                self.show_obstacle_dock(self.obs_display)
                self.obs_display.displayed = True
            else:
                self.obstacle_dock.close()
                self.obs_display.displayed = False

        elif event.key() == Qt.Key_L:
            if not self.physics_window.displayed:
                self.show_physics_dock(self.physics_window)
                self.physics_window.displayed = True
            else:
                self.physics_dock.close()
                self.physics_window.displayed = False

        elif event.key() == Qt.Key_B:
            self.prev_scene_event()

        elif event.key() == Qt.Key_Escape:
            log('Exit game called...',color='y')
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
                val = 'left'
            elif event.key() == Qt.Key_W:
                val = 'up'
            elif event.key() == Qt.Key_S:
                val = 'down'
            elif event.key() == Qt.Key_E:
                pass

            while val in self.key_pressed:
                self.key_pressed.remove(val)
        except:
            log('Key release event failed...',color='y')
        
    def game_loop(self):
        curr_time = time.time()

        if self.game_running:
            if self.new_env:
                self.environment.new_environment()
                self.new_env = False
                return

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
            # tic = time.time()
            self.update_dynamics()
            # toc = time.time()
            # print('Update call took: %e'%(toc-tic))

            ### recreate environment and repaint widget
            # tic = time.time()
            self.environment.redraw_scene()
            self.environment.repaint()
            # toc = time.time()
            # print('Drawing call took: %e'%(toc-tic))
            
            # Update game loop tracking information
            self.loop_number += 1
            self.game_time += self.game_timer.interval() / 1000.0
            self.environment.game_time = self.game_time        

        toc = time.time()
        try:
            self.fps_calc.append((1./(toc-curr_time))) 
            self.fps_throttle.append((1./(curr_time-self.prev_fps_time)))
            self.prev_fps_time = curr_time
            if toc-self.fps_time > 0.5:
                self.avgfps = 'MAX FPS: %.2f'%(np.mean(self.fps_calc))
                self.throtfps = 'Throttled FPS: %.2f'%(np.mean(self.fps_throttle))
                self.fps_calc = []
                self.fps_throttle = []
                self.fps_time = toc
        except ZeroDivisionError:
            self.prev_fps_time = curr_time
        
        # Check for game prompts
        # self.prompt_manager.check_prompts()

        # Actions to run only on first game loop
        if self.run_once:
            x,y = 500,350
            for idx in range(0,5):
                self.dynamic_obstacles.ball(x,y,dir=180.)
                x += 150

            self.run_once = False
