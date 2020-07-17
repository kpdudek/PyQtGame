#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, math
import pathlib

# try:
#     import pwd
# except ImportError:
#     import winpwd as pwd

from Utils import *
file_paths = FilePaths()
# user_name = pwd.getpwuid( os.getuid() ).pw_name
# user_path = str(pathlib.Path().absolute()) + '/lib/'
sys.path.insert(1,file_paths.lib_path)

from PaintUtils import *
from Environment import *
from Player import *
from WelcomeScreen import *
from GameController import *

class Game(QMainWindow,FilePaths):
    
    fps = 45.0
    game_time = 0.0
    loop_number = 0

    key_pressed = []
    tod = 'day'

    new_env = False
    next_scene = False
    prev_scene = False

    exit_game = False

    load = None # If a game is being loaded, set True

    def __init__(self,screen):
        super().__init__()
            # Game window dimensions
        self.width = 1800
        self.height = 850

        self.screen_width = screen.size().width()#1920
        self.screen_height = screen.size().height()#1080

        # setting title 
        self.setWindowTitle("Game Title")

        welcome_width = 800
        welcome_height = 500
        self.setGeometry(math.floor((self.screen_width-welcome_width)/2), math.floor((self.screen_height-welcome_height)/2), welcome_width, welcome_height) 

        # Set main widget as main windows central widget
        self.main_widget = WelcomeScreen()
        self.main_widget.load.connect(self.load_game)
        self.main_widget.create.connect(self.start_game)
        self.setCentralWidget(self.main_widget)

        # Show main window
        self.show()

    def load_game(self,name):
        self.load = True
        self.save_file_name = name
        self.player = Player()
        log(f'Loading game called: {self.save_file_name}')
        self.display_environment()

        # Begin game timer and game loop
        self.game_timer = QTimer()
        self.game_timer.setInterval(math.ceil((1.0/self.fps)*1000.0))
        self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start()
        
    def start_game(self,name):
        # Game Elements
        self.player = Player()
        self.save_file_name = name + '.json'
        self.load = False
        log(f'Creating game called: {self.save_file_name}')
        self.display_environment()

        # Begin game timer and game loop
        self.game_timer = QTimer()
        self.game_timer.setInterval(math.ceil((1.0/self.fps)*1000.0))
        self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start()
    
    def update_player(self):
        tmp_player = self.player

        # self.player.drag()
        # if len(self.key_pressed) != 0:
        self.player.update_position(self.key_pressed,self.width,self.height)
        
        player_bot = self.player.pose[1] + self.player.size[1]
        ground_top = self.environment.env_snapshot['ground']['origin'][1]
        # if player_bot < ground_top:
        #     self.player.gravity()
        if player_bot >= ground_top:
            self.player.pose[1] = ground_top - self.player.size[1]
            self.player.physics.velocity[1] = 0

        #TODO: check for collisions

    def display_environment(self):
        self.game_widget = QWidget()
        self.game_layout = QVBoxLayout()
        self.game_widget.setLayout(self.game_layout)
        self.game_layout.setAlignment(Qt.AlignCenter)

        self.game_menu_options = GameMenuOptions()
        self.game_layout.addWidget(self.game_menu_options)
        self.game_menu_options.save_scene_signal.connect(self.save_scene_event)
        self.game_menu_options.exit_game_signal.connect(self.end_game)

        self.environment = Environment(self.width,self.height,self.player,self.save_file_name,load = self.load,time_of_day = self.tod)
        self.game_layout.addWidget(self.environment)

        self.game_controller = GameController()
        self.game_layout.addWidget(self.game_controller)
        self.game_controller.new_scene_signal.connect(self.new_scene_event)
        self.game_controller.prev_scene_signal.connect(self.prev_scene_event)
        self.game_controller.advance_scene_signal.connect(self.advance_scene_event)
        
        # self.setGeometry(15, 15, self.screen_width-30, self.screen_height-30)
        self.showMaximized()
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
    
    def end_game(self):
        self.environment.save_game()
        self.close()

    def keyPressEvent(self, event):
        ### Move Keys
        if event.key() == Qt.Key_D:
            self.key_pressed.append('right')
        elif event.key() == Qt.Key_A:
            self.key_pressed.append('left')
        elif event.key() == Qt.Key_W:
            self.key_pressed.append('up')
        elif event.key() == Qt.Key_S:
            self.key_pressed.append('down')

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
            self.exit_game = True
        else:
            log('Key not recognized...')

    def keyReleaseEvent(self, event):
        try:
            if event.key() == Qt.Key_D:
                self.key_pressed.remove('right')
            elif event.key() == Qt.Key_A:
                self.key_pressed.remove('left')
            elif event.key() == Qt.Key_W:
                self.key_pressed.remove('up')
            elif event.key() == Qt.Key_S:
                self.key_pressed.remove('down')
        except:
            pass
        
    def game_loop(self):
        # Exit game if flag is true
        if self.exit_game:
            self.end_game()
        
        elif self.new_env:
            self.environment.new_environment()
            self.new_env = False

        elif self.prev_scene:
            self.environment.previous_scene()
            self.prev_scene = False
        
        elif self.next_scene:
            self.environment.advance_scene()
            self.next_scene = False

        ### Update player pose and redraw environment
        self.update_player()

        ### recreate environment and repaint widget
        self.environment.redraw_scene()
        self.environment.repaint()

        # Update game loop tracking information
        self.loop_number += 1
        self.game_time += self.game_timer.interval() / 1000.0
        self.environment.game_time = self.game_time

def main():
    # create pyqt5 app
    if sys.platform == 'win32':
        QApplication.setStyle("fusion")
        dark_mode = True

    elif sys.platform == 'linux':   
        QApplication.setStyle("fusion")
        dark_mode = True

    app = QApplication(sys.argv)
    log('Game started...',color='g')

    # Now use a palette to switch to dark colors
    if dark_mode:
        palette = DarkColors().palette
        app.setPalette(palette)
    else:
        palette = FusionColor().palette
        app.setPalette(palette)
    
    # create the instance of our Window 
    game_window = Game(app.primaryScreen()) 

    # start the app 
    sys.exit(app.exec()) 

if __name__ == '__main__':
    try:
        main()
    finally:
        log('Game ended...',color='g')