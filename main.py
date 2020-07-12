#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, pwd, math
import pathlib

from Utils import *
file_paths = FilePaths()
# user_name = pwd.getpwuid( os.getuid() ).pw_name
# user_path = str(pathlib.Path().absolute()) + '/lib/'
sys.path.insert(1,file_paths.user_path+'lib/')

from PaintUtils import *
from Environment import *
from Player import *
from WelcomeScreen import *

class Game(QMainWindow,FilePaths):
    
    width = 1200
    height = 800
    
    fps = 45.0
    game_time = 0.0
    loop_number = 0

    key_pressed = []
    tod = 'day'

    new_env = False
    next_scene = False
    prev_scene = False

    update_env = False
    exit_game = False

    load = None # If a game is being loaded, set True

    def __init__(self):
        super().__init__()

        # setting title 
        self.setWindowTitle("Game Title")

        screen_width = 1920
        screen_height = 1080
        welcome_width = 800
        welcome_height = 600
        self.setGeometry((screen_width-welcome_width)/2, (screen_height-welcome_height)/2, welcome_width, welcome_height) 

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

        if len(self.key_pressed) != 0:
            self.player.update_position(self.key_pressed)
            self.update_env = True
        
        player_bot = self.player.pose[1] + self.player.size[1]
        ground_top = self.environment.env_snapshot['ground']['origin'][1]
        if player_bot < ground_top:
            self.player.gravity()

        #TODO: check for collisions

    def display_environment(self):
        self.environment = Environment(self.width,self.height,self.player,self.save_file_name,load = self.load,time_of_day = self.tod)
        self.setGeometry(0, 0, self.width, self.height)
        self.setCentralWidget(self.environment)
    
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
            log('New scene called...',color='y')
            self.new_env = True
        
        elif event.key() == Qt.Key_M:
            log('Advancing to next scene')
            self.next_scene = True
        
        elif event.key() == Qt.Key_B:
            log('Switching to previous scene')
            self.prev_scene = True
        
        elif event.key() == Qt.Key_Escape:
            log('Exit game called...',color='y')
            try:
                self.environment.save_game()
                log('Game saved successfully...',color='g')
            except:
                log('Couldn"t save game...',color='r')
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
        
        ### Print the latest key press from last game loop
        # if len(self.key_pressed) != 0:
        #     log(f'Key pressed: {self.key_pressed}')

        ### Update player pose and redraw environment
        self.update_player()

        ### recreate environment and repaint widget
        self.environment.redraw_scene()
        self.environment.repaint()

        # Update game loop tracking information
        # self.key_pressed = []
        self.loop_number += 1
        self.game_time += self.game_timer.interval() / 1000.0

def main():
    # create pyqt5 app 
    app = QApplication(sys.argv) 
    log('Game started...',color='g')

    # Now use a palette to switch to dark colors:
    dark_mode = True
    if dark_mode:
        # palette = QPalette()
        # palette.setColor(QPalette.Window, QColor(53, 53, 53))
        # palette.setColor(QPalette.WindowText, Qt.white)
        # palette.setColor(QPalette.Base, QColor(25, 25, 25))
        # palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        # palette.setColor(QPalette.ToolTipBase, Qt.white)
        # palette.setColor(QPalette.ToolTipText, Qt.white)
        # palette.setColor(QPalette.Text, Qt.white)
        # palette.setColor(QPalette.Button, QColor(53, 53, 53))
        # palette.setColor(QPalette.ButtonText, QColor(255, 153, 85)) #Qt.white
        # palette.setColor(QPalette.BrightText, Qt.red)
        # palette.setColor(QPalette.Link, QColor(255, 153, 85))
        # palette.setColor(QPalette.Highlight, QColor(255, 153, 85))
        # palette.setColor(QPalette.HighlightedText, Qt.black)
        palette = Colors().palette
        app.setPalette(palette)
    
    # create the instance of our Window 
    game_window = Game() 

    # start the app 
    sys.exit(app.exec()) 

if __name__ == '__main__':
    try:
        main()
    finally:
        log('Game ended...',color='g')